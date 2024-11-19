from firebase_admin import auth,firestore
import sys
import os
import context
sys.path.append(os.getcwd() + "framework/")
from queryparams import QueryParams
from redispool import get_redis_connection
from vsystech_users_models import Payments
import pyrebase
import bson
import json
from datetime import datetime
import fastapi
from payment_gateway import getgatewayName

router = fastapi.APIRouter(prefix='/payments',  tags=['Payments'])

@router.get("/cancelPayment") 
async def cancelPayment(token: str = fastapi.Query(...)):
    rcon = await get_redis_connection()
    query = {"order_id": token}
    order_details = await Payments.get_all(QueryParams(q=json.dumps(query), limit=10000))
    if not order_details["data"]:
        return {"status": False, "msg": "No data found"}
    order_details = order_details["data"][0]
    update_doc = {"id": order_details["id"], 
        "payment_status": "CANCELED",
        "c": order_details["created"],
        "u": datetime.utcnow(),
        "tid": order_details["id"]
    }
    print(await Payments(**update_doc).update())
    data = {"status": "failed", "msg": "payment cancelled"}
    await rcon.hset("paymentsdata", token, json.dumps(data))
    return {"status": True, "msg": "success"}
    