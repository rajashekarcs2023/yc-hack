#!/usr/bin/env python3
"""
PixelPilot Dedalus Agent - Reads Notion specs and generates frontend code
"""

import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from dedalus_notion_tool import fetch_notion_page_for_dedalus

load_dotenv()

async def generate_frontend_from_specs():
    """Generate frontend code based on PixelPilot specifications from Notion."""
    
    print("🚀 PixelPilot Frontend Generator")
    print("=" * 50)
    
    # Step 1: Read the PixelPilot specification from Notion
    print("\n📖 Step 1: Reading PixelPilot specification from Notion...")
    pixelpilot_page_id = "258bd31b-99b8-80b3-9a92-ffbbadb0b85f"
    
    try:
        specs = await fetch_notion_page_for_dedalus(pixelpilot_page_id)
        print("✅ Successfully retrieved specifications")
        print(f"Specs preview: {specs[:200]}...")
    except Exception as e:
        print(f"❌ Failed to read specs: {e}")
        return
    
    # Step 2: Use Dedalus to generate frontend code
    print("\n⚙️ Step 2: Generating frontend code with Dedalus...")
    
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    prompt = f"""
You are a frontend developer tasked with creating a React component based on the following specification:

{specs}

Please generate:
1. A complete React component (ProfileCard.jsx) that implements all the requirements
2. A CSS module file (ProfileCard.module.css) with all the design tokens
3. A demo page (App.jsx) that shows the component in action
4. A package.json with all necessary dependencies
5. A README.md with setup instructions

Requirements:
- Use React with hooks
- Use CSS modules for styling
- Implement responsive design with the specified breakpoints
- Include proper accessibility features
- Add the like functionality with state management
- Use Tailwind CSS for additional utilities if needed
- Make it production-ready and well-documented

Generate complete, runnable code that can be deployed immediately.
"""

    try:
        result = await runner.run(
            input=prompt,
            model="openai/gpt-4o",
            stream=False
        )
        
        print("✅ Frontend code generated successfully!")
        print("\n📝 Generated Code:")
        print("-" * 50)
        print(result.final_output)
        
        # Save the generated code to files
        await save_generated_code(result.final_output)
        
        return result.final_output
        
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return None

async def save_generated_code(generated_code):
    """Save the generated code to appropriate files."""
    print("\n💾 Step 3: Saving generated code to files...")
    
    # Create a project directory
    import os
    project_dir = "/Users/radhikadanda/yc-hack/pixelpilot-frontend"
    os.makedirs(project_dir, exist_ok=True)
    
    # Save the full output for now - we can parse it later
    with open(f"{project_dir}/generated_code.md", "w") as f:
        f.write(generated_code)
    
    print(f"✅ Code saved to {project_dir}/generated_code.md")
    print("📁 Next: Parse and create individual files for the React project")

if __name__ == "__main__":
    asyncio.run(generate_frontend_from_specs())
