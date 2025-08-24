#!/usr/bin/env python3
"""
Test script to capture and analyze V0 API response format
"""

import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def test_v0_response():
    """Test V0 API and save raw response for analysis"""
    
    api_key = os.getenv("V0_API_KEY")
    if not api_key:
        print("❌ V0_API_KEY not found in environment")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "v0-1.5-md",
        "messages": [
            {
                "role": "user", 
                "content": "Create a simple Next.js component with package.json"
            }
        ],
        "max_completion_tokens": 4000
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.v0.dev/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        content = response_data['choices'][0]['message']['content']
                        
                        # Save raw response
                        with open('v0_raw_response.txt', 'w') as f:
                            f.write(content)
                        
                        print(f"✅ Saved raw V0 response ({len(content)} chars) to v0_raw_response.txt")
                        print("\n📋 First 2000 characters:")
                        print("=" * 50)
                        print(content[:2000])
                        print("=" * 50)
                        
                        # Analyze patterns
                        lines = content.split('\n')
                        print(f"\n🔍 Pattern Analysis ({len(lines)} lines):")
                        
                        file_patterns = []
                        for i, line in enumerate(lines[:200]):
                            if any(keyword in line.lower() for keyword in ['package.json', '.tsx', '.js', '.css', 'file']):
                                file_patterns.append(f"Line {i}: {line[:100]}")
                        
                        print(f"Found {len(file_patterns)} potential file patterns:")
                        for pattern in file_patterns[:20]:
                            print(pattern)
                        
                        return content
                    else:
                        print("❌ No content in response")
                        return None
                else:
                    error = await response.text()
                    print(f"❌ API Error: {response.status} - {error}")
                    return None
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_v0_response())
