from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import manager
import logging

logger = logging.getLogger("lifelink.ws_router")
router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws/{category}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, category: str, client_id: str):
    await manager.connect(websocket, category=category)
    try:
        # Send an immediate connection acknowledgement
        await websocket.send_json({
            "event": "CONNECTED",
            "message": f"Connected to LifeLink Emergency Dispatch Hub as [{category}:{client_id}]"
        })
        while True:
            # Keep connection alive and listen for client heartbeats/messages
            data = await websocket.receive_text()
            # Client can ping back
            await websocket.send_json({"event": "PONG", "received": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, category=category)
        logger.info(f"Client {client_id} disconnected from {category}")
    except Exception as e:
        manager.disconnect(websocket, category=category)
        logger.error(f"WebSocket error: {e}")
