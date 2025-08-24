#!/usr/bin/env python3
"""
Debug V0 Response Format
=======================
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_v0_response():
    """Debug V0 response format to understand structure."""
    
    prompt = "Create a simple Next.js component with a button"
    
    api_key = os.getenv("V0_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "v0-1.5-md",
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": 2000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.v0.dev/v1/chat/completions",
            headers=headers,
            json=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                content = result["choices"][0]["message"]["content"]
                
                print("🔍 V0 Response Analysis:")
                print("=" * 50)
                print(f"Length: {len(content)} chars")
                print("\n📋 First 1000 characters:")
                print("-" * 30)
                print(content[:1000])
                print("-" * 30)
                
                # Look for file patterns
                lines = content.split('\n')
                print(f"\n📄 Line Analysis (first 20 lines):")
                for i, line in enumerate(lines[:20]):
                    if any(pattern in line.lower() for pattern in ['package.json', '.tsx', '.ts', '.js', '.css', 'next.config']):
                        print(f"  {i:2d}: 🎯 {line}")
                    elif line.startswith('```'):
                        print(f"  {i:2d}: 📝 {line}")
                    elif line.startswith('#') or line.startswith('**'):
                        print(f"  {i:2d}: 📋 {line}")
                    else:
                        print(f"  {i:2d}: {line[:50]}...")
                
                return content
            else:
                print(f"❌ Error: {response.status}")
                return None

if __name__ == "__main__":
    asyncio.run(debug_v0_response())
