"""
Proper MCP Client based on official tutorial
Connects to MCP servers including hosted Notion MCP server
"""

import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    
    async def connect_to_hosted_server(self, server_url: str = "https://mcp.notion.com/mcp"):
        """Connect to a hosted MCP server using mcp-remote
        
        Args:
            server_url: URL of the hosted MCP server
        """
        print(f"Connecting to hosted MCP server: {server_url}")
        
        # Use mcp-remote to connect to hosted server
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "mcp-remote", server_url],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("Connected to server with tools:", [tool.name for tool in tools])
        
        # List available resources
        try:
            resources_response = await self.session.list_resources()
            resources = resources_response.resources
            print("Available resources:", [resource.name for resource in resources])
        except Exception as e:
            print(f"No resources available or error listing resources: {e}")
    
    async def connect_to_server(self, server_script_path: str):
        """Connect to a local MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
        
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("Connected to server with tools:", [tool.name for tool in tools])
    
    async def list_tools(self):
        """List all available tools"""
        if not self.session:
            raise RuntimeError("Not connected to any server")
        
        response = await self.session.list_tools()
        return response.tools
    
    async def list_resources(self):
        """List all available resources"""
        if not self.session:
            raise RuntimeError("Not connected to any server")
        
        try:
            response = await self.session.list_resources()
            return response.resources
        except Exception as e:
            print(f"Error listing resources: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """Call a specific tool with arguments"""
        if not self.session:
            raise RuntimeError("Not connected to any server")
        
        result = await self.session.call_tool(tool_name, arguments)
        return result
    
    async def read_resource(self, resource_uri: str):
        """Read a specific resource"""
        if not self.session:
            raise RuntimeError("Not connected to any server")
        
        result = await self.session.read_resource(resource_uri)
        return result
    
    async def interactive_session(self):
        """Run an interactive session to test tools and resources"""
        print("\nMCP Client Interactive Session!")
        print("Commands:")
        print("  tools - List available tools")
        print("  resources - List available resources")
        print("  call <tool_name> <json_args> - Call a tool")
        print("  read <resource_uri> - Read a resource")
        print("  quit - Exit")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() == 'quit':
                    break
                elif command.lower() == 'tools':
                    tools = await self.list_tools()
                    print("\nAvailable tools:")
                    for tool in tools:
                        print(f"  - {tool.name}: {tool.description}")
                elif command.lower() == 'resources':
                    resources = await self.list_resources()
                    print("\nAvailable resources:")
                    for resource in resources:
                        print(f"  - {resource.name} ({resource.uri})")
                elif command.startswith('call '):
                    parts = command.split(' ', 2)
                    if len(parts) >= 2:
                        tool_name = parts[1]
                        args = {}
                        if len(parts) == 3:
                            import json
                            try:
                                args = json.loads(parts[2])
                            except json.JSONDecodeError:
                                print("Invalid JSON arguments")
                                continue
                        
                        result = await self.call_tool(tool_name, args)
                        print(f"\nResult: {result.content}")
                    else:
                        print("Usage: call <tool_name> <json_args>")
                elif command.startswith('read '):
                    parts = command.split(' ', 1)
                    if len(parts) == 2:
                        resource_uri = parts[1]
                        result = await self.read_resource(resource_uri)
                        print(f"\nResource content: {result.contents}")
                    else:
                        print("Usage: read <resource_uri>")
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except Exception as e:
                print(f"Error: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    
    try:
        if len(sys.argv) > 1:
            # Connect to local server
            await client.connect_to_server(sys.argv[1])
        else:
            # Connect to hosted Notion MCP server by default
            await client.connect_to_hosted_server()
        
        await client.interactive_session()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
