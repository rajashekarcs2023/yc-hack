#!/usr/bin/env python3
"""
Step 2: Simple Code Generation Test
==================================

Test generating Next.js project using Claude API with pre-extracted specs.
"""

import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pre-extracted specs from Step 1 (to avoid MCP conflicts)
PROFILE_CARD_SPECS = """
# 📄 Profile Card Component Spec
**Component Name**
Profile Card
**Description**
A reusable card component that displays a user's profile picture, name, short bio, and an interactive "Like" button.
---
## 🎨 Design Tokens
- **Card Background:** `#ffffff`
- **Border Radius:** `12px`
- **Shadow:** `sm` (equivalent to Tailwind `shadow-sm`)
- **Font Family:** Inter, sans-serif
- **Font Size (Name):** `16px`
- **Font Weight (Name):** `600`
- **Font Size (Bio):** `14px`
- **Font Weight (Bio):** `400`
- **Text Color (Name):** `#1f2937` (gray-800)
- **Text Color (Bio):** `#6b7280` (gray-500)
- **Button Background (Default):** `#3b82f6` (blue-500)
- **Button Background (Hover):** `#2563eb` (blue-600)
- **Button Text Color:** `#ffffff`
- **Like Count Color:** `#ef4444` (red-500)
---
## 📐 Layout & Spacing
- **Card Width:** `320px`
- **Card Padding:** `24px`
- **Avatar Size:** `80px`
- **Avatar Border Radius:** `50%` (circular)
- **Spacing between Avatar and Name:** `16px`
- **Spacing between Name and Bio:** `8px`
- **Spacing between Bio and Button:** `20px`
- **Button Height:** `40px`
- **Button Padding:** `12px 24px`
- **Button Border Radius:** `8px`
---
## 🎯 Interactive States
### Like Button States
1. **Default State**
   - Background: Blue (`#3b82f6`)
   - Text: "Like"
   - Icon: Heart outline
2. **Hover State**
   - Background: Darker blue (`#2563eb`)
   - Slight scale transform (1.02x)
3. **Liked State**
   - Background: Red (`#ef4444`)
   - Text: "Liked"
   - Icon: Filled heart
   - Like count increases by 1
4. **Liked Hover State**
   - Background: Darker red (`#dc2626`)
---
## 📱 Responsive Behavior
- **Mobile (< 640px):** Card width adjusts to `calc(100vw - 32px)` with max-width `320px`
- **Tablet & Desktop:** Fixed width `320px`
- **Avatar:** Scales down to `64px` on mobile
- **Text:** Font sizes remain consistent across devices
---
## ♿ Accessibility Requirements
- **ARIA Labels:** Button has `aria-label` describing current state
- **Keyboard Navigation:** Button is focusable and activatable with Enter/Space
- **Screen Reader:** Like count changes are announced
- **Color Contrast:** All text meets WCAG 2.1 AA standards
- **Focus Indicators:** Clear focus outline on interactive elements
---
## 🧩 Component Props (TypeScript)
```typescript
interface ProfileCardProps {
  name: string;
  bio: string;
  avatarUrl: string;
  initialLikeCount?: number;
  onLikeChange?: (isLiked: boolean, newCount: number) => void;
}
```
---
## 📋 Implementation Notes
- Use React hooks for like state management
- Implement smooth transitions for hover effects
- Ensure proper TypeScript typing
- Include proper error handling for missing props
- Add loading state for avatar images
- Implement proper semantic HTML structure
"""

async def test_claude_code_generation():
    """Test generating Next.js project with Claude API directly."""
    print("🤖 Step 2: Testing Code Generation with Claude")
    print("=" * 50)
    
    print(f"📋 Using pre-extracted specs ({len(PROFILE_CARD_SPECS)} chars)")
    
    # Create Next.js generation prompt
    prompt = f"""
Generate a complete Next.js 14 TypeScript project based on these specifications:

{PROFILE_CARD_SPECS}

GENERATE ALL FILES with complete, production-ready code:

1. **package.json** - Include all dependencies (Next.js 14, React 18, TypeScript, Tailwind CSS, etc.)
2. **next.config.js** - Next.js configuration
3. **tailwind.config.js** - Tailwind configuration with custom theme
4. **tsconfig.json** - TypeScript configuration
5. **app/layout.tsx** - Root layout with metadata
6. **app/page.tsx** - Home page showcasing the Profile Card
7. **app/globals.css** - Global styles and Tailwind imports
8. **components/ProfileCard.tsx** - Main Profile Card component
9. **components/ui/Button.tsx** - Reusable Button component
10. **components/ui/Avatar.tsx** - Avatar component
11. **lib/utils.ts** - Utility functions (cn function for class merging)
12. **types/index.ts** - TypeScript type definitions

Requirements:
- Complete, runnable Next.js 14 project with TypeScript
- Tailwind CSS with custom design system matching the specs
- Responsive design (mobile-first)
- Accessibility compliant (WCAG 2.1 AA)
- Professional, modern design
- All files must have complete, working code

Format your response with clear file separators like:
## filename.ext
```language
[complete file content]
```

Make this immediately deployable to Vercel.
"""

    # Test with Claude API (using Anthropic)
    try:
        print("🧠 Generating code with Claude...")
        
        # Use Anthropic API directly
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ANTHROPIC_API_KEY not found in environment")
            return None
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 8000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    generated_code = result["content"][0]["text"]
                    
                    print("✅ Code generated successfully!")
                    print(f"📄 Generated content length: {len(generated_code)} characters")
                    print("\n📋 First 500 characters:")
                    print("-" * 30)
                    print(generated_code[:500] + "..." if len(generated_code) > 500 else generated_code)
                    print("-" * 30)
                    
                    return generated_code
                else:
                    error_text = await response.text()
                    print(f"❌ Claude API error: {response.status} - {error_text}")
                    return None
                    
    except Exception as e:
        print(f"❌ Error generating code: {e}")
        return None

def save_generated_project(generated_code: str, project_dir: str = "pixelpilot-nextjs") -> bool:
    """Parse generated code and save to project directory."""
    print(f"💾 Saving generated project to {project_dir}/...")
    
    try:
        import os
        import shutil
        
        # Clean directory
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        os.makedirs(project_dir)
        
        # Parse files from generated code
        lines = generated_code.split('\n')
        current_file = None
        current_content = []
        files_saved = 0
        in_code_block = False
        
        for line in lines:
            # Look for file headers (## filename.ext)
            if line.startswith('##') and ('.' in line or 'package.json' in line):
                # Save previous file
                if current_file and current_content:
                    save_file(project_dir, current_file, '\n'.join(current_content))
                    files_saved += 1
                
                # Extract filename
                current_file = line.replace('##', '').strip()
                current_content = []
                in_code_block = False
                
            # Look for code blocks
            elif line.startswith('```') and current_file:
                if not in_code_block:
                    # Opening code block
                    in_code_block = True
                    continue
                else:
                    # Closing code block - save file
                    save_file(project_dir, current_file, '\n'.join(current_content))
                    files_saved += 1
                    current_file = None
                    current_content = []
                    in_code_block = False
                    
            elif current_file and in_code_block:
                current_content.append(line)
        
        # Save last file if exists
        if current_file and current_content:
            save_file(project_dir, current_file, '\n'.join(current_content))
            files_saved += 1
        
        print(f"✅ Saved {files_saved} files to {project_dir}/")
        
        # Show project structure
        show_project_structure(project_dir)
        
        return files_saved > 0
        
    except Exception as e:
        print(f"❌ Error saving project: {e}")
        return False

def save_file(project_dir: str, filepath: str, content: str):
    """Save individual file with directory structure."""
    full_path = os.path.join(project_dir, filepath)
    
    # Create directories if needed
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Save file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    print(f"  ✅ {filepath}")

def show_project_structure(project_dir: str):
    """Display the project structure."""
    print(f"\n📋 Project Structure:")
    print("=" * 30)
    
    for root, dirs, files in os.walk(project_dir):
        level = root.replace(project_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            print(f"{subindent}{file} ({size} bytes)")

async def main():
    """Test code generation workflow."""
    generated_code = await test_claude_code_generation()
    
    if generated_code:
        # Save project
        success = save_generated_project(generated_code)
        
        if success:
            print("\n🎉 Step 2 Complete: Next.js project generated!")
            print("📋 Next steps:")
            print("  1. cd pixelpilot-nextjs")
            print("  2. npm install")
            print("  3. npm run dev")
        else:
            print("❌ Failed to save project files")
    else:
        print("❌ Step 2 Failed: Could not generate code")

if __name__ == "__main__":
    asyncio.run(main())
