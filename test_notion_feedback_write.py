#!/usr/bin/env python3
"""
Test writing feedback to Notion pixelpilot document
"""

import asyncio
from notion_mcp_client import NotionMCPService

async def test_feedback_write():
    """Test writing feedback to pixelpilot document"""
    
    print("🔍 Testing feedback write to Notion...")
    
    try:
        notion_service = NotionMCPService()
        await notion_service.start()
        
        # Search for pixelpilot document
        results = await notion_service.search("pixelpilot", limit=5)
        print(f"📋 Found {len(results)} results")
        
        if not results:
            print("❌ No pixelpilot document found")
            return False
        
        # Get the first result
        page_data = results[0]
        page_id = page_data.get('id') or page_data.get('page_id')
        
        if not page_id:
            print("❌ Could not extract page ID")
            return False
        
        print(f"📄 Found pixelpilot page ID: {page_id}")
        
        # Test feedback content
        test_feedback = """

## Feedback - Test

IMPLEMENTATION SUMMARY
=====================

SPEC COMPLIANCE: 7/10

WHAT'S WORKING:
- Profile card layout
- Like button functionality
- Text content display

WHAT'S MISSING/NEEDS IMPROVEMENT:
- Profile picture implementation

RECOMMENDATIONS FOR NEXT ITERATION:
- Add profile picture feature
- Test on mobile devices

PRIORITY: HIGH - Missing core feature

---
*Test feedback from PixelPilot Agent 3*
"""
        
        # Try to update the page by appending feedback
        result = await notion_service.client.call_tool("update-page", {
            "page_id": page_id,
            "content": test_feedback
        })
        
        print(f"📝 Update result: {result}")
        
        if result and not result.get('error'):
            print("✅ Feedback successfully written to Notion!")
            return True
        else:
            print(f"❌ Failed to write feedback: {result}")
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
    asyncio.run(test_feedback_write())
