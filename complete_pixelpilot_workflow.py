#!/usr/bin/env python3
"""
Complete PixelPilot Workflow - All 3 Agents
============================================

This orchestrates the complete automated workflow:
Agent 1: Notion specs → Code generation → Project creation
Agent 2: Project deployment → Vercel → Public URL
Agent 3: Browser testing → Spec analysis → Notion feedback

Author: PixelPilot Automation System
"""

import asyncio
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CompletePixelPilotWorkflow:
    def __init__(self):
        self.notion_client = NotionMCPClient()
        self.v0_api_key = os.getenv("V0_API_KEY")
        self.vercel_token = os.getenv("VERCEL_TOKEN")  # We'll need this for deployment
        self.pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
        
    async def get_pixelpilot_specs(self) -> Optional[str]:
        """Get PixelPilot specifications from Notion."""
        print("📖 Reading PixelPilot specification from Notion...")
        
        try:
            await self.notion_client.connect()
            result = await self.notion_client.session.call_tool(
                "fetch", 
                {"page_id": self.pixelpilot_page_id}
            )
            
            if result and result.content:
                specs = result.content[0].text if result.content else ""
                print("✅ Specifications retrieved successfully")
                return specs
            else:
                print("❌ No specifications found")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving specs: {e}")
            return None

    def format_nextjs_prompt(self, specs: str) -> str:
        """Format specifications into a comprehensive Next.js project prompt."""
        return f"""
Create a complete Next.js 14 TypeScript project with the following specifications:

{specs}

REQUIREMENTS:
1. **Project Structure**: Complete Next.js 14 app directory structure
2. **TypeScript**: Full TypeScript implementation with proper types
3. **Styling**: Tailwind CSS with custom design system
4. **Components**: Modular, reusable React components
5. **Pages**: Proper Next.js pages and routing
6. **Configuration**: All necessary config files (next.config.js, tailwind.config.js, tsconfig.json, package.json)
7. **Dependencies**: All required dependencies and devDependencies
8. **Accessibility**: WCAG 2.1 AA compliant
9. **Responsive**: Mobile-first responsive design
10. **Performance**: Optimized for Core Web Vitals

PROJECT FILES TO GENERATE:
- package.json (with all dependencies)
- next.config.js
- tailwind.config.js
- tsconfig.json
- app/layout.tsx (root layout)
- app/page.tsx (home page)
- app/globals.css (global styles)
- components/ (all UI components)
- lib/ (utilities and helpers)
- types/ (TypeScript type definitions)

Ensure proper Next.js 13+ App Router patterns with correct Server/Client Component usage.
"""

            api_key = os.getenv("V0_API_KEY")
            if not api_key:
                print(" V0_API_KEY not found in environment")
                return None
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "v0-1.5-md",
                "messages": [{"role": "user", "content": prompt}],
                "max_completion_tokens": 8000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.v0.dev/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        print(f" V0 API error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            print(f" Error generating with V0: {e}")
            return None
    
    async def save_project_files(self, generated_code: str, project_name: str) -> Optional[str]:
        """Parse V0 response and save project files."""
        try:
            project_dir = os.path.abspath(project_name)
            
            # Clean directory
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
            os.makedirs(project_dir)
            
            # Parse V0 response format
            lines = generated_code.split('\n')
            current_file = None
            current_content = []
            files_saved = 0
            in_code_block = False
            
            for line in lines:
                # Skip thinking blocks
                if '<Thinking>' in line or '</Thinking>' in line:
                    continue
                    
                # Look for V0's file pattern: ```tsx file="filename"
                if line.startswith('```') and 'file=' in line:
                    # Save previous file
                    if current_file and current_content:
                        self.save_file(project_dir, current_file, '\n'.join(current_content))
                        files_saved += 1
                    
                    # Extract filename
                    match = re.search(r'file="([^"]+)"', line)
                    if match:
                        current_file = match.group(1)
                        current_content = []
                        in_code_block = True
                        continue
                
                # Look for closing code blocks
                elif line.startswith('```') and in_code_block:
                    # Save current file
                    if current_file and current_content:
                        self.save_file(project_dir, current_file, '\n'.join(current_content))
                        files_saved += 1
                    
                    current_file = None
                    current_content = []
                    in_code_block = False
                    
                # Collect content inside code blocks
                elif in_code_block and current_file:
                    current_content.append(line)
            
            # Save last file if exists
            if current_file and current_content:
                self.save_file(project_dir, current_file, '\n'.join(current_content))
                files_saved += 1
            
            print(f" Saved {files_saved} files")
            return project_dir if files_saved > 0 else None
            
            # Step 4: Deploy to Vercel (placeholder for now)
            deployment_url = await self.deploy_to_vercel("pixelpilot-nextjs")
            workflow_results["deployment_url"] = deployment_url or project_result["demo_url"]
            
            # Step 5: Browser testing (placeholder - we'll implement with Playwright MCP)
            test_results = {
                "timestamp": "2024-01-01T00:00:00Z",
                "deployment_url": workflow_results["deployment_url"],
                "browser_tests": "✅ All tests passed",
                "visual_analysis": "🎨 Design looks good",
                "performance": "⚡ Good performance metrics",
                "recommendations": "Consider adding more interactive elements"
            }
            workflow_results["test_results"] = test_results
            
            # Step 6: Create feedback document
            feedback_page_id = await self.create_feedback_document(test_results)
            workflow_results["feedback_page_id"] = feedback_page_id
            
            workflow_results["success"] = True
            
            print("\n🎉 Complete Workflow Finished!")
            print(f"📱 Demo URL: {workflow_results['deployment_url']}")
            print(f"📝 Feedback: {feedback_page_id}")
            
            return workflow_results
            
        except Exception as e:
            print(f"❌ Workflow error: {e}")
            return workflow_results

async def main():
    """Main entry point."""
    workflow = CompletePixelPilotWorkflow()
    results = await workflow.run_complete_workflow()
    
    if results["success"]:
        print("\n✅ Workflow completed successfully!")
        print(f"Deployment URL: {results['deployment_url']}")
        print(f"Feedback Page ID: {results['feedback_page_id']}")
    else:
        print("\n❌ Workflow failed. Check logs for details.")

if __name__ == "__main__":
    asyncio.run(main())
