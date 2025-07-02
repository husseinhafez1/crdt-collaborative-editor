"""
FastAPI Main Application
This module provides the REST and WebSocket API endpoints for the collaborative editor.

TODO: Implement the following:

1. FastAPI app setup:
   - Create FastAPI instance
   - Add CORS middleware
   - Set up logging

2. REST endpoints:
   - GET /api/document - Get document state
   - POST /api/document/reset - Reset document
   - GET /metrics - Prometheus metrics

3. WebSocket endpoint:
   - WS /ws/{client_id} - Real-time collaboration

4. Integration:
   - Connect Document and SessionManager
   - Handle operation routing
   - Error handling
"""

import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.session import SessionManager
from app.document import Document
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from app.metrics import crdt_operations_total, active_sessions, crdt_conflicts_resolved

app = FastAPI()
document = Document()
session_manager = SessionManager(document)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    """Serve a simple HTML page for testing."""
    # TODO: Implement this method
    # 1. Return HTML with basic editor interface
    # 2. Include JavaScript for WebSocket connection
    # 3. Add basic styling
    pass


@app.get("/api/document")
async def get_document():
    return JSONResponse(content=document.get_state())


@app.post("/api/document/reset")
async def reset_document():
    document.reset()
    await session_manager.broadcast(document.get_state())
    return {"message": "Document reset"}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await session_manager.add_session(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            document.apply_operation(data)
            await session_manager.broadcast(data, exclude_client=client_id)
    except WebSocketDisconnect:
        await session_manager.remove_session(client_id)
    except Exception as e:
        logger.error(f"Error in WebSocket endpoint: {e}")
        await session_manager.remove_session(client_id)


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# TODO: Add helper functions for:
# - Message validation
# - Error handling
# - Operation routing
# - Client notification


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 