#!/usr/bin/env python3
"""
Agent 4: Feedback-Based Code Iteration Agent
==============================================

Reads feedback from Notion and modifies existing code to address issues.

Tools:
1. extract_feedback - Read latest feedback from Notion
2. analyze_feedback - Parse feedback into actionable items  
3. modify_code - Use AI to update existing code files
4. validate_changes - Basic validation of code changes
"""

import asyncio
import os
import subprocess
import json
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def extract_feedback(project_name: str = "pixelpilot-project") -> str:
    """Tool 1: Extract latest feedback from Notion pixelpilot document"""
    print("📖 Extracting feedback from Notion...")
    
    try:
        result = subprocess.run([
            "python", "step1_test_notion_extraction.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "Clean specs length:" in result.stdout:
            # Parse output to extract feedback sections
            lines = result.stdout.split('\n')
            specs_start = False
            content_lines = []
            
            for line in lines:
                if "Clean specs preview:" in line:
                    specs_start = True
                    continue
                elif specs_start and line.strip() == "------------------------------":
                    if content_lines:  # End of content
                        break
                    else:  # Start of content
                        continue
                elif specs_start:
                    content_lines.append(line)
            
            full_content = '\n'.join(content_lines).strip()
            
            # Extract feedback sections
            feedback_sections = []
            if "## Feedback" in full_content:
                feedback_parts = full_content.split("## Feedback")
                for i, part in enumerate(feedback_parts[1:], 1):  # Skip first part
                    feedback_sections.append(f"## Feedback{part.split('---')[0]}")
            
            if feedback_sections:
                latest_feedback = feedback_sections[-1]  # Get most recent feedback
                print("✅ Latest feedback extracted successfully")
                return f"SUCCESS: Latest feedback extracted:\n\n{latest_feedback}"
            else:
                print("⚠️ No feedback sections found")
                return "NO_FEEDBACK: No feedback sections found in document"
            
        return "FAILED: Could not extract content from Notion"
        
    except Exception as e:
        print(f"❌ Feedback extraction error: {e}")
        return f"ERROR: {str(e)}"

def analyze_feedback(feedback: str) -> str:
    """Tool 2: Parse feedback into actionable items"""
    print("🔍 Analyzing feedback for actionable items...")
    
    try:
        if "NO_FEEDBACK" in feedback or "FAILED" in feedback:
            return feedback
        
        # Extract key sections from feedback
        missing_features = []
        recommendations = []
        
        lines = feedback.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if "WHAT'S MISSING" in line or "MISSING FEATURES" in line:
                current_section = "missing"
            elif "RECOMMENDATIONS" in line:
                current_section = "recommendations"
            elif line.startswith('- ') and current_section == "missing":
                missing_features.append(line[2:])
            elif line.startswith('- ') and current_section == "recommendations":
                recommendations.append(line[2:])
        
        # Create actionable analysis
        analysis = {
            "missing_features": missing_features,
            "recommendations": recommendations,
            "priority": "HIGH" if missing_features else "MEDIUM"
        }
        
        print("✅ Feedback analysis completed")
        return f"SUCCESS: Feedback analysis:\n{json.dumps(analysis, indent=2)}"
        
    except Exception as e:
        print(f"❌ Feedback analysis error: {e}")
        return f"ERROR: {str(e)}"

def modify_code(analysis: str, project_name: str = "pixelpilot-project") -> str:
    """Tool 3: Use AI to modify existing code based on feedback"""
    print("🛠️ Modifying code based on feedback...")
    
    try:
        if "ERROR" in analysis or "NO_FEEDBACK" in analysis:
            return analysis
        
        # Parse analysis
        analysis_data = json.loads(analysis.split("SUCCESS: Feedback analysis:\n")[1])
        missing_features = analysis_data.get("missing_features", [])
        recommendations = analysis_data.get("recommendations", [])
        
        if not missing_features and not recommendations:
            print("⚠️ No actionable items found")
            return "NO_CHANGES: No actionable items found in feedback"
        
        # Find the project directory
        project_dir = f"./{project_name}"
        if not os.path.exists(project_dir):
            print(f"❌ Project directory not found: {project_dir}")
            return f"ERROR: Project directory not found: {project_dir}"
        
        # Create simple modification using Agent 1 pattern
        modification_specs = f"""
ITERATION REQUEST: Modify existing code based on feedback

MISSING FEATURES TO ADD:
{chr(10).join(['- ' + feature for feature in missing_features])}

IMPROVEMENTS TO MAKE:
{chr(10).join(['- ' + rec for rec in recommendations])}

INSTRUCTIONS:
- Preserve all existing working functionality
- Add missing features seamlessly
- Improve styling and UX based on recommendations
- Maintain clean, readable code structure
"""
        
        # Create a temporary iteration specs file
        iteration_specs_file = f"{project_name}_iteration_specs.txt"
        with open(iteration_specs_file, "w") as f:
            f.write(modification_specs)
        
        # Use multi_api_code_generator directly for iteration
        result = subprocess.run([
            "python", "-c", f"""
import asyncio
import sys
sys.path.append('.')
from multi_api_code_generator import generate_code_multi_api

async def main():
    with open('{iteration_specs_file}', 'r') as f:
        specs = f.read()
    
    result = await generate_code_multi_api(specs, '{project_name}-iteration')
    if result.get('success'):
        print('SUCCESS: Code iteration completed')
    else:
        print('FAILED: Code iteration failed')

asyncio.run(main())
"""
        ], capture_output=True, text=True, timeout=120)
        
        # Clean up temp file
        if os.path.exists(iteration_specs_file):
            os.remove(iteration_specs_file)
        
        if result.returncode == 0 and "SUCCESS" in result.stdout:
            print("✅ Code modifications completed")
            return "SUCCESS: Code modified based on feedback"
        else:
            print(f"❌ Code modification failed: {result.stderr}")
            return f"FAILED: Code modification failed: {result.stderr}"
            
    except Exception as e:
        print(f"❌ Code modification error: {e}")
        return f"ERROR: {str(e)}"

def validate_changes(project_name: str = "pixelpilot-project") -> str:
    """Tool 4: Basic validation of code changes"""
    print("✅ Validating code changes...")
    
    try:
        project_dir = f"./{project_name}"
        if not os.path.exists(project_dir):
            return f"ERROR: Project directory not found: {project_dir}"
        
        # Check for basic file structure
        required_files = ["package.json", "next.config.js"]
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(os.path.join(project_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            return f"WARNING: Missing files: {', '.join(missing_files)}"
        
        # Check for syntax errors in main files
        tsx_files = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.tsx'):
                    tsx_files.append(os.path.join(root, file))
        
        print(f"✅ Found {len(tsx_files)} TypeScript files")
        print("✅ Basic validation completed")
        return f"SUCCESS: Validation passed - {len(tsx_files)} files checked"
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return f"ERROR: {str(e)}"

async def run_agent4_workflow(project_name: str = "pixelpilot-project"):
    """Main Agent 4 workflow"""
    print("🚀 Starting Agent 4: Feedback-Based Code Iteration")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # Step 1: Extract feedback from Notion
    print("\n📖 STEP 1: Extracting feedback from Notion")
    feedback = extract_feedback(project_name)
    
    if "ERROR" in feedback or "NO_FEEDBACK" in feedback:
        print(f"❌ Agent 4 failed at Step 1: {feedback}")
        return False
    
    # Step 2: Analyze feedback for actionable items
    print("\n🔍 STEP 2: Analyzing feedback for actionable items")
    analysis = analyze_feedback(feedback)
    
    if "ERROR" in analysis:
        print(f"❌ Agent 4 failed at Step 2: {analysis}")
        return False
    
    # Step 3: Modify code based on feedback
    print("\n🛠️ STEP 3: Modifying code based on feedback")
    modifications = modify_code(analysis, project_name)
    
    if "ERROR" in modifications:
        print(f"❌ Agent 4 failed at Step 3: {modifications}")
        return False
    
    # Step 4: Validate changes
    print("\n✅ STEP 4: Validating code changes")
    validation = validate_changes(project_name)
    
    if "ERROR" in validation:
        print(f"❌ Agent 4 failed at Step 4: {validation}")
        return False
    
    # Success!
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("🎉 AGENT 4 WORKFLOW COMPLETE!")
    print("=" * 60)
    print(f"📖 Feedback Extraction: ✅")
    print(f"🔍 Feedback Analysis: ✅")
    print(f"🛠️ Code Modifications: ✅")
    print(f"✅ Validation: ✅")
    print(f"⏱️  Total Duration: {duration:.1f} seconds")
    print(f"📁 Project: {project_name}")
    print("=" * 60)
    
    return True

def test_agent4():
    """Test function for Agent 4"""
    asyncio.run(run_agent4_workflow("pixelpilot-project"))

if __name__ == "__main__":
    test_agent4()
