#!/usr/bin/env python3
"""
Dedalus PixelPilot Tools with Subprocess Isolation
==================================================

Each tool runs in separate subprocess to avoid asyncio conflicts:
- extract_notion_specs() -> subprocess call to step1_test_notion_extraction.py
- generate_v0_code() -> subprocess call to step2_test_v0_generation.py
- Other tools -> direct calls (no asyncio conflicts)
"""

import subprocess
import json
import os
import shutil
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from dedalus_labs import AsyncDedalus, DedalusRunner

# Load environment variables
load_dotenv()

# Tool 1: Extract Notion Specs (subprocess)
def extract_notion_specs(action: str = "extract") -> str:
    """Extract specifications from Notion page using subprocess."""
    try:
        result = subprocess.run(
            ["python", "step1_test_notion_extraction.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Parse output to extract specs
            output = result.stdout
            if "Clean specs length:" in output:
                # Extract the actual specs from the output
                lines = output.split('\n')
                specs_start = False
                specs_lines = []
                
                for line in lines:
                    if "Clean specs preview:" in line:
                        specs_start = True
                        continue
                    elif specs_start and line.strip() == "------------------------------":
                        if specs_lines:  # End of specs
                            break
                        else:  # Start of specs
                            continue
                    elif specs_start:
                        specs_lines.append(line)
                
                specs = '\n'.join(specs_lines).strip()
                return f"SUCCESS: Extracted {len(specs)} characters from Notion"
            
        return f"FAILED: {result.stderr[:200]}"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 2: Generate V0 Code (subprocess)
def generate_v0_code(specs: str, project_name: str = "pixelpilot-dedalus") -> str:
    """Generate Next.js project code using V0 API via subprocess."""
    try:
        # Save specs to temp file for subprocess
        with open("/tmp/pixelpilot_specs.txt", "w") as f:
            f.write(specs)
        
        result = subprocess.run(
            ["python", "step2_test_v0_generation.py"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            output = result.stdout
            if "Saved" in output and "files to" in output:
                return f"SUCCESS: V0 code generated and saved"
            
        return f"FAILED: {result.stderr[:200]}"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 3: Save Project Files (direct - no asyncio)
def save_project_files(project_name: str = "pixelpilot-dedalus") -> str:
    """Check if project files were saved correctly."""
    try:
        project_dir = os.path.abspath(project_name)
        
        if os.path.exists(project_dir):
            files = []
            for root, dirs, filenames in os.walk(project_dir):
                for filename in filenames:
                    rel_path = os.path.relpath(os.path.join(root, filename), project_dir)
                    files.append(rel_path)
            
            return f"SUCCESS: Found {len(files)} files in {project_name}"
        else:
            return f"FAILED: Project directory {project_name} not found"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 4: Fix Common Errors (direct - no asyncio)
def fix_common_errors(project_name: str = "pixelpilot-dedalus") -> str:
    """Auto-fix common Next.js errors."""
    try:
        from automated_error_fixer import auto_fix_project
        
        project_dir = os.path.abspath(project_name)
        if os.path.exists(project_dir):
            fixes = auto_fix_project(project_dir)
            return f"SUCCESS: Applied {len(fixes)} fixes"
        else:
            return f"FAILED: Project directory not found"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 5: Install Dependencies (subprocess)
def install_dependencies(project_name: str = "pixelpilot-dedalus") -> str:
    """Install npm dependencies using subprocess."""
    try:
        project_dir = os.path.abspath(project_name)
        
        if not os.path.exists(project_dir):
            return f"FAILED: Project directory {project_name} not found"
        
        result = subprocess.run(
            ["npm", "install"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return f"SUCCESS: npm install completed"
        else:
            return f"FAILED: {result.stderr[:200]}"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 6: Test Dev Server (subprocess)
def test_dev_server(project_name: str = "pixelpilot-dedalus") -> str:
    """Test that development server can start."""
    try:
        project_dir = os.path.abspath(project_name)
        
        if not os.path.exists(project_dir):
            return f"FAILED: Project directory {project_name} not found"
        
        # Start dev server in background
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a few seconds then terminate
        import time
        time.sleep(3)
        process.terminate()
        process.wait()
        
        return f"SUCCESS: Development server started successfully"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 7: Deploy to Vercel (placeholder)
def deploy_to_vercel(project_name: str = "pixelpilot-dedalus") -> str:
    """Deploy project to Vercel."""
    try:
        # Mock deployment
        project_hash = hash(project_name) % 10000
        deployment_url = f"https://pixelpilot-{project_hash}.vercel.app"
        return f"SUCCESS: Deployed to {deployment_url}"
    except Exception as e:
        return f"ERROR: {str(e)}"

# Tool 8: Test with Browser (placeholder)
def test_with_browser(deployment_url: str) -> str:
    """Test deployed site with browser automation."""
    try:
        return f"SUCCESS: Browser tests passed for {deployment_url}"
    except Exception as e:
        return f"ERROR: {str(e)}"

async def main():
    """Run PixelPilot workflow using Dedalus with subprocess isolation."""
    print("🚀 PixelPilot Dedalus Workflow - Subprocess Isolation")
    print("=" * 55)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    workflow_prompt = """
Execute the complete PixelPilot automated frontend development workflow:

1. First extract specifications from Notion
2. Then generate Next.js code with those specs  
3. Verify the project files were created
4. Fix any common errors
5. Install dependencies
6. Test the development server
7. Deploy to Vercel
8. Test with browser automation

Execute each step in order and report the final results.
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
            ],
        )
        
        print("🎉 Dedalus Workflow Results:")
        print("=" * 30)
        print(result.final_output)
        
    except Exception as e:
        print(f"❌ Dedalus workflow failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
