#!/usr/bin/env python3
"""
Debug V0 Full Response - Save to File
====================================
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def save_v0_full_response():
    """Save full V0 response to file for analysis."""
    
    prompt = """
Create a complete Next.js 14 TypeScript project with a ProfileCard component.

Requirements:
- package.json with dependencies
- next.config.js
- tailwind.config.js
- app/page.tsx
- components/ProfileCard.tsx

Keep it simple but complete.
"""
    
    api_key = os.getenv("V0_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "v0-1.5-md",
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": 8000
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
                
                # Save to file for analysis
                with open('v0_response_debug.txt', 'w') as f:
                    f.write(content)
                
                print(f"✅ Saved V0 response to v0_response_debug.txt ({len(content)} chars)")
                
                # Quick analysis
                lines = content.split('\n')
                file_patterns = []
                for i, line in enumerate(lines):
                    if 'file=' in line and '```' in line:
                        file_patterns.append(f"Line {i}: {line}")
                
                print(f"\n📄 Found {len(file_patterns)} file patterns:")
                for pattern in file_patterns:
                    print(f"  {pattern}")
                
                return content
            else:
                print(f"❌ Error: {response.status}")
                return None

if __name__ == "__main__":
    asyncio.run(save_v0_full_response())
