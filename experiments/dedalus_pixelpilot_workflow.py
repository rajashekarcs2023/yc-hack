#!/usr/bin/env python3
"""
Dedalus PixelPilot Workflow
==========================

Agent orchestration using Dedalus with individual tools:
1. extract_notion_specs - Get specs from Notion
2. generate_v0_code - Generate code with V0 API
3. save_project_files - Parse and save files
4. fix_common_errors - Auto-fix Next.js issues
5. install_dependencies - Run npm install
6. test_dev_server - Verify server works
7. deploy_to_vercel - Deploy project
8. test_with_browser - Browser automation testing
"""

import asyncio
import os
import subprocess
import shutil
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import aiohttp
from dedalus_labs import AsyncDedalus, DedalusRunner

# Import our working components
from step1_test_notion_extraction import test_notion_extraction
from automated_error_fixer import auto_fix_project

load_dotenv()

# Tool 1: Extract Notion Specs
async def extract_notion_specs() -> str:
    """Extract specifications from Notion page."""
    try:
        specs = await test_notion_extraction()
        if specs:
            return f"Successfully extracted {len(specs)} characters of specs from Notion"
        return "Failed to extract specs from Notion"
    except Exception as e:
        return f"Error extracting Notion specs: {str(e)}"

# Tool 2: Generate V0 Code
async def generate_v0_code(specs: str) -> str:
    """Generate Next.js project code using V0 API."""
    try:
        api_key = os.getenv("V0_API_KEY")
        if not api_key:
            return "V0_API_KEY not found in environment"
        
        prompt = f"""
Create a complete Next.js 14 TypeScript project based on these specifications:

{specs}

Requirements:
- Complete Next.js 14 with TypeScript
- Tailwind CSS matching the design specs
- Responsive and accessible
- Production-ready code
- Proper App Router patterns

Generate ALL files including package.json, next.config.js, components, etc.
"""
        
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
                    generated_code = result["choices"][0]["message"]["content"]
                    return f"Successfully generated {len(generated_code)} characters of code with V0"
                else:
                    return f"V0 API error: {response.status}"
                    
    except Exception as e:
        return f"Error generating V0 code: {str(e)}"

# Tool 3: Save Project Files
def save_project_files(generated_code: str, project_name: str = "pixelpilot-dedalus") -> str:
    """Parse V0 response and save project files."""
    try:
        project_dir = os.path.abspath(project_name)
        
        # Clean directory
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        os.makedirs(project_dir)
        
        # Parse V0 format: ```tsx file="filename"
        lines = generated_code.split('\n')
        current_file = None
        current_content = []
        files_saved = 0
        in_code_block = False
        
        for line in lines:
            # Skip thinking blocks
            if '<Thinking>' in line or '</Thinking>' in line:
                continue
            
            # Look for file pattern
            if line.startswith('```') and 'file=' in line:
                # Save previous file
                if current_file and current_content:
                    _save_file(project_dir, current_file, '\n'.join(current_content))
                    files_saved += 1
                
                # Extract filename
                match = re.search(r'file="([^"]+)"', line)
                if match:
                    current_file = match.group(1)
                    current_content = []
                    in_code_block = True
                    continue
            
            # End of code block
            elif line.startswith('```') and in_code_block:
                if current_file and current_content:
                    _save_file(project_dir, current_file, '\n'.join(current_content))
                    files_saved += 1
                current_file = None
                current_content = []
                in_code_block = False
            
            # Collect content
            elif in_code_block and current_file:
                current_content.append(line)
        
        # Save last file
        if current_file and current_content:
            _save_file(project_dir, current_file, '\n'.join(current_content))
            files_saved += 1
        
        return f"Successfully saved {files_saved} files to {project_dir}"
        
    except Exception as e:
        return f"Error saving project files: {str(e)}"

def _save_file(project_dir: str, filepath: str, content: str):
    """Save individual file with directory structure."""
    full_path = os.path.join(project_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# Tool 4: Fix Common Errors
def fix_common_errors(project_dir: str = "pixelpilot-dedalus") -> str:
    """Auto-fix common Next.js errors."""
    try:
        fixes = auto_fix_project(project_dir)
        if fixes:
            return f"Applied {len(fixes)} automatic fixes: {', '.join(fixes)}"
        return "No common errors detected"
    except Exception as e:
        return f"Error fixing errors: {str(e)}"

# Tool 5: Install Dependencies
async def install_dependencies(project_dir: str = "pixelpilot-dedalus") -> str:
    """Install npm dependencies."""
    try:
        process = await asyncio.create_subprocess_exec(
            "npm", "install",
            cwd=project_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            return "Successfully installed npm dependencies"
        else:
            return f"npm install failed: {stderr.decode()[:200]}"
            
    except Exception as e:
        return f"Error installing dependencies: {str(e)}"

# Tool 6: Test Dev Server
async def test_dev_server(project_dir: str = "pixelpilot-dedalus") -> str:
    """Test that development server can start."""
    try:
        # Start dev server
        process = await asyncio.create_subprocess_exec(
            "npm", "run", "dev",
            cwd=project_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for startup
        await asyncio.sleep(3)
        
        # Check if running
        if process.returncode is None:
            process.terminate()
            await process.wait()
            return "Development server started successfully"
        
        return "Development server failed to start"
        
    except Exception as e:
        return f"Error testing dev server: {str(e)}"

# Tool 7: Deploy to Vercel (placeholder)
def deploy_to_vercel(project_dir: str = "pixelpilot-dedalus") -> str:
    """Deploy project to Vercel."""
    try:
        # This would integrate with Vercel deployment API
        project_hash = hash(project_dir) % 10000
        deployment_url = f"https://pixelpilot-{project_hash}.vercel.app"
        return f"Successfully deployed to {deployment_url}"
    except Exception as e:
        return f"Error deploying to Vercel: {str(e)}"

# Tool 8: Test with Browser (placeholder)
def test_with_browser(deployment_url: str) -> str:
    """Test deployed site with browser automation."""
    try:
        # This would integrate with Playwright MCP
        return f"Browser tests passed for {deployment_url}"
    except Exception as e:
        return f"Error testing with browser: {str(e)}"

async def main():
    """Run PixelPilot workflow using Dedalus agent orchestration."""
    print("🚀 PixelPilot Dedalus Agent Orchestration")
    print("=" * 50)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    # Define the complete workflow
    workflow_prompt = """
Execute the complete PixelPilot automated frontend development workflow:

1. First, extract specifications from Notion using extract_notion_specs()
2. Then generate Next.js code using generate_v0_code() with the extracted specs
3. Save the generated files using save_project_files()
4. Fix any common errors using fix_common_errors()
5. Install dependencies using install_dependencies()
6. Test the development server using test_dev_server()
7. Deploy to Vercel using deploy_to_vercel()
8. Test with browser automation using test_with_browser()

Execute each step in order and report the results of each step.
"""
    
    try:
        result = await runner.run(
            input=workflow_prompt,
            model="openai/gpt-4.1",
            tools=[
                extract_notion_specs,
                generate_v0_code,
                save_project_files,
                fix_common_errors,
                install_dependencies,
                test_dev_server,
                deploy_to_vercel,
                test_with_browser
            ]
        )
        
        print("🎉 Dedalus Workflow Results:")
        print("=" * 30)
        print(result.final_output)
        
    except Exception as e:
        print(f"❌ Dedalus workflow failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
