import json
import logging
from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
from app.metrics import crdt_operations_total, active_sessions, crdt_conflicts_resolved
from app.utils import log_operation, validate_operation

class SessionManager:    
    def __init__(self, document):
        self.active_sessions = {}
        self.document = document
    
    async def add_session(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        await websocket.send_json(self.document.get_state())
        self.active_sessions[client_id] = websocket
        active_sessions.inc()
    
    async def remove_session(self, client_id: str):
        websocket = self.active_sessions.pop(client_id, None)
        if websocket:
            await websocket.close()
        active_sessions.dec()
    
    async def broadcast(self, message: dict, exclude_client: str = None):
        for cid, ws in self.active_sessions.items():
            if cid != exclude_client:
                await ws.send_json(message)
    
    async def send_to_client(self, client_id: str, message: dict):
        ws = self.active_sessions.get(client_id)
        if ws:
            await ws.send_json(message)
    
    def get_active_clients(self) -> Set[str]:
        return set(self.active_sessions.keys())
    
    def is_client_connected(self, client_id: str) -> bool:
        return client_id in self.active_sessions
    
    async def handle_websocket_connection(self, websocket: WebSocket, client_id: str):
        await self.add_session(client_id, websocket)
        logging.info(f"Client {client_id} connected")
        try:
            while True:
                message = await websocket.receive_json()
                await self._handle_client_message(client_id, message)
        except WebSocketDisconnect:
            await self.remove_session(client_id)
            logging.info(f"Client {client_id} disconnected")
        except Exception as e:
            logging.error(f"Error handling WebSocket connection for client {client_id}: {e}")
            await self.remove_session(client_id)
            logging.info(f"Client {client_id} disconnected due to error")
    
    async def _handle_client_message(self, client_id: str, message: dict):
        try:
            if not validate_operation(message):
                logging.error(f"Invalid operation received from client {client_id}: {message}")
                return
            await self.document.apply_operation(message)
            log_operation(message, client_id)
            await self.broadcast(message, client_id)
        except Exception as e:
            logging.error(f"Error processing message from client {client_id}: {e}")
            await self.send_to_client(client_id, {"error": "Failed to process message"})