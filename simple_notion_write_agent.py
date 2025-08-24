#!/usr/bin/env python3
"""
Simple Dedalus Agent to test Notion writing functionality only
"""

import asyncio
from datetime import datetime
from dedalus_labs import AsyncDedalus, DedalusRunner
from dedalus_notion_tool import NotionMCPTool

# Simple Dedalus agent that only tests writing to Notion
agent_definition = {
    "name": "NotionWriteTestAgent",
    "description": "Simple agent to test writing feedback to Notion pixelpilot document",
    "tools": [
        {
            "name": "write_test_feedback",
            "description": "Write test feedback to pixelpilot Notion document",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Test message to write"
                    }
                },
                "required": ["message"]
            }
        }
    ]
}

class NotionWriteTestAgent:
    def __init__(self):
        self.notion_tool = NotionMCPTool()
        self.pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
    
    async def write_test_feedback(self, message: str) -> str:
        """Test writing feedback to Notion document"""
        print(f"📝 Testing write to Notion: {message}")
        
        try:
            timestamp = datetime.now().isoformat()[:19]
            
            # Format test feedback
            test_content = f"""

## Test Feedback - {timestamp}

{message}

---
*Test from Simple Notion Write Agent*
"""
            
            # For now, let's see what tools are available in the Notion MCP
            print("🔍 Checking available Notion tools...")
            
            # Try to connect and see what we can do
            await self.notion_tool._ensure_connected()
            
            # List available tools
            if self.notion_tool.session:
                tools_result = await self.notion_tool.session.list_tools()
                print(f"Available tools: {[tool.name for tool in tools_result.tools]}")
                
                # Try to find an update or append method
                for tool in tools_result.tools:
                    print(f"Tool: {tool.name} - {tool.description}")
            
            return f"SUCCESS: Connected to Notion and prepared feedback content ({len(test_content)} chars)"
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"ERROR: {str(e)}"
        finally:
            try:
                await self.notion_tool.exit_stack.aclose()
            except:
                pass

async def test_notion_write_agent():
    """Test the simple Notion write agent"""
    print("🤖 Simple Notion Write Test Agent")
    print("=" * 50)
    
    agent = NotionWriteTestAgent()
    
    test_message = """
IMPLEMENTATION SUMMARY
=====================

SPEC COMPLIANCE: 8/10 (Test)

WHAT'S WORKING:
- Agent connection
- Notion MCP setup
- Tool discovery

WHAT'S MISSING/NEEDS IMPROVEMENT:
- Actual write functionality
- Update page method

RECOMMENDATIONS FOR NEXT ITERATION:
- Find correct update tool
- Test with real feedback

PRIORITY: HIGH - Testing write capability
"""
    
    result = await agent.write_test_feedback(test_message)
    print(f"\n🎯 Result: {result}")
    
    return "SUCCESS" in result

if __name__ == "__main__":
    asyncio.run(test_notion_write_agent())
