#!/usr/bin/env python3
"""
Test subprocess string escaping to fix Agent 3
"""

import subprocess

def test_subprocess_escaping():
    """Test different escaping approaches"""
    
    test_content = "Line 1\nLine 2\nLine 3"
    
    print("🔍 Testing subprocess string escaping...")
    print(f"Original content: {repr(test_content)}")
    
    # Test 1: Single backslash (what we had)
    result1 = subprocess.run([
        "python", "-c", f"""
test_content = '''{test_content}'''
lines = test_content.split('\\n')
print(f"Single backslash result: {{len(lines)}} lines")
for i, line in enumerate(lines):
    print(f"  {{i}}: {{repr(line)}}")
"""
    ], capture_output=True, text=True)
    
    print("Result 1 (single backslash):")
    print(result1.stdout)
    
    # Test 2: Double backslash (current Agent 3)
    result2 = subprocess.run([
        "python", "-c", f"""
test_content = '''{test_content}'''
lines = test_content.split('\\\\n')
print(f"Double backslash result: {{len(lines)}} lines")
for i, line in enumerate(lines):
    print(f"  {{i}}: {{repr(line)}}")
"""
    ], capture_output=True, text=True)
    
    print("Result 2 (double backslash):")
    print(result2.stdout)
    
    # Test 3: Using splitlines() method
    result3 = subprocess.run([
        "python", "-c", f"""
test_content = '''{test_content}'''
lines = test_content.splitlines()
print(f"splitlines() result: {{len(lines)}} lines")
for i, line in enumerate(lines):
    print(f"  {{i}}: {{repr(line)}}")
"""
    ], capture_output=True, text=True)
    
    print("Result 3 (splitlines method):")
    print(result3.stdout)

if __name__ == "__main__":
    test_subprocess_escaping()
