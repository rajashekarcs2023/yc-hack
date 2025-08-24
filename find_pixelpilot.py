#!/usr/bin/env python3
"""
Find and access the PixelPilot specification document in Notion.
"""

import asyncio
from mcp_client import MCPClient

async def find_pixelpilot_spec():
    """Search for and access the PixelPilot specification document."""
    client = MCPClient()
    
    try:
        # Connect to hosted Notion MCP server
        await client.connect_to_hosted_server()
        
        print("🔍 Searching for PixelPilot specification document...")
        print("=" * 60)
        
        # First, let's see what tools are available
        print("\n🔧 Available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  • {tool.name}: {tool.description[:80]}...")
        
        # Search for pixelpilot document
        search_terms = ["pixelpilot", "pixel pilot", "PixelPilot", "spec", "specification"]
        
        for term in search_terms:
            print(f"\n📋 Searching for '{term}':")
            try:
                search_result = await client.call_tool("search", {
                    "query": term,
                    "query_type": "internal"
                })
                
                if hasattr(search_result, 'content') and search_result.content:
                    content = search_result.content
                    if isinstance(content, list):
                        print(f"✅ Found {len(content)} results:")
                        for i, result in enumerate(content, 1):
                            print(f"  {i}. {result}")
                    else:
                        print(f"✅ Found content: {str(content)[:500]}...")
                else:
                    print("❌ No results found")
                    
            except Exception as e:
                print(f"❌ Search failed: {e}")
        
        # Also try searching for "specification" or "spec"
        print(f"\n📋 Searching for 'specification':")
        try:
            search_result = await client.call_tool("search", {
                "query": "specification",
                "query_type": "internal"
            })
            
            if hasattr(search_result, 'content') and search_result.content:
                content = search_result.content
                if isinstance(content, list):
                    print(f"✅ Found {len(content)} specification documents:")
                    for i, result in enumerate(content, 1):
                        print(f"  {i}. {result}")
                        # Look for pixelpilot in the results
                        if "pixelpilot" in str(result).lower():
                            print(f"    🎯 This might be our PixelPilot spec!")
                else:
                    print(f"✅ Found content: {str(content)[:500]}...")
            else:
                print("❌ No specification documents found")
                
        except Exception as e:
            print(f"❌ Search failed: {e}")
        
        # List available resources to see what we can access
        print(f"\n📚 Available resources:")
        try:
            resources = await client.list_resources()
            for resource in resources:
                print(f"  • {resource.name} ({resource.uri})")
                if "pixelpilot" in resource.name.lower():
                    print(f"    🎯 Found PixelPilot resource!")
                    
                    # Try to read this resource
                    print(f"    📖 Reading content...")
                    try:
                        resource_content = await client.read_resource(resource.uri)
                        print(f"    ✅ Content preview: {str(resource_content.contents)[:300]}...")
                    except Exception as e:
                        print(f"    ❌ Failed to read: {e}")
        except Exception as e:
            print(f"❌ Failed to list resources: {e}")
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(find_pixelpilot_spec())
