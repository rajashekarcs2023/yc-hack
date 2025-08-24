#!/usr/bin/env python3
"""
Test Notion MCP client write functionality
"""

import asyncio
from notion_mcp_client import NotionMCPService

async def test_notion_write():
    """Test creating a new page in Notion"""
    
    print("🔍 Testing Notion write functionality...")
    
    try:
        notion_service = NotionMCPService()
        await notion_service.start()
        
        # List available tools first
        tools = await notion_service.list_available_tools()
        print(f"📋 Available tools: {[tool.get('name') for tool in tools]}")
        
        # Test creating a page
        result = await notion_service.create_page(
            title="Test Page from Agent 3",
            content="This is a test page created by the browser testing agent."
        )
        
        print(f"📝 Create page result: {result}")
        
        if result and not result.get('error'):
            print("✅ Notion write functionality works!")
            return True
        else:
            print("❌ Notion write failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        try:
            await notion_service.stop()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_notion_write())
