#!/usr/bin/env python3
"""
Startup script for the Notion MCP API server.
Run this to start the server that Dedalus can connect to.
"""

import asyncio
import uvicorn
from notion_api_server import app

def start_server():
    """Start the Notion MCP API server."""
    print("Starting Notion MCP API server on http://localhost:8000")
    print("Available endpoints:")
    print("  - GET  /health - Health check")
    print("  - GET  /resources - List Notion resources")
    print("  - GET  /tools - List Notion tools")
    print("  - POST /search - Search Notion workspace")
    print("  - GET  /search/{query} - Search via GET")
    print("  - POST /page - Get specific page")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    start_server()
