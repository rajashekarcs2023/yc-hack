#!/usr/bin/env python3
"""
Simple Playwright MCP Client using documented tools
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class SimplePlaywrightClient:
    def __init__(self):
        self.session = None
        self.stdio_context = None
        
    async def connect(self):
        """Connect to Playwright MCP server"""
        try:
            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "@executeautomation/playwright-mcp-server"]
            )
            
            self.stdio_context = stdio_client(server_params)
            read_stream, write_stream = await self.stdio_context.__aenter__()
            self.session = ClientSession(read_stream, write_stream)
            await self.session.initialize()
            
            print("✅ Connected to Playwright MCP server")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def navigate(self, url: str, width: int = 1280, height: int = 720) -> dict:
        """Navigate to a URL"""
        try:
            result = await self.session.call_tool("Playwright_navigate", {
                "url": url,
                "width": width,
                "height": height,
                "headless": False
            })
            return {"success": True, "message": "Navigation successful"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def screenshot(self, name: str = "screenshot", full_page: bool = True) -> dict:
        """Take a screenshot"""
        try:
            result = await self.session.call_tool("Playwright_screenshot", {
                "name": name,
                "fullPage": full_page,
                "savePng": True
            })
            return {"success": True, "message": f"Screenshot saved as {name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_visible_text(self) -> dict:
        """Get visible text from current page"""
        try:
            result = await self.session.call_tool("playwright_get_visible_text", {})
            content = result.content[0].text if result.content else ""
            return {"success": True, "text": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def click(self, selector: str) -> dict:
        """Click an element"""
        try:
            result = await self.session.call_tool("Playwright_click", {
                "selector": selector
            })
            return {"success": True, "message": f"Clicked {selector}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def fill(self, selector: str, value: str) -> dict:
        """Fill an input field"""
        try:
            result = await self.session.call_tool("Playwright_fill", {
                "selector": selector,
                "value": value
            })
            return {"success": True, "message": f"Filled {selector} with {value}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def execute_js(self, script: str) -> dict:
        """Execute JavaScript"""
        try:
            result = await self.session.call_tool("Playwright_evaluate", {
                "script": script
            })
            return {"success": True, "result": result.content[0].text if result.content else ""}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def close(self):
        """Close browser and session"""
        try:
            if self.session:
                await self.session.call_tool("Playwright_close", {})
            if self.stdio_context:
                await self.stdio_context.__aexit__(None, None, None)
            print("🔌 Playwright session closed")
        except Exception as e:
            print(f"⚠️ Error closing session: {e}")

# Test deployed PixelPilot app
async def test_pixelpilot_deployment(url: str):
    """Test a deployed PixelPilot app"""
    client = SimplePlaywrightClient()
    
    try:
        print(f"🎭 Testing PixelPilot deployment: {url}")
        
        # Connect to Playwright
        if not await client.connect():
            return False
        
        # Navigate to the deployed app
        nav_result = await client.navigate(url)
        if not nav_result["success"]:
            print(f"❌ Navigation failed: {nav_result['error']}")
            return False
        
        print("✅ Navigation successful")
        
        # Take a screenshot
        screenshot_result = await client.screenshot("pixelpilot-test")
        if screenshot_result["success"]:
            print("✅ Screenshot captured")
        
        # Get visible text to verify content
        text_result = await client.get_visible_text()
        if text_result["success"]:
            text = text_result["text"]
            print(f"📄 Page content preview: {text[:200]}...")
            
            # Check for key elements
            if "John Doe" in text:
                print("✅ Found 'John Doe' - ProfileCard working")
            if "Like" in text:
                print("✅ Found 'Like' button - Interactive element present")
        
        # Try to click the Like button if it exists
        try:
            click_result = await client.click("button")
            if click_result["success"]:
                print("✅ Successfully clicked button")
        except:
            print("ℹ️ No clickable button found")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        await client.close()

# Quick connection test
async def test_connection():
    """Test basic connection to Playwright MCP"""
    client = SimplePlaywrightClient()
    
    try:
        success = await client.connect()
        if success:
            print("🎉 Playwright MCP client working!")
            
            # List available tools
            tools_result = await client.session.list_tools()
            print(f"📋 Available tools: {len(tools_result.tools)}")
            for tool in tools_result.tools[:5]:  # Show first 5
                print(f"  - {tool.name}")
            
        return success
    
    finally:
        await client.close()

if __name__ == "__main__":
    print("🎭 Simple Playwright MCP Client")
    print("=" * 40)
    
    # Test connection first
    asyncio.run(test_connection())
