#!/usr/bin/env python3
"""
Test Individual Subprocess Tools
================================

Test each subprocess tool individually before Dedalus orchestration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dedalus_subprocess_tools import (
    extract_notion_specs,
    generate_v0_code,
    save_project_files,
    fix_common_errors,
    install_dependencies,
    test_dev_server
)

def main():
    """Test all subprocess tools individually."""
    print("🧪 Testing Individual Subprocess Tools")
    print("=" * 40)
    
    # Test 1: Notion Extraction
    print("1️⃣ Testing Notion Extraction...")
    result1 = extract_notion_specs()
    print(f"   Result: {result1}")
    
    # Test 2: V0 Code Generation (with mock specs)
    print("\n2️⃣ Testing V0 Code Generation...")
    mock_specs = "Create a simple profile card component with name, bio, and like button"
    result2 = generate_v0_code(mock_specs)
    print(f"   Result: {result2}")
    
    # Test 3: Check Project Files
    print("\n3️⃣ Testing Project Files Check...")
    result3 = save_project_files("pixelpilot-v0-test")
    print(f"   Result: {result3}")
    
    # Test 4: Error Fixing
    print("\n4️⃣ Testing Error Fixing...")
    result4 = fix_common_errors("pixelpilot-v0-test")
    print(f"   Result: {result4}")
    
    # Test 5: NPM Install
    print("\n5️⃣ Testing NPM Install...")
    result5 = install_dependencies("pixelpilot-v0-test")
    print(f"   Result: {result5}")
    
    # Test 6: Dev Server
    print("\n6️⃣ Testing Dev Server...")
    result6 = test_dev_server("pixelpilot-v0-test")
    print(f"   Result: {result6}")
    
    print("\n" + "=" * 40)
    print("🎯 Individual Tool Testing Complete")
    
    # Count successes
    results = [result1, result2, result3, result4, result5, result6]
    successes = sum(1 for r in results if "SUCCESS" in r)
    
    print(f"✅ {successes}/{len(results)} tools working correctly")
    
    if successes == len(results):
        print("🚀 Ready for Dedalus orchestration!")
    else:
        print("⚠️  Fix individual tools before Dedalus orchestration")

if __name__ == "__main__":
    main()
