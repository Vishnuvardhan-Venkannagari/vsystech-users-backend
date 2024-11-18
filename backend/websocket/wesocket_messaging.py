from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
sys.path.append(os.getcwd() + "framework/")
from redispool import get_redis_connection
app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=['*']
)
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

sockets = ConnectionManager()

@app.websocket("/ws/{id}")
async def paymentSocket(websocket: WebSocket,id: str):
    await sockets.connect(websocket)
    rcon = await get_redis_connection()
    is_success = False
    try:
        while True:
            if rcon.hexists("paymentsdata", id):
                await sockets.send_personal_message("Success", websocket)
                is_success = True
    except WebSocketDisconnect:
        await sockets.disconnect(id)
    if is_success:
        await sockets.send_personal_message("Failed", websocket)
