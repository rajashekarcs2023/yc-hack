#!/usr/bin/env python3
"""
Test Single Notion Extraction Tool with Dedalus
===============================================

Test only the Notion extraction tool to isolate the issue.
"""

import asyncio
import subprocess
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
            return f"Extracted specs from Notion:\n\n{specs_content[:500]}..."
            
        return "Failed to extract specs from Notion"
        
    except Exception as e:
        return f"Error extracting specs: {str(e)}"

async def main():
    """Test single Notion extraction tool with Dedalus."""
    print("🧪 Testing Single Notion Tool with Dedalus")
    print("=" * 45)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    result = await runner.run(
        input="Call extract_notion_specs with action='extract' to get specifications from Notion", 
        model="openai/gpt-4o", 
        tools=[extract_notion_specs]
    )

    print(f"Result: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
