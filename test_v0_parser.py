#!/usr/bin/env python3
"""
Test V0 Parser with Debug File
==============================
"""

import re
import os
import shutil

def parse_v0_response(content: str, project_dir: str = "pixelpilot-v0-test"):
    """Parse V0 response and extract files."""
    
    # Clean directory
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    os.makedirs(project_dir)
    
    # Split content into lines
    lines = content.split('\n')
    current_file = None
    current_content = []
    files_saved = 0
    in_code_block = False
    
    for i, line in enumerate(lines):
        # Skip thinking blocks
        if '<Thinking>' in line or '</Thinking>' in line:
            continue
            
        # Look for code block start with file attribute
        if line.startswith('```') and 'file=' in line:
            # Save previous file if exists
            if current_file and current_content:
                save_file(project_dir, current_file, '\n'.join(current_content))
                files_saved += 1
                print(f"  ✅ {current_file}")
            
            # Extract filename
            match = re.search(r'file="([^"]+)"', line)
            if match:
                current_file = match.group(1)
                current_content = []
                in_code_block = True
                continue
        
        # Look for code block end
        elif line.startswith('```') and in_code_block:
            # Save current file
            if current_file and current_content:
                save_file(project_dir, current_file, '\n'.join(current_content))
                files_saved += 1
                print(f"  ✅ {current_file}")
            
            current_file = None
            current_content = []
            in_code_block = False
            
        # Collect content inside code blocks
        elif in_code_block and current_file:
            current_content.append(line)
    
    # Save last file if exists
    if current_file and current_content:
        save_file(project_dir, current_file, '\n'.join(current_content))
        files_saved += 1
        print(f"  ✅ {current_file}")
    
    print(f"\n✅ Parsed {files_saved} files from V0 response")
    return files_saved

def save_file(project_dir: str, filepath: str, content: str):
    """Save file with directory structure."""
    full_path = os.path.join(project_dir, filepath)
    
    # Create directories if needed
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Save file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())

def main():
    """Test parser with saved V0 response."""
    print("🔍 Testing V0 Parser with Debug File")
    print("=" * 40)
    
    # Read the debug file
    with open('v0_response_debug.txt', 'r') as f:
        content = f.read()
    
    print(f"📄 Content length: {len(content)} characters")
    
    # Parse and save files
    files_saved = parse_v0_response(content)
    
    if files_saved > 0:
        print(f"\n🎉 Successfully parsed V0 response!")
        print("📋 Next steps:")
        print("  1. cd pixelpilot-v0-test")
        print("  2. npm install")
        print("  3. npm run dev")
    else:
        print("❌ Failed to parse V0 response")

if __name__ == "__main__":
    main()
