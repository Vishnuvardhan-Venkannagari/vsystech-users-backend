from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import sys
import datetime
import os
from redispool import get_redis_connection
import json
sys.path.append(os.getcwd() + "application/")
from vsystech_users_models import SupportTicket
from ai_bot_response import get_ai_response

router = APIRouter()

mongo_client = AsyncIOMotorClient("mongodb://admin:admin@localhost:27017")
mongo_db = mongo_client["message_app"]
message_collection = mongo_db["messages"]

MaxReturnTime = 4 * 60

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            await self.disconnect(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for ws in self.active_connections:
            try:
                await ws.send_text(message)
            except Exception as e:
                print("Failed to send message to a websocket:", e)
                disconnected.append(ws)

        for ws in disconnected:
            await self.disconnect(ws)
sockets = ConnectionManager()

@router.websocket("/ws/{id}")
async def message(websocket: WebSocket,id: str):
    await sockets.connect(websocket, id)
    # rcon = await get_redis_connection()
    # is_success = False
    # startTime = datetime.datetime.utcnow().timestamp()
    try:
        
        while True:
            data = await websocket.receive_text()
            msg_data = json.loads(data)
            message_doc = {
                "room_id": msg_data.get("room_id"),
                "sender_id": msg_data.get("sender_id"),
                "sender_name": msg_data.get("sender_name"),
                "message": msg_data.get("message"),
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }
            result = await message_collection.insert_one(message_doc)
            message_doc["_id"] = str(result.inserted_id)
            message_doc["chat_id"] = message_doc["room_id"]
            await sockets.broadcast(json.dumps(message_doc))
            print("Broadcasted message:", message_doc)
            
            ai_response = await get_ai_response(message_doc["message"])
            bot_message = {
                "room_id": msg_data.get("room_id"),
                "sender_id": "ai_bot",
                "sender_name": "VSYSTECH Support Bot",
                "message": ai_response["message"],
                "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "needs_escalation": ai_response["needs_escalation"]
            }
            result = await message_collection.insert_one(bot_message)
            bot_message["_id"] = str(result.inserted_id)
            bot_message["chat_id"] = bot_message["room_id"]

            await sockets.broadcast(json.dumps(bot_message))
            print("Broadcasted AI message:", bot_message)


    except WebSocketDisconnect:
        print("WebSocket disconnected")
        await sockets.disconnect(websocket)

    except Exception as e:
        print("Error occured", e)