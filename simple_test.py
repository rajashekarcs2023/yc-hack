#!/usr/bin/env python3
"""
Simple test to check what's happening with our setup.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def check_setup():
    """Check our current setup."""
    print("🔍 Checking setup...")
    
    # Check Notion token
    notion_token = os.getenv("NOTION_TOKEN")
    print(f"NOTION_TOKEN: {notion_token}")
    
    if not notion_token or notion_token == "your_notion_integration_token_here":
        print("❌ No valid Notion token found!")
        print("\nTo fix this:")
        print("1. Go to https://www.notion.so/profile/integrations")
        print("2. Create a new internal integration")
        print("3. Copy the integration token (starts with 'secret_')")
        print("4. Update NOTION_TOKEN in your .env file")
        print("5. Connect your integration to some pages in Notion")
        return False
    
    print("✅ Notion token found")
    
    # Check if npx is available
    import subprocess
    try:
        result = subprocess.run(["npx", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ npx is available")
        else:
            print("❌ npx not found")
            return False
    except FileNotFoundError:
        print("❌ npx not found - Node.js may not be installed")
        return False
    
    # Check if we can install the Notion MCP server
    try:
        print("🔄 Checking Notion MCP server availability...")
        result = subprocess.run(
            ["npx", "-y", "@notionhq/notion-mcp-server", "--help"], 
            capture_output=True, 
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✅ Notion MCP server is available")
        else:
            print(f"❌ Notion MCP server check failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ Notion MCP server check timed out")
        return False
    except Exception as e:
        print(f"❌ Error checking Notion MCP server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if check_setup():
        print("\n✅ Setup looks good! You can proceed with testing the MCP client.")
    else:
        print("\n❌ Setup issues found. Please fix them before proceeding.")
