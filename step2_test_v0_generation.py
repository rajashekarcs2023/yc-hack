#!/usr/bin/env python3
"""
Step 2B: Test V0 Code Generation
===============================

Test generating Next.js project using V0 API directly from Python.
"""

import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Minimal specs for fast testing
PROFILE_CARD_SPECS = """
Create a simple Next.js component called ProfileCard with:
- A card with white background
- User name "John Doe" 
- A blue "Like" button
- Include package.json file
"""

async def test_v0_code_generation():
    """Test generating Next.js project with V0 API directly with retry logic."""
    print("🚀 Step 2B: Testing Code Generation with V0")
    print("=" * 50)
    
    print(f"📋 Using pre-extracted specs ({len(PROFILE_CARD_SPECS)} chars)")
    
    # Retry logic for V0 API
    max_retries = 3
    for attempt in range(max_retries):
        if attempt > 0:
            print(f"🔄 Retry attempt {attempt + 1}/{max_retries}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
        # Create V0 generation prompt
        prompt = f"""
Create a complete Next.js 14 TypeScript project based on these specifications:

{PROFILE_CARD_SPECS}

Requirements:
- Complete, production-ready Next.js 14 project with TypeScript
- Tailwind CSS with custom design system matching the specs exactly
- Responsive design (mobile-first)
- Accessibility compliant (WCAG 2.1 AA)
- Professional, modern design
- All components should be properly structured for Next.js App Router
- Include proper error handling and loading states
- Make it immediately deployable to Vercel

Generate ALL necessary files including:
1. package.json with all dependencies
2. next.config.js
3. tailwind.config.js  
4. tsconfig.json
5. app/layout.tsx
6. app/page.tsx
7. app/globals.css
8. components/ProfileCard.tsx
9. components/ui/Button.tsx
10. components/ui/Avatar.tsx
11. lib/utils.ts
12. types/index.ts

Ensure proper Next.js 13+ App Router patterns with correct Server/Client Component usage.
"""

    try:
        print("🧠 Generating code with V0...")
        
        # Use V0 API directly
        api_key = os.getenv("V0_API_KEY")
        if not api_key:
            print("❌ V0_API_KEY not found in environment")
            return None
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "v0-1.5-md",
            "messages": [
                {
                    "role": "user",
                    "content": f"Create a complete Next.js project with the following specifications:\n\n{prompt}\n\nGenerate all necessary files including package.json, components, pages, and configuration files."
                }
            ],
            "max_completion_tokens": 8000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.v0.dev/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        generated_code = response_data['choices'][0]['message']['content']
                        print("✅ Code generated successfully with V0!")
                        print(f"📄 Generated content length: {len(generated_code)} characters")
                        print("\n📋 First 1000 characters:")
                        print("-" * 30)
                        print(generated_code[:1000] + "..." if len(generated_code) > 1000 else generated_code)
                        print("-" * 30)
                        
                        # Debug: Look for file patterns
                        print("\n🔍 Looking for file patterns...")
                        lines = generated_code.split('\n')
                        for i, line in enumerate(lines[:100]):
                            if any(keyword in line.lower() for keyword in ['package.json', 'tsx', 'jsx', 'css', 'config', 'file']):
                                print(f"Line {i}: {line[:100]}")
                        
                        return generated_code
                    else:
                        print("❌ No content in V0 response")
                        return None
                else:
                    error_text = await response.text()
                    print(f"❌ V0 API error: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        print(f"❌ Error generating code with V0: {e}")
        return None

def save_generated_project(generated_code: str, project_dir: str = None) -> bool:
    """Universal V0 parser that handles all format variations."""
    if not project_dir:
        project_dir = os.environ.get('PIXELPILOT_PROJECT_NAME', 'pixelpilot-v0')
    
    print(f"💾 Saving V0 generated project to {project_dir}/...")
    
    try:
        import os
        import shutil
        import re
        
        # Clean directory
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        os.makedirs(project_dir)
        
        files_saved = 0
        
        # Universal V0 parser - handles multiple formats
        # Format 1: ```json file="package.json" (current V0 format)
        pattern1 = r'```(\w+)\s+file="([^"]+)"\s*\n(.*?)```'
        matches1 = re.findall(pattern1, generated_code, re.DOTALL)
        
        for lang, filename, content in matches1:
            save_file(project_dir, filename, content.strip())
            files_saved += 1
            print(f"  ✓ {filename} ({lang})")
        
        # Format 2: <File path="filename"> ... </File> (capital F)
        pattern2 = r'<[Ff]ile path="([^"]+)">\s*\n(.*?)</[Ff]ile>'
        matches2 = re.findall(pattern2, generated_code, re.DOTALL)
        
        for filename, content in matches2:
            save_file(project_dir, filename, content.strip())
            files_saved += 1
            print(f"  ✓ {filename}")
        
        # Format 3: ## filename followed by code block
        pattern3 = r'## ([^\n]+\.(json|js|tsx|ts|css|md))\s*\n```[^\n]*\n(.*?)```'
        matches3 = re.findall(pattern3, generated_code, re.DOTALL)
        
        for filename, ext, content in matches3:
            save_file(project_dir, filename, content.strip())
            files_saved += 1
            print(f"  ✓ {filename}")
        
        # Format 4: ```tsx file="filename" (alternative spacing)
        pattern4 = r'```\w+\s*file="([^"]+)"\s*\n(.*?)```'
        matches4 = re.findall(pattern4, generated_code, re.DOTALL)
        
        for filename, content in matches4:
            if filename not in [m[1] for m in matches1]:  # Avoid duplicates
                save_file(project_dir, filename, content.strip())
                files_saved += 1
                print(f"  ✓ {filename}")
        
        print(f"✅ Saved {files_saved} files to {project_dir}/")
        
        # Show project structure
        show_project_structure(project_dir)
        
        return files_saved > 0
        
    except Exception as e:
        print(f"❌ Error saving V0 project: {e}")
        return False

def save_file(project_dir: str, filepath: str, content: str):
    """Save individual file with directory structure."""
    full_path = os.path.join(project_dir, filepath)
    
    # Create directories if needed
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Save file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"  ✅ {filepath}")

def show_project_structure(project_dir: str):
    """Display the project structure."""
    print(f"\n📋 V0 Project Structure:")
    print("=" * 30)
    
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
    """Test V0 code generation workflow."""
    generated_code = await test_v0_code_generation()
    
    if generated_code:
        generated_code = await generate_v0_code(prompt)
        
        if generated_code:
            # Save to project directory
            success = save_generated_project(generated_code)
            
            if success:
                print("🎉 Step 2B Complete: V0 Next.js project generated!")
                print(f"📁 Project saved to: {os.environ.get('PIXELPILOT_PROJECT_NAME', 'pixelpilot-v0')}")
                print("📋 Next steps:")
                print("  1. cd pixelpilot-v0")
                print("  2. npm install")
                print("  3. npm run dev")
                return  # Success, exit retry loop
            else:
                print("❌ Step 2B Failed: Could not save V0 project files")
                if attempt == max_retries - 1:
                    return
        else:
            print(f"❌ V0 API failed on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                print("❌ Step 2B Failed: Could not generate code with V0 after retries")

if __name__ == "__main__":
    asyncio.run(main())
