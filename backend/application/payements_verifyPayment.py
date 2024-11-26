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
async def verifyPayment(token: str = fastapi.Query(...), PayerID: str = fastapi.Query(...)):
    rcon = await get_redis_connection()
    gateway =  getgatewayName("PayPal")
    query = {"order_id": token}
    order_details = await Payments.get_all(QueryParams(q=json.dumps(query), limit=10000))
    if not order_details["data"]:
        return {"status": False, "msg": "No data found"}
    order_details = order_details["data"][0]
    verify_order = await gateway().verifyOrder(order_details)
    print("In verify method",verify_order)
    if verify_order == "FAILED":
        print("Inside if failed")
        data = {"status": "failed", "msg": "Payment not Completed"}
        update_doc = {"id": order_details["id"], 
            "payment_status": "FAILED",
            "c": order_details["c"],
            "u": datetime.utcnow(),
            "tid": order_details["id"]
        }
        updatePayment = await Payments(**update_doc).update()
        await rcon.hset("paymentsdata", token, json.dumps(data))
        print(updatePayment)
        return {"status": False, "msg": "Payment Failed"}
    data = {"status": "success", "msg": "Payment completed Success"}
    await rcon.hset("paymentsdata", token, json.dumps(data))
    update_doc = {
        "id": order_details["id"], 
        "payment_status": "PAID",
        "c": order_details["c"],
        "u": datetime.utcnow(),
        "tid": order_details["id"],
        "payment_id": verify_order.get("purchase_units", [])[1].get("payments", {}).get("captures", {}).get("id", ""),
        "paid_amt": float(verify_order.get("purchase_units", [])[1].get("payments", {}).get("captures", {}).get("amount", {}).get("value", ""))

    }
    updatePayment = await Payments(**update_doc).update()
    print(updatePayment)
    return {"status": True, "msg": "success"}
    