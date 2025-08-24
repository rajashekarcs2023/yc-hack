#!/usr/bin/env python3
"""
First fetch the pixelpilot page content, then write feedback
"""

import asyncio
from datetime import datetime
from dedalus_notion_tool import NotionMCPTool

async def test_fetch_then_write():
    """Fetch page content first, then write feedback"""
    
    print("📖 Fetching pixelpilot page content first...")
    
    try:
        notion_tool = NotionMCPTool()
        pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
        
        # First, fetch the page to see its content
        result = await notion_tool.fetch_notion_page(pixelpilot_page_id)
        
        if result.get("success"):
            content = result.get("content", "")
            
            # Extract text content
            if isinstance(content, list) and len(content) > 0:
                raw_text = content[0].text if hasattr(content[0], 'text') else str(content[0])
            else:
                raw_text = str(content)
            
            print(f"📄 Page content preview (first 500 chars):")
            print("-" * 50)
            print(raw_text[:500])
            print("-" * 50)
            
            # Look for a good anchor point
            lines = raw_text.split('\n')
            anchor_candidates = []
            
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                if line.strip() and len(line.strip()) > 5:
                    anchor_candidates.append(line.strip()[:20] + "...")
            
            print(f"🎯 Potential anchor points:")
            for i, anchor in enumerate(anchor_candidates):
                print(f"  {i+1}. {anchor}")
            
            # Try to write feedback using the first good anchor
            if anchor_candidates:
                test_anchor = anchor_candidates[0]
                
                timestamp = datetime.now().isoformat()[:19]
                test_feedback = f"""

## Test Feedback - {timestamp}

WRITE TEST: Successfully found anchor point and writing feedback.

---
*Test from Fetch Then Write*
"""
                
                print(f"📝 Attempting to write using anchor: {test_anchor}")
                
                await notion_tool._ensure_connected()
                
                write_result = await notion_tool.session.call_tool("notion-update-page", {
                    "data": {
                        "page_id": pixelpilot_page_id,
                        "command": "insert_content_after",
                        "selection_with_ellipsis": test_anchor,
                        "new_str": test_feedback
                    }
                })
                
                print(f"📝 Write result: {write_result}")
                
                if write_result.isError:
                    print(f"❌ Write failed: {write_result.content[0].text}")
                    return False
                else:
                    print("✅ Feedback successfully written!")
                    return True
            else:
                print("❌ No suitable anchor points found")
                return False
        else:
            print("❌ Failed to fetch page content")
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
    result = asyncio.run(test_fetch_then_write())
    print(f"\n🎯 Test Result: {'SUCCESS' if result else 'FAILED'}")
