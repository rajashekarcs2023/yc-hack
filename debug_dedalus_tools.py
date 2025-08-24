#!/usr/bin/env python3
"""
Debug Dedalus Tool Message Format Issue
=======================================

Test different tool patterns to identify the root cause.
"""

import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()

# Test 1: Simple tool with no parameters (like math example)
def simple_test() -> str:
    """Simple test function with no parameters."""
    return "Simple test executed successfully"

# Test 2: Tool that takes a parameter
def parameterized_test(message: str) -> str:
    """Test function that takes a parameter."""
    return f"Received message: {message}"

# Test 3: Tool that does subprocess (like our Notion tool)
def subprocess_test() -> str:
    """Test subprocess execution."""
    import subprocess
    try:
        result = subprocess.run(["echo", "Hello from subprocess"], capture_output=True, text=True)
        return f"Subprocess result: {result.stdout.strip()}"
    except Exception as e:
        return f"Subprocess error: {str(e)}"

async def test_simple_tool():
    """Test 1: Simple tool with no parameters."""
    print("🧪 Test 1: Simple Tool (No Parameters)")
    print("-" * 40)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    try:
        result = await runner.run(
            input="Execute the simple_test function", 
            model="openai/gpt-4o", 
            tools=[simple_test]
        )
        print(f"✅ Success: {result.final_output}")
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

async def test_parameterized_tool():
    """Test 2: Tool with parameters."""
    print("\n🧪 Test 2: Parameterized Tool")
    print("-" * 40)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    try:
        result = await runner.run(
            input="Call parameterized_test with message 'Hello World'", 
            model="openai/gpt-4o", 
            tools=[parameterized_test]
        )
        print(f"✅ Success: {result.final_output}")
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

async def test_subprocess_tool():
    """Test 3: Subprocess tool."""
    print("\n🧪 Test 3: Subprocess Tool")
    print("-" * 40)
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    try:
        result = await runner.run(
            input="Execute the subprocess_test function", 
            model="openai/gpt-4o", 
            tools=[subprocess_test]
        )
        print(f"✅ Success: {result.final_output}")
        return True
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

async def main():
    """Run all debugging tests."""
    print("🔍 Debugging Dedalus Tool Message Format Issue")
    print("=" * 50)
    
    results = []
    
    # Test 1: Simple tool
    results.append(await test_simple_tool())
    
    # Test 2: Parameterized tool
    results.append(await test_parameterized_tool())
    
    # Test 3: Subprocess tool
    results.append(await test_subprocess_tool())
    
    print("\n" + "=" * 50)
    print("🎯 Debug Results Summary")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🚀 All tests passed - tool format is correct")
    else:
        print("❌ Some tests failed - investigating tool format issues")

if __name__ == "__main__":
    asyncio.run(main())
