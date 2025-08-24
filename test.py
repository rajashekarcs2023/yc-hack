import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from dedalus_notion_tool import search_notion_for_dedalus, fetch_notion_page_for_dedalus, create_notion_page_for_dedalus

load_dotenv()

async def test_notion_integration():
    """Test the Notion MCP integration with Dedalus."""
    print("Testing Notion MCP integration...")
    
    # Test direct Notion search
    print("\n1. Testing direct Notion search:")
    search_result = await search_notion_for_dedalus("meeting notes")
    print(search_result)
    
    # Test with Dedalus
    print("\n2. Testing Dedalus with Notion tool:")
    client = AsyncDedalus()
    runner = DedalusRunner(client)
    
    result = await runner.run(
        input="Search my Notion workspace for 'project planning' and summarize what you find. Use the search_notion_for_dedalus function.",
        model="openai/gpt-4o-mini",
        stream=False
    )
    
    print("Dedalus + Notion Result:")
    print(result.final_output)

async def main():
    """Original Dedalus test + Notion integration test."""
    # Original test
    print("Running original Dedalus test...")
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    result = await runner.run(
        input="Who won Wimbledon 2025?",
        model="openai/gpt-4o-mini",
        mcp_servers=["akakak/sonar"],
        stream=False
    )

    print("Original result:")
    print(result.final_output)
    
    # Notion integration test
    print("\n" + "="*50)
    await test_notion_integration()

if __name__ == "__main__":
    asyncio.run(main())