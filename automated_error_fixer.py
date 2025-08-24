#!/usr/bin/env python3
"""
Automated Error Detection and Fixing System
==========================================

Detects common Next.js errors and applies automatic fixes.
"""

import re
import os
import json
from typing import List, Dict, Tuple

class NextJSErrorFixer:
    """Automated error detection and fixing for Next.js projects."""
    
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.fixes_applied = []
    
    def detect_and_fix_all_errors(self) -> List[str]:
        """Run all error detection and fixes."""
        print("🔍 Scanning for common Next.js errors...")
        
        # Fix 1: Image hostname configuration
        self.fix_image_hostname_errors()
        
        # Fix 2: Turbopack compatibility
        self.fix_turbopack_errors()
        
        # Fix 3: Client Component boundaries
        self.fix_client_component_errors()
        
        # Fix 4: Package.json issues
        self.fix_package_json_issues()
        
        return self.fixes_applied
    
    def fix_image_hostname_errors(self):
        """Fix Next.js image hostname configuration."""
        next_config_path = os.path.join(self.project_dir, 'next.config.js')
        
        if not os.path.exists(next_config_path):
            return
        
        with open(next_config_path, 'r') as f:
            content = f.read()
        
        # Check if images config exists
        if 'images:' not in content and 'unsplash.com' in self.get_all_file_contents():
            print("  🔧 Adding Unsplash image configuration...")
            
            # Insert images config
            if 'const nextConfig = {' in content:
                content = content.replace(
                    'const nextConfig = {',
                    '''const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        port: '',
        pathname: '/**',
      },
    ],
  },'''
                )
                
                with open(next_config_path, 'w') as f:
                    f.write(content)
                
                self.fixes_applied.append("Fixed Next.js image hostname configuration")
    
    def fix_turbopack_errors(self):
        """Fix turbopack compatibility issues."""
        package_json_path = os.path.join(self.project_dir, 'package.json')
        
        if not os.path.exists(package_json_path):
            return
        
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        # Remove --turbopack flag if present
        if 'scripts' in package_data and 'dev' in package_data['scripts']:
            dev_script = package_data['scripts']['dev']
            if '--turbopack' in dev_script:
                print("  🔧 Removing incompatible --turbopack flag...")
                package_data['scripts']['dev'] = dev_script.replace(' --turbopack', '')
                
                with open(package_json_path, 'w') as f:
                    json.dump(package_data, f, indent=2)
                
                self.fixes_applied.append("Removed incompatible --turbopack flag")
    
    def fix_client_component_errors(self):
        """Fix Server/Client Component boundary issues."""
        # Scan all .tsx files for common patterns
        for root, dirs, files in os.walk(self.project_dir):
            for file in files:
                if file.endswith('.tsx'):
                    file_path = os.path.join(root, file)
                    self.fix_client_component_in_file(file_path)
    
    def fix_client_component_in_file(self, file_path: str):
        """Fix Client Component issues in a specific file."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Server Component passing functions to Client Component
        if 'onLikeChange=' in content and "'use client'" not in content:
            # This is likely a server component passing functions
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'onLikeChange=' in line:
                    # Remove the problematic prop
                    lines[i] = re.sub(r'\s*onLikeChange=\{[^}]+\}', '', line)
            
            content = '\n'.join(lines)
        
        # Save if changed
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            
            relative_path = os.path.relpath(file_path, self.project_dir)
            self.fixes_applied.append(f"Fixed Client Component boundaries in {relative_path}")
    
    def fix_package_json_issues(self):
        """Fix common package.json issues."""
        package_json_path = os.path.join(self.project_dir, 'package.json')
        
        if not os.path.exists(package_json_path):
            return
        
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        changed = False
        
        # Ensure required dependencies
        required_deps = {
            "next": "^14.0.0",
            "react": "^18.0.0", 
            "react-dom": "^18.0.0"
        }
        
        if 'dependencies' not in package_data:
            package_data['dependencies'] = {}
        
        for dep, version in required_deps.items():
            if dep not in package_data['dependencies']:
                package_data['dependencies'][dep] = version
                changed = True
        
        if changed:
            with open(package_json_path, 'w') as f:
                json.dump(package_data, f, indent=2)
            
            self.fixes_applied.append("Added missing dependencies to package.json")
    
    def get_all_file_contents(self) -> str:
        """Get concatenated content of all project files."""
        all_content = ""
        
        for root, dirs, files in os.walk(self.project_dir):
            # Skip node_modules and .next
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.next', '.git']]
            
            for file in files:
                if file.endswith(('.tsx', '.ts', '.js', '.jsx')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            all_content += f.read() + "\n"
                    except:
                        pass
        
        return all_content

def auto_fix_project(project_dir: str) -> List[str]:
    """Auto-fix common errors in a Next.js project."""
    print(f"🔧 Auto-fixing errors in {project_dir}...")
    
    fixer = NextJSErrorFixer(project_dir)
    fixes = fixer.detect_and_fix_all_errors()
    
    if fixes:
        print("✅ Applied fixes:")
        for fix in fixes:
            print(f"  • {fix}")
    else:
        print("✅ No common errors detected")
    
    return fixes

if __name__ == "__main__":
    # Test on both projects
    print("🔧 Testing Automated Error Fixer")
    print("=" * 40)
    
    # Fix Claude project
    claude_fixes = auto_fix_project("pixelpilot-nextjs")
    
    print()
    
    # Fix V0 project  
    v0_fixes = auto_fix_project("pixelpilot-v0-test")
    
    print(f"\n📊 Summary:")
    print(f"  Claude project: {len(claude_fixes)} fixes")
    print(f"  V0 project: {len(v0_fixes)} fixes")
