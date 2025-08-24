# YC Hack - Notion MCP Integration

This project creates a standalone Notion MCP client that integrates with Dedalus, allowing AI agents to access Notion workspace data.

## Architecture

1. **Notion MCP Client** (`notion_mcp_client.py`) - Direct connection to Notion's MCP server
2. **API Server** (`notion_api_server.py`) - FastAPI server exposing Notion data via REST API
3. **Dedalus Tool** (`dedalus_notion_tool.py`) - Tool for Dedalus to access Notion data
4. **Test Integration** (`test.py`) - Example usage and testing

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Notion MCP connection (requires OAuth with Notion)

3. Start the Notion API server:
```bash
python start_notion_server.py
```

4. Run tests:
```bash
python test.py
```

## Usage

### Direct Notion MCP Client
```python
from notion_mcp_client import NotionMCPService

service = NotionMCPService()
await service.start()
results = await service.search("meeting notes", limit=5)
```

### With Dedalus
```python
from dedalus_notion_tool import search_notion_for_dedalus

# Use in Dedalus prompts
result = await search_notion_for_dedalus("project planning", 10)
```

## API Endpoints

- `GET /health` - Health check
- `GET /resources` - List Notion resources  
- `GET /tools` - List Notion tools
- `POST /search` - Search Notion workspace
- `POST /page` - Get specific page

## Files

- `notion_mcp_client.py` - Core MCP client implementation
- `notion_api_server.py` - FastAPI server wrapper
- `dedalus_notion_tool.py` - Dedalus integration tool
- `start_notion_server.py` - Server startup script
- `test.py` - Integration tests and examples