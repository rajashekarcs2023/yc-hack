#!/usr/bin/env python3
"""
Playwright MCP Client - Browser automation via Anthropic MCP
Similar to notion_mcp_client.py but for Playwright server
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class PlaywrightMCPClient:
    def __init__(self):
        self.session = None
        
    async def connect(self):
        """Connect to Playwright MCP server via npx (remote)"""
        try:
            # Use npx to run the remote Playwright MCP server
            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "@executeautomation/playwright-mcp-server"]
            )
            
            # Properly handle the async context manager
            self.stdio_context = stdio_client(server_params)
            read_stream, write_stream = await self.stdio_context.__aenter__()
            self.session = ClientSession(read_stream, write_stream)
            await self.session.initialize()
            
            print("✅ Connected to Playwright MCP server")
            
            # List available tools
            tools_result = await self.session.list_tools()
            print(f"📋 Available Playwright tools: {len(tools_result.tools)}")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to Playwright MCP server: {e}")
            return False
    
    async def take_screenshot(self, url: str, selector: str = None) -> dict:
        """Take a screenshot of a webpage"""
        try:
            if not self.session:
                await self.connect()
            
            args = {"url": url}
            if selector:
                args["selector"] = selector
            
            result = await self.session.call_tool("screenshot", args)
            return {
                "success": True,
                "content": result.content,
                "screenshot_path": result.content[0].text if result.content else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def navigate_and_click(self, url: str, selector: str) -> dict:
        """Navigate to URL and click an element"""
        try:
            if not self.session:
                await self.connect()
            
            result = await self.session.call_tool("click", {
                "url": url,
                "selector": selector
            })
            
            return {
                "success": True,
                "content": result.content,
                "message": result.content[0].text if result.content else "Click executed"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def extract_text(self, url: str, selector: str = None) -> dict:
        """Extract text content from a webpage"""
        try:
            if not self.session:
                await self.connect()
            
            args = {"url": url}
            if selector:
                args["selector"] = selector
            
            result = await self.session.call_tool("extract_text", args)
            return {
                "success": True,
                "content": result.content,
                "text": result.content[0].text if result.content else ""
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def fill_form(self, url: str, form_data: dict) -> dict:
        """Fill out a form on a webpage"""
        try:
            if not self.session:
                await self.connect()
            
            result = await self.session.call_tool("fill_form", {
                "url": url,
                "form_data": form_data
            })
            
            return {
                "success": True,
                "content": result.content,
                "message": result.content[0].text if result.content else "Form filled"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def wait_for_element(self, url: str, selector: str, timeout: int = 5000) -> dict:
        """Wait for an element to appear on the page"""
        try:
            if not self.session:
                await self.connect()
            
            result = await self.session.call_tool("wait_for_element", {
                "url": url,
                "selector": selector,
                "timeout": timeout
            })
            
            return {
                "success": True,
                "content": result.content,
                "message": result.content[0].text if result.content else "Element found"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def execute_javascript(self, url: str, script: str) -> dict:
        """Execute JavaScript on a webpage"""
        try:
            if not self.session:
                await self.connect()
            
            result = await self.session.call_tool("execute_js", {
                "url": url,
                "script": script
            })
            
            return {
                "success": True,
                "content": result.content,
                "result": result.content[0].text if result.content else ""
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def close(self):
        """Close the MCP session"""
        if hasattr(self, 'stdio_context') and self.stdio_context:
            await self.stdio_context.__aexit__(None, None, None)
            print("🔌 Playwright MCP session closed")

# Test functions
async def test_playwright_screenshot():
    """Test taking a screenshot"""
    client = PlaywrightMCPClient()
    
    try:
        await client.connect()
        
        # Test screenshot of a deployed PixelPilot project
        result = await client.take_screenshot("https://example.com")
        
        if result["success"]:
            print(f"✅ Screenshot taken: {result.get('screenshot_path', 'Success')}")
        else:
            print(f"❌ Screenshot failed: {result['error']}")
        
    finally:
        await client.close()

async def test_playwright_text_extraction():
    """Test extracting text from a webpage"""
    client = PlaywrightMCPClient()
    
    try:
        await client.connect()
        
        # Test text extraction
        result = await client.extract_text("https://example.com", "h1")
        
        if result["success"]:
            print(f"✅ Text extracted: {result['text']}")
        else:
            print(f"❌ Text extraction failed: {result['error']}")
        
    finally:
        await client.close()

if __name__ == "__main__":
    print("🎭 Testing Playwright MCP Client")
    print("=" * 40)
    
    # Test basic connection
    async def test_connection():
        client = PlaywrightMCPClient()
        success = await client.connect()
        if success:
            print("🎉 Playwright MCP client working!")
        await client.close()
    
    asyncio.run(test_connection())
