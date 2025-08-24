#!/usr/bin/env python3
"""
Debug Notion MCP connection and tools
"""

import asyncio
from notion_mcp_client import NotionMCPService

async def debug_notion():
    """Debug Notion MCP connection step by step"""
    
    print("🔍 Debugging Notion MCP connection...")
    
    try:
        notion_service = NotionMCPService()
        print("✅ NotionMCPService created")
        
        # Start the service
        print("🚀 Starting Notion service...")
        await notion_service.start()
        print("✅ Notion service started")
        
        # List available tools
        print("🛠️ Listing available tools...")
        tools = await notion_service.list_available_tools()
        print(f"Available tools ({len(tools)}):")
        for tool in tools:
            print(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
        
        # Test search
        print("\n🔍 Testing search...")
        results = await notion_service.search("pixelpilot", limit=3)
        print(f"Search results: {len(results)} found")
        
        for i, result in enumerate(results):
            print(f"Result {i+1}:")
            print(f"  Keys: {list(result.keys())}")
            if 'title' in result:
                print(f"  Title: {result['title']}")
            if 'id' in result:
                print(f"  ID: {result['id']}")
            if 'page_id' in result:
                print(f"  Page ID: {result['page_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            await notion_service.stop()
            print("🛑 Notion service stopped")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(debug_notion())
