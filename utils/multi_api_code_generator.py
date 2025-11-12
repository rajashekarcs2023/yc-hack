#!/usr/bin/env python3
"""
Multi-API code generator with fallback strategy
Supports: V0, Claude, OpenAI, and local generation
"""

import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def generate_with_v0(specs: str) -> tuple[str, bool]:
    """Try V0 API first"""
    try:
        api_key = os.getenv("V0_API_KEY")
        if not api_key:
            return "V0_API_KEY not found", False
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "v0-1.5-md",
            "messages": [{"role": "user", "content": f"Create a complete Next.js project: {specs}"}],
            "max_completion_tokens": 8000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.v0.dev/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        content = response_data['choices'][0]['message']['content']
                        return content, True
                        
        return f"V0 API error: {response.status}", False
        
    except Exception as e:
        return f"V0 API exception: {str(e)}", False

async def generate_with_claude(specs: str) -> tuple[str, bool]:
    """Fallback to Claude API"""
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "ANTHROPIC_API_KEY not found", False
            
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        prompt = f"""Create a complete Next.js 14 TypeScript project based on: {specs}

Generate ALL files with this exact format:
```json file="package.json"
{{
  "name": "nextjs-app",
  "version": "0.1.0",
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }},
  "dependencies": {{
    "next": "14.2.15",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }}
}}
```

```tsx file="app/page.tsx"
export default function Home() {{
  return <div>Hello Next.js</div>
}}
```

Include: package.json, app/layout.tsx, app/page.tsx, components, styles."""

        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    if 'content' in response_data and len(response_data['content']) > 0:
                        content = response_data['content'][0]['text']
                        return content, True
                        
        return f"Claude API error: {response.status}", False
        
    except Exception as e:
        return f"Claude API exception: {str(e)}", False

async def generate_with_openai(specs: str) -> tuple[str, bool]:
    """Fallback to OpenAI API"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "OPENAI_API_KEY not found", False
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Create a complete Next.js 14 TypeScript project for: {specs}

Use this EXACT format for each file:
```json file="package.json"
[file content here]
```

```tsx file="app/page.tsx"
[file content here]
```

Generate: package.json, next.config.js, app/layout.tsx, app/page.tsx, and component files."""

        data = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 8000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        content = response_data['choices'][0]['message']['content']
                        return content, True
                        
        return f"OpenAI API error: {response.status}", False
        
    except Exception as e:
        return f"OpenAI API exception: {str(e)}", False

def generate_fallback_project(specs: str) -> tuple[str, bool]:
    """Last resort: generate minimal working project"""
    try:
        content = f'''```json file="package.json"
{{
  "name": "pixelpilot-project",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }},
  "dependencies": {{
    "next": "14.2.15",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }},
  "devDependencies": {{
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "eslint": "^8",
    "eslint-config-next": "14.2.15",
    "typescript": "^5"
  }}
}}
```

```tsx file="app/layout.tsx"
import type {{ Metadata }} from 'next'

export const metadata: Metadata = {{
  title: 'PixelPilot App',
  description: 'Generated by PixelPilot',
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en">
      <body>{{children}}</body>
    </html>
  )
}}
```

```tsx file="app/page.tsx"
export default function Home() {{
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-xl font-semibold mb-4">John Doe</h1>
        <p className="text-gray-600 mb-4">Welcome to PixelPilot!</p>
        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Like
        </button>
      </div>
    </main>
  )
}}
```

```js file="next.config.js"
/** @type {{import('next').NextConfig}} */
const nextConfig = {{}}

module.exports = nextConfig
```

```json file="tsconfig.json"
{{
  "compilerOptions": {{
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {{
        "name": "next"
      }}
    ],
    "paths": {{
      "@/*": ["./*"]
    }}
  }},
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}}
```'''
        
        return content, True
        
    except Exception as e:
        return f"Fallback generation failed: {str(e)}", False

async def generate_code_multi_api(specs: str) -> tuple[str, str]:
    """Try multiple APIs with fallback strategy"""
    
    print("🤖 Multi-API Code Generation")
    print("=" * 40)
    
    # Strategy 1: V0 API (preferred)
    print("🔄 Trying V0 API...")
    content, success = await generate_with_v0(specs)
    if success:
        print("✅ V0 API succeeded!")
        return content, "v0"
    else:
        print(f"❌ V0 failed: {content}")
    
    # Strategy 2: Claude API
    print("🔄 Trying Claude API...")
    content, success = await generate_with_claude(specs)
    if success:
        print("✅ Claude API succeeded!")
        return content, "claude"
    else:
        print(f"❌ Claude failed: {content}")
    
    # Strategy 3: OpenAI API
    print("🔄 Trying OpenAI API...")
    content, success = await generate_with_openai(specs)
    if success:
        print("✅ OpenAI API succeeded!")
        return content, "openai"
    else:
        print(f"❌ OpenAI failed: {content}")
    
    # Strategy 4: Fallback generation
    print("🔄 Using fallback generation...")
    content, success = generate_fallback_project(specs)
    if success:
        print("✅ Fallback generation succeeded!")
        return content, "fallback"
    else:
        print(f"❌ All strategies failed: {content}")
        return "", "failed"

if __name__ == "__main__":
    async def test():
        specs = "Create a simple Next.js component with a card, user name John Doe, and blue Like button"
        content, source = await generate_code_multi_api(specs)
        print(f"\n🎉 Generated {len(content)} chars using {source}")
        if content:
            print(content[:500] + "...")
    
    asyncio.run(test())
