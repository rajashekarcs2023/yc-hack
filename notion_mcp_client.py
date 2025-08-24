"""Notion MCP Client using mcp-remote
Connects to Notion's hosted MCP server using the mcp-remote proxy approach.
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotionMCPClient:
    def __init__(self, server_url: str = "https://mcp.notion.com/mcp"):
        self.server_url = server_url
        self.session: Optional[ClientSession] = None
        self.stdio_context = None
        # Use mcp-remote to connect to the hosted server
        self.server_params = StdioServerParameters(
            command="npx",
            args=["-y", "mcp-remote", self.server_url]
        )
    
    async def connect(self) -> None:
        """Connect to the hosted Notion MCP server using mcp-remote."""
        if self.session is not None:
            return
            
        logger.info(f"Connecting to hosted Notion MCP server at {self.server_url}...")
        
        try:
            # Create stdio client connection using mcp-remote
            self.stdio_context = stdio_client(self.server_params)
            read, write = await self.stdio_context.__aenter__()
            
            # Create client session
            self.session = ClientSession(read, write)
            
            # Initialize the session
            await self.session.initialize()
            logger.info("Connected to hosted Notion MCP server successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Notion MCP server: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        if self.session:
            await self.session.close()
            self.session = None
        if self.stdio_context:
            await self.stdio_context.__aexit__(None, None, None)
            self.stdio_context = None
        logger.info("Disconnected from Notion MCP server")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the Notion MCP server."""
        if not self.session:
            await self.connect()
        
        result = await self.session.list_tools()
        return [tool.model_dump() for tool in result.tools]
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources from the Notion MCP server."""
        if not self.session:
            await self.connect()
        
        result = await self.session.list_resources()
        return [resource.model_dump() for resource in result.resources]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the Notion MCP server."""
        if not self.session:
            await self.connect()
        
        result = await self.session.call_tool(name, arguments)
        return result.model_dump()
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource from the Notion MCP server."""
        if not self.session:
            await self.connect()
        
        result = await self.session.read_resource(uri)
        return result.model_dump()
    
    async def search_pages(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Notion pages using the search tool."""
        try:
            result = await self.call_tool("search_pages", {
                "query": query,
                "limit": limit
            })
            return result.get("content", [])
        except Exception as e:
            logger.error(f"Error searching pages: {e}")
            return []
    
    async def get_page_content(self, page_id: str) -> Dict[str, Any]:
        """Get content of a specific Notion page."""
        try:
            result = await self.call_tool("get_page", {
                "page_id": page_id
            })
            return result
        except Exception as e:
            logger.error(f"Error getting page content: {e}")
            return {}
    
    async def create_page(self, title: str, content: str, parent_id: str = None) -> Dict[str, Any]:
        """Create a new Notion page."""
        try:
            arguments = {
                "title": title,
                "content": content
            }
            if parent_id:
                arguments["parent_id"] = parent_id
                
            result = await self.call_tool("create_page", arguments)
            return result
        except Exception as e:
            logger.error(f"Error creating page: {e}")
            return {}


class NotionMCPService:
    """Service wrapper for the Notion MCP Client with a simple API."""
    
    def __init__(self):
        self.client = NotionMCPClient()
        self.initialized = False
    
    async def start(self):
        """Start the Notion MCP service."""
        if not self.initialized:
            await self.client.connect()
            self.initialized = True
            logger.info("Notion MCP Service started successfully")
    
    async def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Notion workspace."""
        if not self.initialized:
            await self.start()
        return await self.client.search_pages(query, limit)
    
    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get a specific page from Notion."""
        if not self.initialized:
            await self.start()
        return await self.client.get_page_content(page_id)
    
    async def create_page(self, title: str, content: str, parent_id: str = None) -> Dict[str, Any]:
        """Create a new page in Notion."""
        if not self.initialized:
            await self.start()
        return await self.client.create_page(title, content, parent_id)
    
    async def list_available_resources(self) -> List[Dict[str, Any]]:
        """List all available Notion resources."""
        if not self.initialized:
            await self.start()
        return await self.client.list_resources()
    
    async def list_available_tools(self) -> List[Dict[str, Any]]:
        """List all available Notion tools."""
        if not self.initialized:
            await self.start()
        return await self.client.list_tools()
    
    async def stop(self):
        """Stop the service."""
        await self.client.disconnect()


# Example usage
async def main():
    service = NotionMCPService()
    
    try:
        # Start the service
        await service.start()
        
        # List available resources
        resources = await service.list_available_resources()
        print("Available Resources:")
        for resource in resources:
            print(f"  - {resource}")
        
        # List available tools
        tools = await service.list_available_tools()
        print("\nAvailable Tools:")
        for tool in tools:
            print(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
        
        # Example search
        results = await service.search("meeting notes", limit=5)
        print(f"\nSearch Results for 'meeting notes': {len(results)} found")
        for result in results:
            print(f"  - {result}")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        await service.stop()

if __name__ == "__main__":
    asyncio.run(main())
