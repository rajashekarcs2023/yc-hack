#!/usr/bin/env python3
"""
Quick exploration script to see what resources and pages are available
through the Notion MCP client.
"""

import asyncio
from mcp_client import MCPClient

async def explore_notion():
    """Explore available Notion resources and test search functionality."""
    client = MCPClient()
    
    try:
        # Connect to hosted Notion MCP server
        await client.connect_to_hosted_server()
        
        print("\n" + "="*60)
        print("EXPLORING NOTION MCP ACCESS")
        print("="*60)
        
        # 1. List available tools
        print("\n1. AVAILABLE TOOLS:")
        print("-" * 30)
        tools = await client.list_tools()
        for tool in tools:
            print(f"• {tool.name}")
            print(f"  Description: {tool.description[:100]}...")
            print()
        
        # 2. List available resources
        print("\n2. AVAILABLE RESOURCES:")
        print("-" * 30)
        resources = await client.list_resources()
        for resource in resources:
            print(f"• {resource.name} ({resource.uri})")
            print(f"  Description: {getattr(resource, 'description', 'No description')}")
            print()
        
        # 3. Try a simple search to see what pages we can access
        print("\n3. TESTING SEARCH - Looking for any pages:")
        print("-" * 30)
        try:
            search_result = await client.call_tool("search", {
                "query": "",  # Empty query to see what's available
                "query_type": "internal"
            })
            print("Search result:")
            print(search_result.content)
        except Exception as e:
            print(f"Search failed: {e}")
        
        # 4. Try searching for common terms
        print("\n4. TESTING SEARCH - Common terms:")
        print("-" * 30)
        search_terms = ["meeting", "project", "notes", "todo", "task"]
        
        for term in search_terms:
            try:
                print(f"\nSearching for '{term}':")
                search_result = await client.call_tool("search", {
                    "query": term,
                    "query_type": "internal"
                })
                print(f"Found results: {len(search_result.content) if isinstance(search_result.content, list) else 'N/A'}")
                if hasattr(search_result, 'content') and search_result.content:
                    # Show first result if available
                    content = search_result.content
                    if isinstance(content, list) and len(content) > 0:
                        print(f"First result: {content[0]}")
                    else:
                        print(f"Content: {str(content)[:200]}...")
            except Exception as e:
                print(f"Search for '{term}' failed: {e}")
        
        # 5. Try to read the available resource
        print("\n5. READING AVAILABLE RESOURCES:")
        print("-" * 30)
        for resource in resources:
            try:
                print(f"\nReading resource: {resource.name}")
                resource_content = await client.read_resource(resource.uri)
                print(f"Content preview: {str(resource_content.contents)[:300]}...")
            except Exception as e:
                print(f"Failed to read resource {resource.name}: {e}")
        
    except Exception as e:
        print(f"Error during exploration: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(explore_notion())
