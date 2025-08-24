#!/usr/bin/env python3
"""
Test Dedalus Tools Step by Step
===============================

Test each PixelPilot tool individually before orchestration.
"""

import asyncio
import os
from dotenv import load_dotenv

# Import our working components
from step1_test_notion_extraction import test_notion_extraction
from automated_error_fixer import auto_fix_project

load_dotenv()

async def test_step1_notion():
    """Test Step 1: Notion extraction"""
    print("🔍 Testing Step 1: Notion Extraction")
    try:
        specs = await test_notion_extraction()
        if specs:
            print(f"✅ Success: {len(specs)} characters extracted")
            return specs
        else:
            print("❌ Failed: No specs returned")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def test_step2_v0_generation(specs):
    """Test Step 2: V0 Code Generation (using our working format)"""
    print("\n🤖 Testing Step 2: V0 Code Generation")
    
    if not specs:
        print("❌ Skipping: No specs from Step 1")
        return None
        
    try:
        # Use our working V0 function from step2_test_v0_generation.py
        from step2_test_v0_generation import test_v0_code_generation
        
        result = await test_v0_code_generation()
        if result:
            print("✅ Success: V0 code generated")
            return result
        else:
            print("❌ Failed: No code generated")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_step3_error_fixing():
    """Test Step 3: Error Fixing"""
    print("\n🔧 Testing Step 3: Error Fixing")
    
    # Test on existing project
    test_project = "pixelpilot-v0-test"
    if os.path.exists(test_project):
        try:
            fixes = auto_fix_project(test_project)
            print(f"✅ Success: Applied {len(fixes)} fixes")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("⚠️  Skipping: No test project found")
        return True

def test_step4_npm_install():
    """Test Step 4: NPM Install (synchronous to avoid asyncio conflicts)"""
    print("\n📦 Testing Step 4: NPM Install")
    
    test_project = "pixelpilot-v0-test"
    if os.path.exists(test_project):
        try:
            import subprocess
            result = subprocess.run(
                ["npm", "install"],
                cwd=test_project,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ Success: npm install completed")
                return True
            else:
                print(f"❌ Failed: {result.stderr[:100]}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("⚠️  Skipping: No test project found")
        return True

async def main():
    """Test all tools step by step"""
    print("🧪 Testing Dedalus Tools Step by Step")
    print("=" * 40)
    
    # Step 1: Notion
    specs = await test_step1_notion()
    
    # Step 2: V0 Generation  
    generated_code = await test_step2_v0_generation(specs)
    
    # Step 3: Error Fixing
    test_step3_error_fixing()
    
    # Step 4: NPM Install
    test_step4_npm_install()
    
    print("\n" + "=" * 40)
    print("🎯 Individual Tool Testing Complete")
    
    if specs and generated_code:
        print("✅ Ready for Dedalus orchestration")
    else:
        print("❌ Fix individual tools before orchestration")

if __name__ == "__main__":
    asyncio.run(main())
