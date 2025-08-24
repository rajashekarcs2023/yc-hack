#!/usr/bin/env python3
"""
Agent 1: Notion Specs Extraction + V0 Code Generation
====================================================

Focused agent that only handles:
1. Extract specifications from Notion
2. Generate Next.js project code using V0 API
"""

import asyncio
import subprocess
import os
import time
from datetime import datetime
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

def generate_v0_code(specs: str, project_name: str = "pixelpilot-project") -> str:
    """Generate Next.js project code using multi-API fallback strategy."""
    try:
        # Use fixed project name for consistency
        if not project_name:
            project_name = "pixelpilot-project"
        
        # Set environment variable for project name
        env = os.environ.copy()
        env['PIXELPILOT_PROJECT_NAME'] = project_name
        
        # Use multi-API generator with fallback
        result = subprocess.run(
            ["python", "-c", f"""
import asyncio
import sys
import os
sys.path.append('.')
from multi_api_code_generator import generate_code_multi_api
from step2_test_v0_generation import save_generated_project

async def main():
    specs = '''{specs}'''
    content, source = await generate_code_multi_api(specs)
    if content:
        success = save_generated_project(content, '{project_name}')
        if success:
            print(f'SUCCESS: Code generated using {{source}} and saved to {project_name}')
        else:
            print('FAILED: Could not save generated files')
    else:
        print('FAILED: All code generation APIs failed')

asyncio.run(main())
            """],
            capture_output=True,
            text=True,
            timeout=180,
            env=env
        )
        
        if result.returncode == 0:
            output = result.stdout
            if "SUCCESS:" in output:
                return output.strip()
            
        return f"FAILED: Multi-API generation error - {result.stderr[:200]}"
        
    except Exception as e:
        return f"ERROR: {str(e)}"

async def main():
    """Agent 1: Extract specs and generate code."""
    print("🤖 Agent 1: Specs Extraction + Code Generation")
    print("=" * 50)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    result = await runner.run(
        input="Extract specifications from Notion, then generate Next.js code using V0 API. Use the project name 'pixelpilot-project' for the generated project.", 
        model="openai/gpt-4o", 
        tools=[extract_notion_specs, generate_v0_code]
    )

    print(f"🎉 Agent 1 Result:\n{result.final_output}")
    return result.final_output

if __name__ == "__main__":
    asyncio.run(main())
