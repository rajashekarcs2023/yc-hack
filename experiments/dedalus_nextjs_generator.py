#!/usr/bin/env python3
"""
Dedalus Next.js Project Generator
================================

Generate complete Next.js TypeScript project using Dedalus agent
when v0 API is unavailable.
"""

import asyncio
import os
import json
from pathlib import Path
from notion_mcp_client import NotionMCPClient
from dedalus_notion_tool import NotionMCPTool

class DedalusNextJSGenerator:
    def __init__(self):
        self.notion_tool = NotionMCPTool()
        self.pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
        
    async def get_pixelpilot_specs(self) -> str:
        """Get PixelPilot specifications from Notion."""
        print("📖 Reading PixelPilot specification from Notion...")
        
        try:
            result = await self.notion_tool.fetch_page(self.pixelpilot_page_id)
            if result and result.get("success"):
                specs = result.get("content", "")
                print("✅ Specifications retrieved successfully")
                return specs
            else:
                print("❌ No specifications found")
                return ""
        except Exception as e:
            print(f"❌ Error retrieving specs: {e}")
            return ""

    def create_nextjs_prompt(self, specs: str) -> str:
        """Create comprehensive Next.js project generation prompt for Dedalus."""
        return f"""
Create a complete Next.js 14 TypeScript project based on these specifications:

{specs}

GENERATE ALL THESE FILES with complete, production-ready code:

1. **package.json** - Include all dependencies:
   - next@14.0.0
   - react@18.0.0
   - typescript@5.0.0
   - tailwindcss@3.0.0
   - @types/node, @types/react
   - All necessary devDependencies

2. **next.config.js** - Next.js configuration

3. **tailwind.config.js** - Tailwind configuration with custom theme

4. **tsconfig.json** - TypeScript configuration

5. **app/layout.tsx** - Root layout with metadata and providers

6. **app/page.tsx** - Home page showcasing the Profile Card

7. **app/globals.css** - Global styles and Tailwind imports

8. **components/ProfileCard.tsx** - Main Profile Card component

9. **components/ui/Button.tsx** - Reusable Button component

10. **components/ui/Avatar.tsx** - Avatar component

11. **lib/utils.ts** - Utility functions (cn function for class merging)

12. **types/index.ts** - TypeScript type definitions

REQUIREMENTS:
- Complete, runnable Next.js 14 project
- TypeScript with strict mode
- Tailwind CSS with custom design system
- Responsive design (mobile-first)
- Dark/light mode support
- Accessibility compliant
- Professional, modern design
- All files must have complete, working code

Generate each file with its full path and complete content. Make this immediately deployable.
"""

    async def generate_with_dedalus(self, prompt: str) -> str:
        """Generate Next.js project using Dedalus."""
        print("🤖 Generating complete Next.js project with Dedalus...")
        
        try:
            # Use Dedalus to generate the complete project
            from dedalus import Dedalus
            
            dedalus = Dedalus(api_key=os.getenv("DEDALUS_API_KEY"))
            
            response = await dedalus.chat(
                message=prompt,
                system_prompt="You are an expert Next.js developer. Generate complete, production-ready code for all requested files. Provide full file contents, not just snippets.",
                model="claude-3-5-sonnet-20241022"
            )
            
            print("✅ Project generated with Dedalus")
            return response
            
        except Exception as e:
            print(f"❌ Error with Dedalus generation: {e}")
            return ""

    def parse_and_save_project(self, dedalus_response: str, project_dir: str = "pixelpilot-nextjs") -> bool:
        """Parse Dedalus response and save project files."""
        print(f"💾 Parsing and saving project to {project_dir}/...")
        
        try:
            # Create project directory
            if os.path.exists(project_dir):
                import shutil
                shutil.rmtree(project_dir)
            os.makedirs(project_dir)
            
            # Parse the response to extract files
            # This is a simple parser - in practice, you'd want more robust parsing
            lines = dedalus_response.split('\n')
            current_file = None
            current_content = []
            files_saved = 0
            
            for line in lines:
                # Look for file headers (e.g., "## package.json" or "**package.json**")
                if (line.startswith('##') or line.startswith('**')) and any(ext in line.lower() for ext in ['.json', '.js', '.ts', '.tsx', '.css']):
                    # Save previous file if exists
                    if current_file and current_content:
                        self.save_file(project_dir, current_file, '\n'.join(current_content))
                        files_saved += 1
                    
                    # Extract filename
                    current_file = self.extract_filename(line)
                    current_content = []
                    
                # Look for code blocks
                elif line.startswith('```') and current_file:
                    # Skip the opening ```
                    continue
                elif current_file and not line.startswith('```'):
                    current_content.append(line)
            
            # Save last file
            if current_file and current_content:
                self.save_file(project_dir, current_file, '\n'.join(current_content))
                files_saved += 1
            
            print(f"✅ Saved {files_saved} files to {project_dir}/")
            
            # Create basic structure if parsing failed
            if files_saved == 0:
                self.create_basic_structure(project_dir, dedalus_response)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving project: {e}")
            return False

    def extract_filename(self, line: str) -> str:
        """Extract filename from header line."""
        # Remove markdown formatting
        line = line.replace('##', '').replace('**', '').strip()
        
        # Common file patterns
        if 'package.json' in line.lower():
            return 'package.json'
        elif 'next.config' in line.lower():
            return 'next.config.js'
        elif 'tailwind.config' in line.lower():
            return 'tailwind.config.js'
        elif 'tsconfig' in line.lower():
            return 'tsconfig.json'
        elif 'layout.tsx' in line.lower():
            return 'app/layout.tsx'
        elif 'page.tsx' in line.lower():
            return 'app/page.tsx'
        elif 'globals.css' in line.lower():
            return 'app/globals.css'
        elif 'ProfileCard' in line:
            return 'components/ProfileCard.tsx'
        elif 'Button' in line:
            return 'components/ui/Button.tsx'
        elif 'Avatar' in line:
            return 'components/ui/Avatar.tsx'
        elif 'utils' in line.lower():
            return 'lib/utils.ts'
        elif 'types' in line.lower():
            return 'types/index.ts'
        else:
            return 'unknown.txt'

    def save_file(self, project_dir: str, filepath: str, content: str):
        """Save individual file with proper directory structure."""
        full_path = os.path.join(project_dir, filepath)
        
        # Create directories if needed
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Save file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        
        print(f"  ✅ {filepath}")

    def create_basic_structure(self, project_dir: str, content: str):
        """Create basic project structure if parsing failed."""
        print("📁 Creating basic project structure...")
        
        # Save the full response as a reference
        with open(os.path.join(project_dir, 'dedalus_response.txt'), 'w') as f:
            f.write(content)
        
        # Create basic package.json
        package_json = {
            "name": "pixelpilot-nextjs",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "14.0.0",
                "react": "^18",
                "react-dom": "^18",
                "tailwindcss": "^3.3.0"
            },
            "devDependencies": {
                "typescript": "^5",
                "@types/node": "^20",
                "@types/react": "^18",
                "@types/react-dom": "^18",
                "autoprefixer": "^10.0.1",
                "postcss": "^8",
                "eslint": "^8",
                "eslint-config-next": "14.0.0"
            }
        }
        
        with open(os.path.join(project_dir, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)
        
        print("  ✅ package.json")
        print("  ✅ dedalus_response.txt (full response for manual extraction)")

async def main():
    """Test Dedalus Next.js project generation."""
    print("🎯 Testing Dedalus Next.js Project Generation")
    print("=" * 50)
    
    generator = DedalusNextJSGenerator()
    
    # Get specs
    specs = await generator.get_pixelpilot_specs()
    if not specs:
        print("❌ Could not retrieve specifications")
        return
    
    # Create prompt
    prompt = generator.create_nextjs_prompt(specs)
    
    # Generate with Dedalus
    response = await generator.generate_with_dedalus(prompt)
    if not response:
        print("❌ Could not generate project with Dedalus")
        return
    
    # Parse and save
    success = generator.parse_and_save_project(response)
    
    if success:
        print("\n🎉 Next.js project generated!")
        print("📋 Next steps:")
        print("  1. cd pixelpilot-nextjs")
        print("  2. npm install")
        print("  3. npm run dev")
    else:
        print("❌ Failed to save project")

if __name__ == "__main__":
    asyncio.run(main())
