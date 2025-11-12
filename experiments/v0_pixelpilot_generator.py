#!/usr/bin/env python3
"""
PixelPilot v0 Generator - Uses Vercel v0 SDK to generate frontend from Notion specs
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from mcp_client import MCPClient

load_dotenv()

class V0PixelPilotGenerator:
    def __init__(self):
        self.pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
        self.v0_api_key = os.getenv("V0_API_KEY")
        
        if not self.v0_api_key:
            raise ValueError("V0_API_KEY environment variable is required. Get it from https://v0.dev/chat/settings/keys")
    
    async def get_pixelpilot_specs(self):
        """Retrieve PixelPilot specifications from Notion."""
        print("📖 Reading PixelPilot specification from Notion...")
        
        client = MCPClient()
        try:
            await client.connect_to_hosted_server()
            
            # Fetch the page content
            page_result = await client.call_tool("fetch", {
                "id": self.pixelpilot_page_id
            })
            
            # Extract the text content from the response
            if hasattr(page_result, 'content') and page_result.content:
                content = page_result.content[0].text if isinstance(page_result.content, list) else page_result.content
                
                # Parse JSON to get the actual text
                if isinstance(content, str) and content.startswith('{"'):
                    parsed = json.loads(content)
                    specs_text = parsed.get('text', '')
                    return specs_text
                else:
                    return str(content)
            
            return None
            
        except Exception as e:
            print(f"❌ Failed to retrieve specs: {e}")
            return None
        finally:
            await client.cleanup()
    
    def format_specs_for_v0(self, specs_text):
        """Format the Notion specs into a clear prompt for v0."""
        
        # Extract key information from the specs
        prompt = f"""
Create a React component based on this specification:

{specs_text}

Requirements:
- Build a ProfileCard component in React with TypeScript
- Use Tailwind CSS for styling with the exact design tokens specified
- Implement responsive behavior (horizontal ≥500px, vertical <500px)
- Add interactive like button with counter functionality
- Include proper accessibility (keyboard navigation, focus states)
- Use modern React hooks for state management
- Make the component reusable and well-documented
- Include a demo page showing the component in action

The component should be production-ready and follow React best practices.
"""
        
        return prompt.strip()
    
    async def create_v0_project(self):
        """Create a v0 project for PixelPilot."""
        print("🚀 Creating v0 project...")
        
        # This would be the Node.js equivalent, but we need to implement HTTP calls in Python
        # For now, let's create the structure for the API calls we need to make
        
        project_data = {
            "name": "PixelPilot Profile Card",
            "description": "AI-generated Profile Card component from Notion specifications",
            "environmentVariables": []
        }
        
        return project_data
    
    async def generate_with_v0(self, formatted_prompt):
        """Generate frontend code using v0 API."""
        print("⚙️ Generating frontend with v0...")
        
        # Since we're in Python, we need to make HTTP requests to v0 API
        # The v0-sdk is TypeScript/JavaScript, so we'll implement the HTTP calls directly
        
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.v0_api_key}",
            "Content-Type": "application/json"
        }
        
        # Create chat with v0
        chat_data = {
            "message": formatted_prompt,
            "system": "You are an expert React developer specializing in component design and Tailwind CSS. Create production-ready, accessible components.",
            "chatPrivacy": "private"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create chat
                async with session.post(
                    "https://api.v0.dev/v1/chats",
                    headers=headers,
                    json=chat_data
                ) as response:
                    if response.status == 200:
                        chat_result = await response.json()
                        print(f"✅ Chat created: {chat_result.get('url', 'N/A')}")
                        print(f"📱 Demo URL: {chat_result.get('demo', 'N/A')}")
                        
                        return {
                            "chat_id": chat_result.get("id"),
                            "chat_url": chat_result.get("url"),
                            "demo_url": chat_result.get("demo"),
                            "files": chat_result.get("files", [])
                        }
                    else:
                        error_text = await response.text()
                        print(f"❌ Failed to create chat: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            print(f"❌ Error calling v0 API: {e}")
            return None
    
    async def get_generated_files(self, chat_id):
        """Retrieve generated files from v0 chat."""
        print("📁 Retrieving generated files...")
        
        import aiohttp
        
        headers = {
            "Authorization": f"Bearer {self.v0_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.v0.dev/v1/chats/{chat_id}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        chat_data = await response.json()
                        print(f"🔍 Full API response keys: {list(chat_data.keys())}")
                        
                        # Try different possible file locations in response
                        files = []
                        if "files" in chat_data:
                            files = chat_data["files"]
                        elif "data" in chat_data and "files" in chat_data["data"]:
                            files = chat_data["data"]["files"]
                        elif "result" in chat_data and "files" in chat_data["result"]:
                            files = chat_data["result"]["files"]
                        
                        print(f"✅ Retrieved {len(files)} files")
                        for file in files:
                            print(f"  📄 {file.get('name', file.get('filename', 'Unknown'))}")
                            print(f"    📝 Content length: {len(str(file.get('content', file.get('code', ''))))}")
                        
                        return files
                    else:
                        error_text = await response.text()
                        print(f"❌ Failed to get files: {response.status} - {error_text}")
                        return []
                        
        except Exception as e:
            print(f"❌ Error retrieving files: {e}")
            return []
    
    async def save_generated_files(self, files, output_dir="pixelpilot-frontend"):
        # Save files locally
        if files:
            print("💾 Saving files to pixelpilot-frontend/...")
            os.makedirs("pixelpilot-frontend", exist_ok=True)
            
            for file in files:
                # Try different possible field names for filename and content
                filename = file.get("name") or file.get("filename") or file.get("path") or "unknown.txt"
                content = file.get("content") or file.get("code") or file.get("source") or ""
                
                # Clean filename if it has path separators
                if "/" in filename:
                    filename = filename.split("/")[-1]
                
                filepath = os.path.join("pixelpilot-frontend", filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(str(content))
                print(f"  ✅ Saved {filename} ({len(str(content))} chars)")
            
            print("📁 All files saved to pixelpilot-frontend/")
    
    async def run_complete_workflow(self):
        """Run the complete PixelPilot generation workflow."""
        print("🎯 Starting PixelPilot v0 Generation Workflow")
        print("=" * 60)
        
        # Step 1: Get specs from Notion
        specs = await self.get_pixelpilot_specs()
        if not specs:
            print("❌ Failed to retrieve specifications")
            return None
        
        print("✅ Specifications retrieved successfully")
        
        # Step 2: Format for v0
        formatted_prompt = self.format_specs_for_v0(specs)
        print("✅ Prompt formatted for v0")
        
        # Step 3: Generate with v0
        result = await self.generate_with_v0(formatted_prompt)
        if not result:
            print("❌ Failed to generate with v0")
            return None
        
        # Step 4: Get generated files
        if result.get("chat_id"):
            files = await self.get_generated_files(result["chat_id"])
            
            # Step 5: Save files locally
            if files:
                await self.save_generated_files(files)
        
        print("\n🎉 PixelPilot Generation Complete!")
        print(f"📱 Demo URL: {result.get('demo_url', 'N/A')}")
        print(f"🔗 Chat URL: {result.get('chat_url', 'N/A')}")
        
        return result

async def main():
    """Main function to run the PixelPilot generator."""
    try:
        generator = V0PixelPilotGenerator()
        result = await generator.run_complete_workflow()
        
        if result and result.get("demo_url"):
            print(f"\n🚀 Ready for browser testing: {result['demo_url']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have V0_API_KEY set in your .env file")
        print("   Get your API key from: https://v0.dev/chat/settings/keys")

if __name__ == "__main__":
    asyncio.run(main())
