#!/usr/bin/env python3
"""
Agent 3: Browser Testing and Analysis Agent
Uses Dedalus with three tools:
1. extract_specs - Extract specs from Notion
2. browser_test_analysis - Test deployed app with Browser Use
3. write_to_notion - Write results to new Notion page
"""

import asyncio
import os
import subprocess
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def extract_specs() -> str:
    """Tool 1: Extract specifications from Notion page using subprocess (same as Agent 1)"""
    print("🔍 Extracting specs from Notion...")
    
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
            print("✅ Specs extracted successfully")
            return specs_content
            
        print("❌ Could not extract specs from Notion")
        return "FAILED: Could not extract specs from Notion"
        
    except subprocess.TimeoutExpired:
        print("❌ Specs extraction timed out")
        return "ERROR: Specs extraction timed out"
    except Exception as e:
        print(f"❌ Specs extraction error: {e}")
        return f"ERROR: {str(e)}"

def browser_test_analysis(url: str, specs: str, project_name: str = "pixelpilot-project") -> str:
    """Tool 2: Test deployed app using Browser Use with spec comparison"""
    print(f"🎭 Testing deployed app: {url}")
    
    try:
        # Create a temporary file with specs for the subprocess
        specs_file = f"/tmp/specs_{project_name}.txt"
        with open(specs_file, 'w') as f:
            f.write(specs)
        
        result = subprocess.run([
            "python", "-c", f"""
import asyncio
import sys
import os
sys.path.append('.')
from browser_use import Agent
from browser_use.llm import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

async def main():
    try:
        # Read specs from file
        with open('{specs_file}', 'r') as f:
            original_specs = f.read()
        
        # Create browser agent with Claude
        llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        
        agent = Agent(
            task='''
            Test this deployed web application: {url}
            
            IMPORTANT: You need to evaluate how well this implementation matches the original specifications.
            
            ORIGINAL SPECIFICATIONS:
            ''' + original_specs + '''
            
            Please perform the following comprehensive testing:
            1. Navigate to the URL and take a screenshot
            2. Compare the visual design against the original specs
            3. Test any interactive elements mentioned in specs
            4. Check if all required features are implemented
            5. Evaluate how closely it matches the specified requirements
            6. Look for any missing features or deviations
            
            Provide detailed feedback on:
            - SPEC COMPLIANCE: How well does it match the original requirements? (1-10)
            - MISSING FEATURES: What's missing from the specs?
            - EXTRA FEATURES: What was added beyond specs?
            - VISUAL ACCURACY: Does the design match spec descriptions?
            - FUNCTIONALITY: Do interactive elements work as specified?
            - OVERALL IMPLEMENTATION QUALITY: (1-10)
            
            Be specific about what matches the specs and what doesn't.
            ''',
            llm=llm,
            use_vision=True
        )
        
        # Run the browser testing
        history = await agent.run(max_steps=15)
        
        # Get results
        final_result = history.final_result()
        screenshots = history.screenshot_paths()
        errors = history.errors()
        
        print("ANALYSIS_START")
        print(f"URL: {url}")
        print(f"Screenshots: {{len(screenshots)}}")
        print(f"Errors: {{len(errors)}}")
        print("RESULT:")
        print(final_result)
        print("ANALYSIS_END")
        
    except Exception as e:
        print(f"ERROR: Browser testing failed: {{e}}")
    finally:
        # Clean up specs file
        try:
            os.remove('{specs_file}')
        except:
            pass

asyncio.run(main())
"""
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            output = result.stdout
            if "ANALYSIS_START" in output and "ANALYSIS_END" in output:
                analysis = output.split("ANALYSIS_START")[1].split("ANALYSIS_END")[0].strip()
                print("✅ Browser testing completed")
                return analysis
            else:
                print("✅ Browser testing completed (check logs)")
                return "Browser testing completed - see logs for details"
        else:
            print(f"❌ Browser testing failed: {result.stderr}")
            return f"Browser testing failed: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        print("❌ Browser testing timed out")
        return "Browser testing timed out"
    except Exception as e:
        print(f"❌ Browser testing error: {e}")
        return f"Error: {str(e)}"

def write_to_notion(analysis: str, project_name: str = "pixelpilot-project") -> str:
    """Tool 3: Write test results to new Notion page using create-pages tool"""
    print("📝 Writing results to Notion...")
    
    try:
        # Create timestamp for page title
        timestamp = datetime.now().isoformat()[:19]
        page_title = f"Browser Test: {project_name} - {timestamp}"
        
        # Format content for Notion
        content = f"""## Browser Test Results - {timestamp}

**Project:** {project_name}
**Status:** ✅ Completed

### Analysis Results
{analysis}

### Test Summary
- **Timestamp:** {timestamp}
- **Test Type:** Spec Compliance Analysis
- **Agent:** Browser Use with Claude Vision

---
Generated by PixelPilot Agent 3"""
        
        result = subprocess.run([
            "python", "-c", f"""
import asyncio
import sys
sys.path.append('.')
from notion_mcp_client import NotionMCPService

async def main():
    try:
        notion_service = NotionMCPService()
        await notion_service.start()
        
        # Use create-pages tool (correct tool name)
        result = await notion_service.client.call_tool("create-pages", {{
            "title": "{page_title}",
            "content": '''{content}'''
        }})
        
        if result and not result.get('error'):
            print("SUCCESS: New Notion page created: {page_title}")
        else:
            print(f"ERROR: Failed to create Notion page: {{result}}")
            
    except Exception as e:
        print(f"ERROR: Notion write failed: {{e}}")
    finally:
        try:
            await notion_service.stop()
        except:
            pass

asyncio.run(main())
"""
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and "SUCCESS" in result.stdout:
            print("✅ Results written to Notion")
            return f"Successfully created Notion page: {page_title}"
        else:
            print(f"❌ Notion write failed: {result.stderr}")
            return f"Failed to write to Notion: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        print("❌ Notion write timed out")
        return "Notion write timed out"
    except Exception as e:
        print(f"❌ Notion write error: {e}")
        return f"Error: {str(e)}"

# Main Agent 3 workflow
async def run_agent3_workflow(url: str, project_name: str = "pixelpilot-project"):
    """Complete Agent 3 workflow: Extract specs -> Test app -> Write to Notion"""
    
    print("🚀 Starting Agent 3: Browser Testing and Analysis")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # Step 1: Extract specs from Notion
    print("\n📋 STEP 1: Extracting specifications from Notion")
    specs = extract_specs()
    
    if "Error" in specs or "No specifications" in specs:
        print(f"❌ Agent 3 failed at Step 1: {specs}")
        return False
    
    # Step 2: Browser testing with spec analysis
    print(f"\n🎭 STEP 2: Testing deployed app with spec comparison")
    analysis = browser_test_analysis(url, specs, project_name)
    
    if "Error" in analysis or "failed" in analysis:
        print(f"❌ Agent 3 failed at Step 2: {analysis}")
        return False
    
    # Step 3: Write results to Notion
    print(f"\n📝 STEP 3: Writing test results to Notion")
    notion_result = write_to_notion(analysis, project_name)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("🎯 AGENT 3 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"✅ Specs Extraction: Success")
    print(f"✅ Browser Testing: Success") 
    print(f"✅ Notion Documentation: {'Success' if 'Successfully' in notion_result else 'Failed'}")
    print(f"⏱️  Total Duration: {duration:.1f} seconds")
    print(f"🌐 Tested URL: {url}")
    
    return "Successfully" in notion_result

# Test with existing deployment
async def test_agent3():
    """Test Agent 3 with existing PixelPilot deployment"""
    url = "https://pixelpilot-project-iq4zyr9zy-rajashekarvs-projects.vercel.app"
    result = await run_agent3_workflow(url, "pixelpilot-project")
    return result

if __name__ == "__main__":
    print("🤖 Agent 3: Browser Testing and Analysis")
    print("=" * 50)
    
    # Test the complete workflow
    asyncio.run(test_agent3())
