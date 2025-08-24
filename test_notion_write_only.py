#!/usr/bin/env python3
"""
Test only the Notion writing functionality
"""

import asyncio
from notion_mcp_client import NotionMCPService

async def test_notion_write():
    """Test writing feedback to pixelpilot document"""
    
    print("🔍 Testing Notion write functionality...")
    
    try:
        notion_service = NotionMCPService()
        await notion_service.start()
        
        # Search for pixelpilot document
        print("📋 Searching for pixelpilot document...")
        results = await notion_service.search("pixelpilot", limit=5)
        print(f"Found {len(results)} results")
        
        if not results:
            print("❌ No pixelpilot document found")
            return False
        
        # Get the first result
        page_data = results[0]
        page_id = page_data.get('id') or page_data.get('page_id')
        
        if not page_id:
            print("❌ Could not extract page ID")
            print(f"Page data: {page_data}")
            return False
        
        print(f"📄 Found pixelpilot page ID: {page_id}")
        
        # Test feedback content
        test_feedback = """

## Test Feedback - Individual Write Test

IMPLEMENTATION SUMMARY
=====================

SPEC COMPLIANCE: 8/10 (Test)

WHAT'S WORKING:
- Notion MCP client connection
- Search functionality
- Page ID extraction

WHAT'S MISSING/NEEDS IMPROVEMENT:
- Need to verify update-page functionality

RECOMMENDATIONS FOR NEXT ITERATION:
- Test complete Agent 3 workflow
- Verify feedback appears in Notion

PRIORITY: HIGH - Testing write functionality

---
*Test feedback from PixelPilot Agent 3 - Individual Test*
"""
        
        # Try to update the page
        print("📝 Attempting to write feedback...")
        result = await notion_service.update_page(page_id, content=test_feedback)
        
        print(f"📝 Update result: {result}")
        
        if result and not result.get('error'):
            print("✅ Feedback successfully written to Notion!")
            return True
        else:
            print(f"❌ Failed to write feedback: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            await notion_service.stop()
        except:
            pass

if __name__ == "__main__":
    result = asyncio.run(test_notion_write())
    print(f"\n🎯 Test Result: {'SUCCESS' if result else 'FAILED'}")
