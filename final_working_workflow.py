#!/usr/bin/env python3
"""
Final Working PixelPilot Workflow
=================================

Complete automated workflow using ONLY tested working components:
1. ✅ Notion specs extraction (step1_test_notion_extraction.py)
2. ✅ V0 code generation (step2_test_v0_generation.py) 
3. ✅ Automated error fixing (automated_error_fixer.py)
4. ✅ npm install & dev server testing
5. 🔄 Vercel deployment (optional)

NO Dedalus - V0 is better for frontend generation.
"""

import asyncio
import os
import subprocess
import shutil
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import aiohttp

# Import working components
from step1_test_notion_extraction import test_notion_extraction
from automated_error_fixer import auto_fix_project

load_dotenv()

class FinalPixelPilotWorkflow:
    """Complete working PixelPilot workflow using tested components."""
    
    def __init__(self):
        self.project_dir = None
        
    async def run_workflow(self, project_name: str = "pixelpilot-final") -> Dict[str, Any]:
        """Run complete workflow with only working components."""
        print("🚀 Final PixelPilot Workflow - Using Only Working Components")
        print("=" * 60)
        
        results = {
            "success": False,
            "steps": [],
            "errors": [],
            "project_dir": None,
            "files_generated": 0,
            "fixes_applied": []
        }
        
        try:
            # Step 1: Extract specs from Notion ✅ TESTED WORKING
            print("\n📖 Step 1: Extracting specs from Notion...")
            specs = await test_notion_extraction()
            if not specs:
                results["errors"].append("Notion extraction failed")
                return results
            
            results["steps"].append("notion_extraction")
            print(f"✅ Extracted {len(specs)} characters")
            
            # Step 2: Generate code with V0 ✅ TESTED WORKING
            print("\n🤖 Step 2: Generating code with V0...")
            generated_code = await self.generate_with_v0(specs)
            if not generated_code:
                results["errors"].append("V0 code generation failed")
                return results
            
            results["steps"].append("v0_generation")
            print(f"✅ Generated {len(generated_code)} characters")
            
            # Step 3: Save project files ✅ TESTED WORKING
            print("\n💾 Step 3: Saving project files...")
            files_saved = await self.save_project(generated_code, project_name)
            if files_saved == 0:
                results["errors"].append("Failed to save project files")
                return results
            
            results["steps"].append("file_saving")
            results["project_dir"] = self.project_dir
            results["files_generated"] = files_saved
            print(f"✅ Saved {files_saved} files to {self.project_dir}")
            
            # Step 4: Auto-fix errors ✅ TESTED WORKING
            print("\n🔧 Step 4: Auto-fixing common errors...")
            fixes = auto_fix_project(self.project_dir)
            results["fixes_applied"] = fixes
            results["steps"].append("error_fixing")
            print(f"✅ Applied {len(fixes)} fixes")
            
            # Step 5: Install dependencies ✅ TESTED WORKING
            print("\n📦 Step 5: Installing dependencies...")
            if not await self.install_deps():
                results["errors"].append("npm install failed")
                return results
            
            results["steps"].append("npm_install")
            print("✅ Dependencies installed")
            
            # Step 6: Test dev server ✅ TESTED WORKING
            print("\n🌐 Step 6: Testing development server...")
            if not await self.test_dev_server():
                results["errors"].append("Dev server test failed")
                return results
            
            results["steps"].append("dev_server_test")
            print("✅ Development server working")
            
            results["success"] = True
            print("\n🎉 Complete workflow successful!")
            
        except Exception as e:
            results["errors"].append(f"Unexpected error: {str(e)}")
            print(f"❌ Workflow failed: {e}")
        
        return results
    
    async def generate_with_v0(self, specs: str) -> Optional[str]:
        """Generate code using V0 API - TESTED WORKING."""
        try:
            api_key = os.getenv("V0_API_KEY")
            if not api_key:
                print("❌ V0_API_KEY not found")
                return None
            
            prompt = f"""
Create a complete Next.js 14 TypeScript project based on these specifications:

{specs}

Requirements:
- Complete Next.js 14 with TypeScript
- Tailwind CSS matching the design specs
- Responsive and accessible
- Production-ready code
- Proper App Router patterns

Generate ALL files including package.json, next.config.js, components, etc.
"""
            
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
                        return result["choices"][0]["message"]["content"]
                    else:
                        print(f"❌ V0 API error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"❌ V0 generation error: {e}")
            return None
    
    async def save_project(self, generated_code: str, project_name: str) -> int:
        """Save V0 generated files - TESTED WORKING."""
        try:
            self.project_dir = os.path.abspath(project_name)
            
            # Clean directory
            if os.path.exists(self.project_dir):
                shutil.rmtree(self.project_dir)
            os.makedirs(self.project_dir)
            
            # Parse V0 format: ```tsx file="filename"
            lines = generated_code.split('\n')
            current_file = None
            current_content = []
            files_saved = 0
            in_code_block = False
            
            for line in lines:
                # Skip thinking blocks
                if '<Thinking>' in line or '</Thinking>' in line:
                    continue
                
                # Look for file pattern
                if line.startswith('```') and 'file=' in line:
                    # Save previous file
                    if current_file and current_content:
                        self._save_file(current_file, '\n'.join(current_content))
                        files_saved += 1
                    
                    # Extract filename
                    match = re.search(r'file="([^"]+)"', line)
                    if match:
                        current_file = match.group(1)
                        current_content = []
                        in_code_block = True
                        continue
                
                # End of code block
                elif line.startswith('```') and in_code_block:
                    if current_file and current_content:
                        self._save_file(current_file, '\n'.join(current_content))
                        files_saved += 1
                    current_file = None
                    current_content = []
                    in_code_block = False
                
                # Collect content
                elif in_code_block and current_file:
                    current_content.append(line)
            
            # Save last file
            if current_file and current_content:
                self._save_file(current_file, '\n'.join(current_content))
                files_saved += 1
            
            return files_saved
            
        except Exception as e:
            print(f"❌ Save project error: {e}")
            return 0
    
    def _save_file(self, filepath: str, content: str):
        """Save individual file with directory structure."""
        full_path = os.path.join(self.project_dir, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
    
    async def install_deps(self) -> bool:
        """Install npm dependencies - TESTED WORKING."""
        try:
            process = await asyncio.create_subprocess_exec(
                "npm", "install",
                cwd=self.project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            return process.returncode == 0
            
        except Exception as e:
            print(f"❌ npm install error: {e}")
            return False
    
    async def test_dev_server(self) -> bool:
        """Test dev server starts - TESTED WORKING."""
        try:
            # Start dev server
            process = await asyncio.create_subprocess_exec(
                "npm", "run", "dev",
                cwd=self.project_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for startup
            await asyncio.sleep(3)
            
            # Check if running
            if process.returncode is None:
                process.terminate()
                await process.wait()
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Dev server test error: {e}")
            return False

async def main():
    """Run the final working workflow."""
    workflow = FinalPixelPilotWorkflow()
    results = await workflow.run_workflow("pixelpilot-final")
    
    print("\n📊 Final Results:")
    print("=" * 30)
    print(f"✅ Success: {results['success']}")
    print(f"📋 Steps completed: {len(results['steps'])}")
    
    for step in results['steps']:
        print(f"  • {step}")
    
    if results['fixes_applied']:
        print(f"🔧 Auto-fixes applied: {len(results['fixes_applied'])}")
        for fix in results['fixes_applied']:
            print(f"  • {fix}")
    
    if results['errors']:
        print(f"❌ Errors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  • {error}")
    
    if results['project_dir']:
        print(f"📁 Project: {results['project_dir']}")
        print(f"📄 Files: {results['files_generated']}")
        print("\n🚀 To run the project:")
        print(f"  cd {results['project_dir']}")
        print("  npm run dev")

if __name__ == "__main__":
    asyncio.run(main())
