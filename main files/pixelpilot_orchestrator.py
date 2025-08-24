#!/usr/bin/env python3
"""
PixelPilot Orchestrator
======================

Coordinates the three-agent workflow:
1. Agent 1: Extract specs from Notion + Generate code
2. Agent 2: Install deps + Fix errors + Test + Deploy
3. Agent 3: Browser testing + Analysis + Feedback to Notion

Extracts project name from Agent 1, deployment URL from Agent 2, and passes to Agent 3.
"""

import asyncio
import subprocess
import re
import sys
from datetime import datetime

async def run_agent1():
    """Run Agent 1 and extract project name from output."""
    print("🚀 Starting Agent 1: Specs Extraction + Code Generation")
    print("=" * 60)
    print("📋 Status: Extracting specs from Notion...")
    
    try:
        # Start the process
        process = subprocess.Popen(
            ["python", "agent1_specs_generation.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        output_lines = []
        
        # Read output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"📝 Agent 1: {output.strip()}")
                output_lines.append(output)
        
        # Wait for completion
        process.wait()
        full_output = ''.join(output_lines)
        
        if process.returncode == 0:
            print("\n🎉 Agent 1 COMPLETED!")
            print("=" * 30)
            
            # Extract project name from output - try multiple patterns
            patterns = [
                r"project ['\"]([^'\"]+)['\"]",  # project 'name'
                r"named ['\"]([^'\"]+)['\"]",    # named 'name'
                r"project named ([A-Za-z0-9_-]+)",  # project named name
                r"(pixelpilot-project)",         # fixed project name
                r"(pixelpilot-\d+_\d+)",        # pixelpilot-timestamp
                r"(UniqueProfileCardProject)",   # specific fallback
                r"([A-Za-z0-9_-]*[Pp]rofile[A-Za-z0-9_-]*)"  # any profile project
            ]
            
            project_name = None
            for pattern in patterns:
                match = re.search(pattern, full_output)
                if match:
                    project_name = match.group(1)
                    break
            
            if project_name:
                print(f"✅ Project created: {project_name}")
                return project_name
                
            print("⚠️ Agent 1 completed but couldn't extract project name")
            return None
        else:
            stderr_output = process.stderr.read()
            print(f"❌ Agent 1 failed: {stderr_output}")
            return None
            
    except Exception as e:
        print(f"❌ Agent 1 error: {e}")
        return None

async def run_agent2(project_name):
    """Run Agent 2 with the project name from Agent 1."""
    print(f"\n🚀 Starting Agent 2: Project Management + Deployment")
    print(f"📁 Target project: {project_name}")
    print("=" * 60)
    print("📋 Status: Installing dependencies and deploying...")
    
    try:
        # Start the process
        process = subprocess.Popen(
            ["python", "agent2_project_deployment.py", project_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        output_lines = []
        
        # Read output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"📝 Agent 2: {output.strip()}")
                output_lines.append(output)
        
        # Wait for completion
        process.wait()
        full_output = ''.join(output_lines)
        
        if process.returncode == 0:
            print("\n🎉 Agent 2 COMPLETED!")
            print("=" * 30)
            
            # Extract deployment URL from output
            url_match = re.search(r"https://[^\s]+\.vercel\.app", full_output)
            if url_match:
                deployment_url = url_match.group(0)
                print(f"✅ Deployed to: {deployment_url}")
                return deployment_url
            else:
                print("✅ Project management completed successfully")
                return "completed"
        else:
            stderr_output = process.stderr.read()
            print(f"❌ Agent 2 failed: {stderr_output}")
            return None
            
    except Exception as e:
        print(f"❌ Agent 2 error: {e}")
        return None

async def run_agent3(deployment_url, project_name):
    """Run Agent 3 with deployment URL for browser testing and feedback."""
    print("\n🚀 Starting Agent 3: Browser Testing and Analysis")
    print("=" * 60)
    print(f"🌐 Testing URL: {deployment_url}")
    
    try:
        # Start the process with deployment URL as argument
        process = subprocess.Popen(
            ["python", "-c", f"""
import asyncio
import sys
sys.path.append('.')
from agent3_browser_testing import run_agent3_workflow

async def main():
    url = "{deployment_url}"
    project_name = "{project_name}"
    result = await run_agent3_workflow(url, project_name)
    if result:
        print("SUCCESS: Agent 3 completed successfully")
    else:
        print("FAILED: Agent 3 failed")

asyncio.run(main())
"""],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        output_lines = []
        
        # Read output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"🎭 Agent 3: {output.strip()}")
                output_lines.append(output)
        
        # Wait for completion
        process.wait()
        full_output = ''.join(output_lines)
        
        if process.returncode == 0 and "SUCCESS" in full_output:
            print("\n🎉 Agent 3 COMPLETED!")
            print("=" * 30)
            return True
        else:
            stderr_output = process.stderr.read()
            print(f"❌ Agent 3 failed: {stderr_output}")
            return False
            
    except Exception as e:
        print(f"❌ Agent 3 error: {e}")
        return False

async def main():
    """Orchestrate the complete PixelPilot workflow."""
    print("🎯 PixelPilot Orchestrator - Three-Agent Workflow")
    print("=" * 60)
    start_time = datetime.now()
    
    # Step 1: Run Agent 1
    project_name = await run_agent1()
    if not project_name:
        print("❌ Workflow failed at Agent 1")
        return
    
    # Step 2: Run Agent 2
    deployment_result = await run_agent2(project_name)
    if not deployment_result or not deployment_result.startswith("https://"):
        print("❌ Workflow failed at Agent 2 - no deployment URL")
        return
    
    # Step 3: Run Agent 3
    agent3_result = await run_agent3(deployment_result, project_name)
    if not agent3_result:
        print("❌ Workflow failed at Agent 3")
        return
    
    # Success!
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("🎉 PIXELPILOT WORKFLOW COMPLETE!")
    print("=" * 60)
    print(f"📁 Project: {project_name}")
    print(f"🌐 Deployment: {deployment_result}")
    print(f"🎭 Browser Testing: ✅ Completed with feedback to Notion")
    print(f"⏱️  Total time: {duration:.1f} seconds")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
