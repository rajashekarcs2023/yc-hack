#!/usr/bin/env python3
"""
Test actual Notion writing using the notion-update-page tool
"""

import asyncio
from datetime import datetime
from dedalus_notion_tool import NotionMCPTool

async def test_actual_notion_write():
    """Test writing feedback to pixelpilot document using notion-update-page"""
    
    print("📝 Testing actual Notion write with notion-update-page...")
    
    try:
        notion_tool = NotionMCPTool()
        pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
        
        await notion_tool._ensure_connected()
        
        timestamp = datetime.now().isoformat()[:19]
        
        # Test feedback content
        test_feedback = f"""

## Test Feedback - {timestamp}

IMPLEMENTATION SUMMARY
=====================

SPEC COMPLIANCE: 8/10 (Test Write)

WHAT'S WORKING:
- Notion MCP connection ✅
- Tool discovery ✅
- Page ID resolution ✅

WHAT'S MISSING/NEEDS IMPROVEMENT:
- Testing actual write functionality

RECOMMENDATIONS FOR NEXT ITERATION:
- Verify feedback appears in Notion
- Test with Agent 3 integration

PRIORITY: HIGH - Testing write capability

---
*Test from Actual Notion Write Test*
"""
        
        # Use notion-update-page with insert_content_after
        print("📝 Attempting to write feedback using notion-update-page...")
        
        result = await notion_tool.session.call_tool("notion-update-page", {
            "data": {
                "page_id": pixelpilot_page_id,
                "command": "insert_content_after",
                "selection_with_ellipsis": "# PixelPilot...",  # Insert after the main title
                "new_str": test_feedback
            }
        })
        
        print(f"📝 Write result: {result}")
        
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
            await notion_tool.exit_stack.aclose()
        except:
            pass

if __name__ == "__main__":
    result = asyncio.run(test_actual_notion_write())
    print(f"\n🎯 Test Result: {'SUCCESS' if result else 'FAILED'}")
