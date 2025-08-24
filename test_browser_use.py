#!/usr/bin/env python3
"""
Simple test of Browser Use agent with our deployed URL
"""

import asyncio
import os
from browser_use import Agent
from browser_use.llm import ChatOpenAI, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

async def test_browser_use_simple():
    """Simple test of Browser Use with our deployed app"""
    
    # Use the deployed URL from our PixelPilot workflow
    url = "https://pixelpilot-project-iq4zyr9zy-rajashekarvs-projects.vercel.app"
    
    print(f"🎭 Testing Browser Use with: {url}")
    
    # Create agent with Claude (better vision)
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    
    agent = Agent(
        task=f"""
        Navigate to {url} and analyze this web application.
        
        Please:
        1. Take a screenshot of the homepage
        2. Describe what you see on the page
        3. Try clicking any buttons or interactive elements
        4. Give me a brief summary of the app's functionality
        5. Rate the design from 1-10
        
        Be specific about what elements you find and test.
        """,
        llm=llm,
        use_vision=True
    )
    
    try:
        print("🚀 Starting browser test...")
        history = await agent.run(max_steps=10)
        
        print("\n" + "="*50)
        print("🎯 BROWSER TEST RESULTS")
        print("="*50)
        
        # Get final result
        result = history.final_result()
        print(f"📋 Final Analysis:\n{result}")
        
        # Show screenshots
        screenshots = history.screenshot_paths()
        print(f"\n📸 Screenshots taken: {len(screenshots)}")
        for i, screenshot in enumerate(screenshots):
            print(f"  {i+1}. {screenshot}")
        
        # Show actions performed
        actions = history.action_names()
        print(f"\n🎬 Actions performed: {', '.join(actions)}")
        
        # Show URLs visited
        urls = history.urls()
        print(f"\n🌐 URLs visited: {urls}")
        
        # Check for errors
        errors = history.errors()
        if errors:
            print(f"\n❌ Errors found: {len(errors)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print("\n✅ No errors found")
        
        return True
        
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎭 Browser Use Test")
    print("=" * 30)
    
    # Run the test
    asyncio.run(test_browser_use_simple())
