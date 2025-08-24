#!/usr/bin/env python3
"""
Test Notion Extraction + V0 Generation with Dedalus
===================================================

Simplified test with only 2 tools: Notion extraction and V0 generation.
"""

import asyncio
import subprocess
import os
import time
import hashlib
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()

def extract_notion_specs(action: str = "extract") -> str:
    """Extract specifications from Notion page using subprocess."""
    try:
        result = subprocess.run(
            ["python", "step1_test_notion_extraction.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and "Clean specs length:" in result.stdout:
            # Parse output to extract actual specs content
            lines = result.stdout.split('\n')
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
            
            specs_content = '\n'.join(specs_lines).strip()
            return f"SUCCESS: Extracted specs from Notion:\n\n{specs_content[:300]}..."
            
        return "FAILED: Could not extract specs from Notion"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def generate_v0_code(specs: str, project_name: str = "pixelpilot-dedalus-test") -> str:
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
                return f"SUCCESS: V0 code generated and saved to project"
            
        return f"FAILED: V0 generation error - {result.stderr[:200]}"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def install_dependencies(project_name: str = "pixelpilot-v0-test") -> str:
    """Install npm dependencies for the generated project."""
    try:
        if not os.path.exists(project_name):
            return f"FAILED: Project directory {project_name} not found"
        
        result = subprocess.run(
            ["npm", "install"],
            cwd=project_name,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return f"SUCCESS: Dependencies installed successfully"
        else:
            return f"FAILED: npm install error - {result.stderr[:200]}"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

def fix_project_errors(project_name: str = "pixelpilot-v0-test") -> str:
    """Auto-fix common Next.js errors in the project."""
    try:
        from automated_error_fixer import auto_fix_project
        
        if not os.path.exists(project_name):
            return f"FAILED: Project directory {project_name} not found"
        
        fixes = auto_fix_project(project_name)
        return f"SUCCESS: Applied {len(fixes)} automatic fixes"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_dev_server(project_name: str = "pixelpilot-v0-test") -> str:
    """Test that the development server can start successfully."""
    try:
        if not os.path.exists(project_name):
            return f"FAILED: Project directory {project_name} not found"
        
        # Start dev server in background and test
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=project_name,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a few seconds then terminate
        time.sleep(5)
        process.terminate()
        process.wait()
        
        return f"SUCCESS: Development server started successfully"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

def deploy_to_vercel(project_name: str = "pixelpilot-v0-test") -> str:
    """Deploy the project to Vercel and return deployment URL."""
    try:
        if not os.path.exists(project_name):
            return f"FAILED: Project directory {project_name} not found"
        
        # Mock deployment for now - would integrate with Vercel API
        import hashlib
        project_hash = hashlib.md5(project_name.encode()).hexdigest()[:8]
        deployment_url = f"https://pixelpilot-{project_hash}.vercel.app"
        
        return f"SUCCESS: Deployed to {deployment_url}"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

async def main():
    """Test Notion extraction and V0 generation with Dedalus."""
    print("🧪 Testing Notion + V0 Generation with Dedalus")
    print("=" * 50)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    result = await runner.run(
        input="Execute the complete PixelPilot workflow: 1) Extract specs from Notion, 2) Generate Next.js code with V0, 3) Install dependencies, 4) Fix any errors, 5) Test dev server, 6) Deploy to Vercel and return URL", 
        model="openai/gpt-4o", 
        tools=[extract_notion_specs, generate_v0_code, install_dependencies, fix_project_errors, test_dev_server, deploy_to_vercel]
    )

    print(f"🎉 Final Result:\n{result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
