"""
FastAPI server that exposes the Notion MCP client as a REST API.
This allows Dedalus to easily access Notion data through HTTP calls.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import uvicorn
from notion_mcp_client import NotionMCPService

app = FastAPI(title="Notion MCP API", version="1.0.0")

# Global service instance
notion_service: Optional[NotionMCPService] = None

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

class PageRequest(BaseModel):
    page_id: str

@app.on_event("startup")
async def startup_event():
    """Initialize the Notion MCP service on startup."""
    global notion_service
    notion_service = NotionMCPService()
    await notion_service.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up the Notion MCP service on shutdown."""
    global notion_service
    if notion_service:
        await notion_service.stop()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "notion-mcp-api"}

@app.get("/resources")
async def list_resources():
    """List all available Notion resources."""
    try:
        resources = await notion_service.list_available_resources()
        return {"resources": resources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def list_tools():
    """List all available Notion tools."""
    try:
        tools = await notion_service.list_available_tools()
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_notion(request: SearchRequest):
    """Search Notion workspace."""
    try:
        results = await notion_service.search(request.query, request.limit)
        return {
            "query": request.query,
            "limit": request.limit,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/page")
async def get_page(request: PageRequest):
    """Get a specific page from Notion."""
    try:
        page_data = await notion_service.get_page(request.page_id)
        return {
            "page_id": request.page_id,
            "data": page_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/{query}")
async def search_notion_get(query: str, limit: int = 10):
    """Search Notion workspace via GET request."""
    try:
        results = await notion_service.search(query, limit)
        return {
            "query": query,
            "limit": limit,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
