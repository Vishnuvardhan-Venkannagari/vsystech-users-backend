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

@router.get("/verifyPayment") 
async def verifyPayment(token: str = fastapi.Query(...), PayerID: str = fastapi.Query(...)): #: PaymentVerifyPayment
    print(token, PayerID)
    rcon = await get_redis_connection()
    gateway =  getgatewayName("PayPal")
    query = {"order_id": token}
    order_details = await Payments.get_all(QueryParams(q=json.dumps(query), limit=10000))
    print(order_details)
    data = {"gateway_name": "Paypal", "order_id": token}
    verify_order = gateway().verifyOrder(data)
    data = {"status": "Success", "msg": "Success"}
    await rcon.hset("paymentsdata", token, json.dumps(data))
    return {"status": True, "msg": "success"}
    # if not auth_user.get("user_data", {}):
    #     return {"status": False, "msg": "No user found"}
    # auth_user = auth_user["user_data"]
    