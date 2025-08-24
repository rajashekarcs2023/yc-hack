#!/usr/bin/env python3
"""
Read the full PixelPilot specification document directly using its page ID.
"""

import asyncio
from mcp_client import MCPClient

async def read_pixelpilot_spec():
    """Read the full PixelPilot specification document."""
    client = MCPClient()
    
    try:
        # Connect to hosted Notion MCP server
        await client.connect_to_hosted_server()
        
        print("📖 Reading PixelPilot specification document...")
        print("=" * 60)
        
        # Use the page ID we found: 258bd31b-99b8-80b3-9a92-ffbbadb0b85f
        page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
        
        try:
            # Try to fetch the page content using the fetch tool with correct parameter
            page_result = await client.call_tool("fetch", {
                "id": page_id
            })
            
            print("✅ Successfully retrieved PixelPilot specification:")
            print("-" * 60)
            print(page_result.content)
            
        except Exception as e:
            print(f"❌ Failed to fetch page: {e}")
            
            # Try using the page URL format
            try:
                page_url = f"https://www.notion.so/{page_id.replace('-', '')}"
                page_result = await client.call_tool("fetch", {
                    "id": page_url
                })
                
                print("✅ Successfully retrieved via URL:")
                print("-" * 60)
                print(page_result.content)
                
            except Exception as e2:
                print(f"❌ URL fetch also failed: {e2}")
                
                # Fallback to search with more specific query
                try:
                    search_result = await client.call_tool("search", {
                        "query": "Profile Card Component Spec Design Tokens",
                        "query_type": "internal"
                    })
                    
                    print("✅ Found via detailed search:")
                    print("-" * 60)
                    if hasattr(search_result, 'content'):
                        print(search_result.content)
                        
                except Exception as e3:
                    print(f"❌ All methods failed: {e3}")
        
        # List available tools to see what we can use
        print("\n🔧 Available tools for page access:")
        tools = await client.list_tools()
        for tool in tools:
            if "page" in tool.name.lower() or "get" in tool.name.lower():
                print(f"  • {tool.name}: {tool.description[:100]}...")
        
    except Exception as e:
        print(f"❌ Error during read: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(read_pixelpilot_spec())
