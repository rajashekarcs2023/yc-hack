#!/usr/bin/env python3
"""
Browser Testing Agent - Uses Browser Use to test deployed apps and write feedback to Notion
"""

import asyncio
import os
from datetime import datetime
from browser_use import Agent
from browser_use.llm import ChatOpenAI, ChatAnthropic
from dotenv import load_dotenv
import json
import subprocess

# Import our existing Notion client
from notion_mcp_client import NotionMCPClient

load_dotenv()

class BrowserTestingAgent:
    def __init__(self):
        # Use Claude for browser testing (better vision capabilities)
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        self.notion_client = None
        
    async def get_original_specs(self) -> str:
        """Extract original specs from Notion pixelpilot document"""
        try:
            from notion_mcp_client import NotionMCPService
            
            notion_service = NotionMCPService()
            await notion_service.start()
            
            # Search for pixelpilot document
            results = await notion_service.search("pixelpilot", limit=5)
            
            if not results:
                print("⚠️ No pixelpilot specs found in Notion")
                return "No original specifications found."
            
            # Get the first pixelpilot page
            page_data = results[0]
            page_id = page_data.get('id') or page_data.get('page_id')
            
            if page_id:
                page_content = await notion_service.get_page(page_id)
                specs = page_content.get('content', 'No content found')
                print("✅ Original specs extracted from Notion")
                return specs
            else:
                print("⚠️ Could not find pixelpilot page ID")
                return "Original specifications not accessible."
                
        except Exception as e:
            print(f"⚠️ Failed to get original specs: {e}")
            return "Error retrieving original specifications."
        finally:
            try:
                await notion_service.stop()
            except:
                pass

    async def test_deployed_app(self, url: str, project_name: str = "pixelpilot-project") -> dict:
        """Test a deployed app against original specs and return structured feedback"""
        
        print(f"🎭 Testing deployed app: {url}")
        
        # First, get the original specs from Notion
        original_specs = await self.get_original_specs()
        
        # Create browser agent with spec-based testing task
        agent = Agent(
            task=f"""
            Test this deployed web application: {url}
            
            IMPORTANT: You need to evaluate how well this implementation matches the original specifications.
            
            ORIGINAL SPECIFICATIONS:
            {original_specs}
            
            Please perform the following comprehensive testing:
            1. Navigate to the URL and take a screenshot
            2. Compare the visual design against the original specs
            3. Test any interactive elements mentioned in specs
            4. Check if all required features are implemented
            5. Evaluate how closely it matches the specified requirements
            6. Look for any missing features or deviations
            
            Provide detailed feedback on:
            - SPEC COMPLIANCE: How well does it match the original requirements? (1-10)
            - MISSING FEATURES: What's missing from the specs?
            - EXTRA FEATURES: What was added beyond specs?
            - VISUAL ACCURACY: Does the design match spec descriptions?
            - FUNCTIONALITY: Do interactive elements work as specified?
            - OVERALL IMPLEMENTATION QUALITY: (1-10)
            
            Be specific about what matches the specs and what doesn't.
            """,
            llm=self.llm,
            use_vision=True,
            save_conversation_path=f"logs/browser_test_{project_name}"
        )
        
        try:
            # Run the browser testing
            history = await agent.run(max_steps=15)
            
            # Extract results
            final_result = history.final_result()
            screenshots = history.screenshot_paths()
            errors = history.errors()
            
            # Structure the feedback
            feedback = {
                "url": url,
                "project_name": project_name,
                "test_timestamp": datetime.now().isoformat(),
                "screenshots": screenshots,
                "test_results": final_result,
                "errors": [str(e) for e in errors],
                "success": len(errors) == 0,
                "history_summary": {
                    "total_steps": len(history),
                    "urls_visited": history.urls(),
                    "actions_performed": history.action_names()
                }
            }
            
            print(f"✅ Browser testing completed")
            print(f"📸 Screenshots taken: {len(screenshots)}")
            print(f"🔍 Test result: {final_result[:200]}...")
            
            return feedback
            
        except Exception as e:
            print(f"❌ Browser testing failed: {e}")
            return {
                "url": url,
                "project_name": project_name,
                "test_timestamp": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }
    
    async def write_feedback_to_notion(self, feedback: dict) -> bool:
        """Write test feedback to new Notion page"""
        
        try:
            # Import the service class
            from notion_mcp_client import NotionMCPService
            
            # Connect to Notion
            notion_service = NotionMCPService()
            await notion_service.start()
            
            # Create page title with timestamp
            timestamp = feedback.get('test_timestamp', 'unknown')
            project_name = feedback.get('project_name', 'Unknown Project')
            page_title = f"Browser Test: {project_name} - {timestamp[:19]}"
            
            # Format feedback for Notion
            notion_content = self._format_feedback_for_notion(feedback)
            
            # Create new page
            result = await notion_service.create_page(
                title=page_title,
                content=notion_content
            )
            
            if result and not result.get('error'):
                print(f"✅ New Notion page created: {page_title}")
                return True
            else:
                print(f"❌ Failed to create Notion page: {result}")
                return False
            
        except Exception as e:
            print(f"❌ Notion feedback failed: {e}")
            return False
        finally:
            try:
                await notion_service.stop()
            except:
                pass
    
    def _format_feedback_for_notion(self, feedback: dict) -> str:
        """Format feedback data for Notion document"""
        
        timestamp = feedback.get('test_timestamp', datetime.now().isoformat())
        url = feedback.get('url', 'Unknown URL')
        project_name = feedback.get('project_name', 'Unknown Project')
        
        content = f"""
## Browser Test Results - {timestamp}

**Project:** {project_name}
**URL:** {url}
**Status:** {'✅ Success' if feedback.get('success', False) else '❌ Failed'}

### Test Results
{feedback.get('test_results', 'No results available')}

### Screenshots
"""
        
        screenshots = feedback.get('screenshots', [])
        if screenshots:
            content += f"📸 {len(screenshots)} screenshots captured\n"
            for i, screenshot in enumerate(screenshots[:3]):  # Show first 3
                content += f"- Screenshot {i+1}: {screenshot}\n"
        else:
            content += "No screenshots captured\n"
        
        # Add errors if any
        errors = feedback.get('errors', [])
        if errors:
            content += "\n### Errors Found\n"
            for error in errors:
                content += f"- {error}\n"
        
        # Add history summary
        history = feedback.get('history_summary', {})
        if history:
            content += f"""
### Test Summary
- **Total Steps:** {history.get('total_steps', 0)}
- **URLs Visited:** {len(history.get('urls_visited', []))}
- **Actions Performed:** {', '.join(history.get('actions_performed', [])[:5])}

---
"""
        
        return content

# Complete testing workflow
async def test_and_document_deployment(url: str, project_name: str = "pixelpilot-project"):
    """Complete workflow: test deployment and document results"""
    
    print(f"🚀 Starting complete testing workflow for: {url}")
    
    # Create testing agent
    tester = BrowserTestingAgent()
    
    # Test the deployed app
    feedback = await tester.test_deployed_app(url, project_name)
    
    # Write feedback to Notion
    notion_success = await tester.write_feedback_to_notion(feedback)
    
    # Summary
    print("\n" + "="*50)
    print("🎯 TESTING WORKFLOW COMPLETE")
    print("="*50)
    print(f"✅ Browser Testing: {'Success' if feedback.get('success', False) else 'Failed'}")
    print(f"✅ Notion Documentation: {'Success' if notion_success else 'Failed'}")
    
    if feedback.get('screenshots'):
        print(f"📸 Screenshots: {len(feedback['screenshots'])} captured")
    
    return {
        "testing_success": feedback.get('success', False),
        "notion_success": notion_success,
        "feedback": feedback
    }

# Quick test with existing deployment
async def test_existing_deployment():
    """Test the existing PixelPilot deployment"""
    
    # Use the deployment URL from memory
    url = "https://pixelpilot-project-iq4zyr9zy-rajashekarvs-projects.vercel.app"
    
    result = await test_and_document_deployment(url, "pixelpilot-project")
    return result

if __name__ == "__main__":
    print("🎭 Browser Testing Agent")
    print("=" * 40)
    
    # Test existing deployment
    asyncio.run(test_existing_deployment())
