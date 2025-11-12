"""
Dedalus tool for accessing Notion data through the MCP client.
This tool can be used by Dedalus to search and retrieve Notion content.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()

class NotionMCPTool:
    """Tool for Dedalus to access Notion data via MCP client."""
    
    def __init__(self, server_url: str = "https://mcp.notion.com/mcp"):
        self.server_url = server_url
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.connected = False
    
    async def _ensure_connected(self):
        """Ensure MCP connection is established."""
        if not self.connected:
            # Use mcp-remote to connect to hosted server
            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "mcp-remote", self.server_url],
                env=None
            )
            
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            
            await self.session.initialize()
            self.connected = True
    
    async def search_notion(self, query: str, query_type: str = "internal") -> Dict[str, Any]:
        """Search Notion workspace for pages matching the query."""
        try:
            await self._ensure_connected()
            result = await self.session.call_tool("search", {
                "query": query,
                "query_type": query_type
            })
            return {"results": result.content, "success": True}
        except Exception as e:
            return {"error": f"Failed to search Notion: {str(e)}", "success": False}
    
    async def fetch_notion_page(self, page_url_or_id: str) -> Dict[str, Any]:
        """Get a specific page from Notion."""
        try:
            await self._ensure_connected()
            result = await self.session.call_tool("fetch", {
                "id": page_url_or_id
            })
            return {"content": result.content, "success": True}
        except Exception as e:
            return {"error": f"Failed to fetch Notion page: {str(e)}", "success": False}
    
    async def create_notion_page(self, title: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new Notion page."""
        try:
            await self._ensure_connected()
            
            pages_data = {
                "pages": [{
                    "properties": {"title": title},
                    "content": content
                }]
            }
            
            if parent_id:
                pages_data["parent"] = {"page_id": parent_id}
            
            result = await self.session.call_tool("notion-create-pages", pages_data)
            return {"result": result.content, "success": True}
        except Exception as e:
            return {"error": f"Failed to create Notion page: {str(e)}", "success": False}
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available Notion MCP tools."""
        try:
            await self._ensure_connected()
            result = await self.session.list_tools()
            tools = [{
                "name": tool.name,
                "description": tool.description
            } for tool in result.tools]
            return {"tools": tools, "success": True}
        except Exception as e:
            return {"error": f"Failed to list tools: {str(e)}", "success": False}
    
    async def close(self):
        """Close the MCP connection."""
        if self.connected:
            await self.exit_stack.aclose()
            self.connected = False

# Functions that Dedalus can call
async def search_notion_for_dedalus(query: str, query_type: str = "internal") -> str:
    """
    Search Notion workspace and return formatted results for Dedalus.
    
    Args:
        query: Search query string
        query_type: Type of search ("internal" or "user")
    
    Returns:
        Formatted string with search results
    """
    tool = NotionMCPTool()
    
    try:
        # Perform the search
        results = await tool.search_notion(query, query_type)
        
        if not results.get("success"):
            return f"Error searching Notion: {results.get('error', 'Unknown error')}"
        
        # Format the results
        search_results = results.get('results', [])
        if isinstance(search_results, list):
            formatted_results = f"Found {len(search_results)} results for '{query}':\n\n"
            for i, result in enumerate(search_results, 1):
                formatted_results += f"{i}. {result}\n"
        else:
            formatted_results = f"Search results for '{query}':\n{search_results}"
        
        return formatted_results
        
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    finally:
        await tool.close()

async def fetch_notion_page_for_dedalus(page_url_or_id: str) -> str:
    """
    Get a specific Notion page and return formatted content for Dedalus.
    
    Args:
        page_url_or_id: The URL or ID of the Notion page to retrieve
    
    Returns:
        Formatted string with page content
    """
    tool = NotionMCPTool()
    
    try:
        # Get the page
        page_data = await tool.fetch_notion_page(page_url_or_id)
        
        if not page_data.get("success"):
            return f"Error fetching Notion page: {page_data.get('error', 'Unknown error')}"
        
        # Format the page data
        content = page_data.get('content', '')
        formatted_page = f"Page: {page_url_or_id}\n\n{content}"
        
        return formatted_page
        
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    finally:
        await tool.close()

async def create_notion_page_for_dedalus(title: str, content: str, parent_id: Optional[str] = None) -> str:
    """
    Create a new Notion page for Dedalus.
    
    Args:
        title: Page title
        content: Page content in Markdown
        parent_id: Optional parent page ID
    
    Returns:
        Formatted string with creation result
    """
    tool = NotionMCPTool()
    
    try:
        result = await tool.create_notion_page(title, content, parent_id)
        
        if not result.get("success"):
            return f"Error creating Notion page: {result.get('error', 'Unknown error')}"
        
        return f"Successfully created page '{title}': {result.get('result', '')}"
        
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    finally:
        await tool.close()

# Example usage with Dedalus
async def main():
    """Example of how to use the Notion tool with Dedalus."""
    
    # Test the Notion tool directly
    print("Testing Notion tool...")
    search_result = await search_notion_for_dedalus("meeting notes")
    print("Search Result:")
    print(search_result)
    
    # Example of using with Dedalus
    print("\nTesting with Dedalus...")
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    # Create a prompt that uses the Notion search
    prompt = """
    I need to search my Notion workspace for information about "project planning".
    Please help me find relevant pages and summarize what you find.
    
    Use this function to search: search_notion_for_dedalus("project planning", 10)
    """
    
    try:
        result = await runner.run(
            input=prompt,
            model="openai/gpt-4o-mini",
            stream=False
        )
        
        print("Dedalus Result:")
        print(result.final_output)
        
    except Exception as e:
        print(f"Error with Dedalus: {e}")

if __name__ == "__main__":
    asyncio.run(main())
