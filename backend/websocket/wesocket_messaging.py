from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
import sys
import datetime
import os
import json
sys.path.append(os.getcwd() + "framework/")
from redispool import get_redis_connection
import asyncio

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],  # Include all methods
        allow_headers=["*"],  # Allow all headers
        allow_credentials=True
)
MaxReturnTime = 4 * 60

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
    print(f"WebSocket opened for ID: {id}")
    rcon = await get_redis_connection()
    is_success = False
    startTime = datetime.datetime.utcnow().timestamp()
    try:
        while datetime.datetime.utcnow().timestamp() < startTime + MaxReturnTime:
            print("Inside")
            if await rcon.hexists("paymentsdata", id):
                msg_data = await rcon.hget("paymentsdata", id)
                print(f"Payment data found for ID {id}: {msg_data}")
                await sockets.send_personal_message(json.dumps(msg_data), websocket)
                await rcon.hdel("paymentsdata", id)
                # await sockets.disconnect(websocket)
                is_success = True
                break
            await asyncio.sleep(1) 
        if not is_success:
            data = {"status": "failed", "msg": "payment not completed"}
            await sockets.send_personal_message(json.dumps(data), websocket)
    except Exception as e:
        # await sockets.disconnect(websocket)
        print("Error occured", e)
    finally:
        await sockets.disconnect(websocket)
        print(f"WebSocket closed for ID: {id}")
    
