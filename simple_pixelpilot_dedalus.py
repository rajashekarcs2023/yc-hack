#!/usr/bin/env python3
"""
Simple PixelPilot Dedalus Workflow
==================================

Simplified version matching the working math example pattern.
"""

import asyncio
import subprocess
import os
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()

def extract_specs() -> str:
    """Extract specifications from Notion page."""
    try:
        result = subprocess.run(
            ["python", "step1_test_notion_extraction.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and "Clean specs length:" in result.stdout:
            return "Specs extracted successfully from Notion"
        return "Failed to extract specs"
        
    except Exception as e:
        return f"Error: {str(e)}"

def generate_code() -> str:
    """Generate Next.js code using V0 API."""
    try:
        result = subprocess.run(
            ["python", "step2_test_v0_generation.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0 and "Saved" in result.stdout:
            return "Next.js code generated successfully"
        return "Failed to generate code"
        
    except Exception as e:
        return f"Error: {str(e)}"

def install_deps() -> str:
    """Install npm dependencies."""
    try:
        if os.path.exists("pixelpilot-v0-test"):
            result = subprocess.run(
                ["npm", "install"],
                cwd="pixelpilot-v0-test",
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return "Dependencies installed successfully"
            
        return "Failed to install dependencies"
        
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    """Run simplified PixelPilot workflow."""
    print("🚀 Simple PixelPilot Dedalus Workflow")
    print("=" * 40)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    result = await runner.run(
        input="Execute the PixelPilot workflow: extract specs, generate code, and install dependencies", 
        model="openai/gpt-4o", 
        tools=[extract_specs, generate_code, install_deps]
    )

    print(f"Result: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
