#!/usr/bin/env python3
"""
Test Next.js Project Generation with v0
=======================================

Simple test to generate a complete Next.js TypeScript project using v0 API
without the MCP client complexity.
"""

import asyncio
import aiohttp
import os
import json
import shutil
from pathlib import Path

class NextJSProjectGenerator:
    def __init__(self):
        self.v0_api_key = os.getenv("V0_API_KEY")
        
    def get_nextjs_prompt(self) -> str:
        """Create a comprehensive Next.js project generation prompt."""
        return """
Create a complete Next.js 14 TypeScript project for a Profile Card component with the following specifications:

COMPONENT REQUIREMENTS:
- Profile Card with avatar, name, title, bio, and social links
- Responsive design (mobile-first)
- Dark/light mode support
- Tailwind CSS styling
- TypeScript with proper types
- Accessibility compliant (WCAG 2.1 AA)

PROJECT STRUCTURE NEEDED:
1. **package.json** - Complete with all dependencies (Next.js 14, TypeScript, Tailwind CSS, etc.)
2. **next.config.js** - Next.js configuration
3. **tailwind.config.js** - Tailwind configuration with custom theme
4. **tsconfig.json** - TypeScript configuration
5. **app/layout.tsx** - Root layout with metadata and providers
6. **app/page.tsx** - Home page showcasing the Profile Card
7. **app/globals.css** - Global styles and Tailwind imports
8. **components/ProfileCard.tsx** - Main Profile Card component
9. **components/ui/** - Reusable UI components (Button, Avatar, etc.)
10. **lib/utils.ts** - Utility functions
11. **types/index.ts** - TypeScript type definitions

TECHNICAL REQUIREMENTS:
- Next.js 14 with App Router
- TypeScript strict mode
- Tailwind CSS with custom design tokens
- Responsive breakpoints (sm, md, lg, xl)
- Dark mode using next-themes
- Proper SEO metadata
- Performance optimized
- Production ready

DESIGN SPECIFICATIONS:
- Clean, modern design
- Subtle shadows and rounded corners
- Smooth hover animations
- Professional color palette
- Proper spacing and typography
- Mobile-responsive layout

Please generate ALL necessary files for a complete, deployable Next.js project that I can immediately run with `npm install && npm run dev`.
"""

    async def generate_nextjs_project(self) -> dict:
        """Generate complete Next.js project using v0 API."""
        print("🚀 Generating complete Next.js TypeScript project...")
        
        headers = {
            "Authorization": f"Bearer {self.v0_api_key}",
            "Content-Type": "application/json"
        }
        
        chat_data = {
            "message": self.get_nextjs_prompt(),
            "system": "You are an expert Next.js developer. Create a complete, production-ready Next.js 14 TypeScript project with proper file structure, configuration, and all necessary files for immediate deployment. Include package.json with all dependencies.",
            "chatPrivacy": "private"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Create chat
                print("📝 Creating v0 chat for project generation...")
                async with session.post(
                    "https://api.v0.dev/v1/chats",
                    headers=headers,
                    json=chat_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        chat_id = result.get("id")
                        demo_url = result.get("demo")
                        chat_url = result.get("url")
                        
                        print(f"✅ Chat created: {chat_url}")
                        print(f"📱 Demo URL: {demo_url}")
                        print(f"🔄 Waiting for generation to complete...")
                        
                        # Wait for generation
                        await asyncio.sleep(10)
                        
                        # Get files
                        files = await self.get_project_files(chat_id)
                        
                        return {
                            "success": True,
                            "chat_id": chat_id,
                            "demo_url": demo_url,
                            "chat_url": chat_url,
                            "files": files
                        }
                    else:
                        error_text = await response.text()
                        print(f"❌ Failed to create chat: {response.status} - {error_text}")
                        return {"success": False, "error": error_text}
                        
        except Exception as e:
            print(f"❌ Error generating project: {e}")
            return {"success": False, "error": str(e)}

    async def get_project_files(self, chat_id: str) -> list:
        """Retrieve project files from v0 chat."""
        print("📁 Retrieving project files...")
        
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
                        data = await response.json()
                        files = data.get("files", [])
                        
                        print(f"✅ Found {len(files)} files")
                        for i, file in enumerate(files):
                            name = file.get("name", f"file_{i}")
                            content_length = len(str(file.get("content", "")))
                            print(f"  📄 {name} ({content_length} chars)")
                        
                        return files
                    else:
                        print(f"❌ Failed to get files: {response.status}")
                        return []
                        
        except Exception as e:
            print(f"❌ Error retrieving files: {e}")
            return []

    def save_project(self, files: list, project_dir: str = "pixelpilot-nextjs") -> bool:
        """Save project files to directory."""
        print(f"💾 Saving project to {project_dir}/...")
        
        try:
            # Clean directory
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
            os.makedirs(project_dir)
            
            saved_files = []
            
            for i, file in enumerate(files):
                # Get file info
                name = file.get("name") or file.get("path") or f"file_{i}.txt"
                content = file.get("content", "")
                
                # Clean filename
                if "/" in name:
                    # Create subdirectories
                    full_path = os.path.join(project_dir, name)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                else:
                    full_path = os.path.join(project_dir, name)
                
                # Save file
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(str(content))
                
                saved_files.append(name)
                print(f"  ✅ {name}")
            
            print(f"\n📁 Project saved with {len(saved_files)} files")
            print(f"📂 Directory: {os.path.abspath(project_dir)}")
            
            # Show project structure
            self.show_project_structure(project_dir)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving project: {e}")
            return False

    def show_project_structure(self, project_dir: str):
        """Display the project structure."""
        print(f"\n📋 Project Structure:")
        print("=" * 40)
        
        for root, dirs, files in os.walk(project_dir):
            level = root.replace(project_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                print(f"{subindent}{file} ({size} bytes)")

async def main():
    """Test Next.js project generation."""
    print("🎯 Testing Next.js TypeScript Project Generation")
    print("=" * 50)
    
    generator = NextJSProjectGenerator()
    
    # Generate project
    result = await generator.generate_nextjs_project()
    
    if result["success"]:
        print(f"\n✅ Generation successful!")
        print(f"📱 Demo: {result['demo_url']}")
        print(f"🔗 Chat: {result['chat_url']}")
        
        # Save project
        if result["files"]:
            saved = generator.save_project(result["files"])
            if saved:
                print("\n🎉 Complete Next.js project ready!")
                print("📋 Next steps:")
                print("  1. cd pixelpilot-nextjs")
                print("  2. npm install")
                print("  3. npm run dev")
            else:
                print("❌ Failed to save project files")
        else:
            print("⚠️ No files generated - check v0 response")
    else:
        print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())
