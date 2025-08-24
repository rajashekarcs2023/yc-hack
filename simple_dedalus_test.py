import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from dedalus_labs.utils.streaming import stream_async

load_dotenv()

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def main():
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    result = await runner.run(
        input="Calculate (15 + 27) * 2", 
        model="openai/gpt-4o", 
        tools=[add, multiply]
    )

    print(f"Result: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
