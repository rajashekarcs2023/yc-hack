#!/usr/bin/env python3
"""
Simple V0 Test - Minimal specs for fast testing
==============================================
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

# Minimal test specs
SIMPLE_SPECS = """
Create a simple React button component that says "Click me" with blue background.
"""

async def test_v0_simple():
    """Test V0 API with minimal specs."""
    print("🧪 Testing V0 with simple specs...")
    print(f"📝 Specs: {SIMPLE_SPECS.strip()}")
    
    v0_api_key = os.getenv('V0_API_KEY')
    if not v0_api_key:
        print("❌ V0_API_KEY not found in environment")
        return None
    
    print(f"🔑 API Key found: {v0_api_key[:10]}...")
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "v0-1.5-md",
                "messages": [
                    {
                        "role": "user",
                        "content": SIMPLE_SPECS.strip()
                    }
                ],
                "max_completion_tokens": 8000
            }
            
            headers = {
                'Authorization': f'Bearer {v0_api_key}',
                'Content-Type': 'application/json'
            }
            
            print("🌐 Making V0 API call...")
            async with session.post(
                'https://api.v0.dev/v1/chat/completions',
                json=payload,
                headers=headers,
                timeout=30
            ) as response:
                print(f"📊 Response status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    generated_code = result["choices"][0]["message"]["content"]
                    print(f"✅ Success! Response length: {len(generated_code)} chars")
                    print("📋 First 200 chars:")
                    print(generated_code[:200])
                    return generated_code
                else:
                    error_text = await response.text()
                    print(f"❌ API Error {response.status}: {error_text}")
                    return None
                    
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

async def main():
    """Run simple V0 test."""
    print("🚀 Simple V0 API Test")
    print("=" * 30)
    
    result = await test_v0_simple()
    
    if result:
        print("\n🎉 V0 API is working!")
    else:
        print("\n❌ V0 API test failed")

if __name__ == "__main__":
    asyncio.run(main())
