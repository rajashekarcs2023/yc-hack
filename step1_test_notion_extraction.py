#!/usr/bin/env python3
"""
Step 1: Test Notion Specs Extraction
====================================

Test if we can successfully extract PixelPilot specs from Notion.
"""

import asyncio
from dedalus_notion_tool import NotionMCPTool

async def test_notion_extraction():
    """Test extracting specs from Notion."""
    print("🔍 Step 1: Testing Notion Specs Extraction")
    print("=" * 50)
    
    notion_tool = NotionMCPTool()
    pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
    
    try:
        print("📖 Connecting to Notion MCP...")
        result = await notion_tool.fetch_notion_page(pixelpilot_page_id)
        
        if result.get("success"):
            content = result.get("content", "")
            
            # Extract text from MCP response
            if isinstance(content, list) and len(content) > 0:
                raw_text = content[0].text if hasattr(content[0], 'text') else str(content[0])
            else:
                raw_text = str(content)
            
            # Parse the JSON-like response to extract clean specs
            import json
            try:
                # Try to parse as JSON first
                parsed = json.loads(raw_text)
                specs_text = parsed.get("text", raw_text)
                
                # Extract content between <content> tags if present
                if "<content>" in specs_text and "</content>" in specs_text:
                    start = specs_text.find("<content>") + len("<content>")
                    end = specs_text.find("</content>")
                    specs_text = specs_text[start:end].strip()
                
            except json.JSONDecodeError:
                # If not JSON, use raw text
                specs_text = raw_text
            
            print("✅ Specs extracted successfully!")
            print(f"📄 Raw content length: {len(raw_text)} characters")
            print(f"📄 Clean specs length: {len(specs_text)} characters")
            print("\n📋 Clean specs preview:")
            print("-" * 30)
            print(specs_text[:500] + "..." if len(specs_text) > 500 else specs_text)
            print("-" * 30)
            
            return specs_text
            
        else:
            print(f"❌ Failed to extract specs: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_notion_extraction())
