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
from app.redis_pubsub import RedisPubSub
import os
from app.document import Document
from app.session import SessionManager
from app.redis_pubsub import RedisPubSub


app = FastAPI()
document = Document()
session_manager = SessionManager(document)

if not os.environ.get("PYTEST_CURRENT_TEST"):
    redis_pubsub = RedisPubSub(document)
else:
    redis_pubsub = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
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
    await session_manager.handle_websocket_connection(websocket, client_id)


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