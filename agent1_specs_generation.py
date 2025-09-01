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
    """Extract specifications from Notion page using direct API call."""
    try:
        # Import the NotionMCPTool directly and use it to get full specs
        import asyncio
        from dedalus_notion_tool import NotionMCPTool
        
        async def get_full_specs():
            notion_tool = NotionMCPTool()
            pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
            
            result = await notion_tool.fetch_notion_page(pixelpilot_page_id)
            
            if result.get("success"):
                content = result.get("content", "")
                
                # Extract text from MCP response
                if isinstance(content, list) and len(content) > 0:
                    raw_text = content[0].text if hasattr(content[0], 'text') else str(content[0])
                else:
                    raw_text = str(content)
                
                # Parse the JSON-like response to extract clean specs
                import json
                try:
                    # Try to parse as JSON first
                    parsed = json.loads(raw_text)
                    specs_text = parsed.get("text", raw_text)
                    
                    # Extract content between <content> tags if present
                    if "<content>" in specs_text and "</content>" in specs_text:
                        start = specs_text.find("<content>") + len("<content>")
                        end = specs_text.find("</content>")
                        specs_text = specs_text[start:end].strip()
                    
                except json.JSONDecodeError:
                    # If not JSON, use raw text
                    specs_text = raw_text
                
                return specs_text
            else:
                return None
        
        # Get the full specs directly
        specs_content = asyncio.run(get_full_specs())
        
        if specs_content is None:
            return "FAILED: Could not extract specs from Notion"
            
        # DEBUG: Print extracted specs
        print("=" * 60)
        print(" DEBUG: EXTRACTED SPECS FROM NOTION")
        print("=" * 60)
        print(f"Specs length: {len(specs_content)} characters")
        print("Specs content:")
        print(specs_content)
        print("=" * 60)
        
        if specs_content and len(specs_content) > 100:  # Ensure we got substantial content
            return f"SUCCESS: Extracted specs from Notion:\n{specs_content}"
        else:
            return "FAILED: No substantial specs content found in Notion output"
            
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
    
    # DEBUG: Print specs being passed to code generation
    print("=" * 60)
    print("🔍 DEBUG: SPECS PASSED TO CODE GENERATION")
    print("=" * 60)
    print(f"Specs length: {{len(specs)}} characters")
    print("Specs content:")
    print(specs)
    print("=" * 60)
    
    content, source = await generate_code_multi_api(specs)
    
    # DEBUG: Print generated content info
    print("=" * 60)
    print("🔍 DEBUG: CODE GENERATION RESULT")
    print("=" * 60)
    print(f"Generated content length: {{len(content)}} characters")
    print(f"Source: {{source}}")
    print("First 500 chars of content:")
    print(content[:500] if content else "NO CONTENT")
    print("=" * 60)
    
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
