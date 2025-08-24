#!/usr/bin/env python3
"""
Simple test script for the Notion MCP client.
This will help us verify the connection works before integrating with Dedalus.
"""

import asyncio
import os
from notion_mcp_client import NotionMCPClient, NotionMCPService

async def test_notion_mcp():
    """Test the Notion MCP client with basic operations."""
    
    # Check if we have a Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token or notion_token == "your_notion_integration_token_here":
        print("❌ NOTION_TOKEN not set in .env file")
        print("\nTo test the Notion MCP client, you need to:")
        print("1. Go to https://www.notion.so/profile/integrations")
        print("2. Create a new internal integration")
        print("3. Copy the integration token")
        print("4. Update the NOTION_TOKEN in your .env file")
        print("5. Connect your integration to some pages in your Notion workspace")
        return
    
    print("🔄 Testing Notion MCP Client...")
    print(f"Using token: {notion_token[:10]}...")
    
    try:
        # Test direct client
        print("\n1. Testing direct MCP client:")
        client = NotionMCPClient()
        
        # Initialize connection
        print("   - Initializing connection...")
        init_result = await client.initialize()
        print(f"   ✅ Initialized: {init_result}")
        
        # List available tools
        print("   - Listing available tools...")
        tools = await client.list_tools()
        print(f"   ✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"     • {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
        
        # List available resources
        print("   - Listing available resources...")
        resources = await client.list_resources()
        print(f"   ✅ Found {len(resources)} resources:")
        for resource in resources[:3]:  # Show first 3
            print(f"     • {resource}")
        
        await client.close()
        
        # Test service wrapper
        print("\n2. Testing MCP service wrapper:")
        service = NotionMCPService()
        await service.start()
        
        # Try a search
        print("   - Searching for 'test'...")
        search_results = await service.search("test", limit=3)
        print(f"   ✅ Search completed: {len(search_results)} results")
        
        await service.stop()
        
        print("\n✅ All tests passed! Notion MCP client is working correctly.")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nThis might be because:")
        print("- Your Notion token is invalid")
        print("- Your integration doesn't have access to any pages")
        print("- The Notion MCP server is temporarily unavailable")

if __name__ == "__main__":
    asyncio.run(test_notion_mcp())
