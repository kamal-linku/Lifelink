from typing import List, Dict, Any
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger("lifelink.ws")

class ConnectionManager:
    def __init__(self):
        # List of all active WebSocket connections
        self.active_connections: List[WebSocket] = []
        # Client map by category e.g. "volunteers", "hospitals", "requesters"
        self.category_connections: Dict[str, List[WebSocket]] = {
            "volunteers": [],
            "hospitals": [],
            "blood_banks": [],
            "requesters": []
        }

    async def connect(self, websocket: WebSocket, category: str = "requesters"):
        await websocket.accept()
        self.active_connections.append(websocket)
        if category in self.category_connections:
            self.category_connections[category].append(websocket)
        logger.info(f"WebSocket connected. Total active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, category: str = "requesters"):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if category in self.category_connections and websocket in self.category_connections[category]:
            self.category_connections[category].remove(websocket)
        logger.info(f"WebSocket disconnected. Remaining: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast an event payload to every connected client."""
        payload_str = json.dumps(message)
        to_remove = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload_str)
            except Exception:
                to_remove.append(connection)
        
        for dead_conn in to_remove:
            if dead_conn in self.active_connections:
                self.active_connections.remove(dead_conn)

    async def broadcast_to_category(self, category: str, message: Dict[str, Any]):
        """Broadcast specifically to category (e.g. all volunteers for emergency dispatch)."""
        payload_str = json.dumps(message)
        conns = self.category_connections.get(category, [])
        to_remove = []
        for connection in conns:
            try:
                await connection.send_text(payload_str)
            except Exception:
                to_remove.append(connection)
        for dead in to_remove:
            if dead in conns:
                conns.remove(dead)

manager = ConnectionManager()
