#!/usr/bin/env python3
"""
Test spec extraction from Notion
"""

import asyncio
from browser_testing_agent import BrowserTestingAgent

async def test_spec_extraction():
    """Test extracting specs from Notion"""
    
    print("🔍 Testing spec extraction from Notion...")
    
    agent = BrowserTestingAgent()
    specs = await agent.get_original_specs()
    
    print("\n" + "="*50)
    print("📋 EXTRACTED SPECS")
    print("="*50)
    print(specs[:500] + "..." if len(specs) > 500 else specs)
    print("="*50)
    
    return len(specs) > 0

if __name__ == "__main__":
    asyncio.run(test_spec_extraction())
