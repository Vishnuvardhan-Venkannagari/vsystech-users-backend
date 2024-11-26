from firebase_admin import auth,firestore
import sys
import os
import context
sys.path.append(os.getcwd() + "framework/")
from queryparams import QueryParams
from vsystech_users_models import PaymentCreatePayment, CartItem, Payments
import pyrebase
import bson
import json
from datetime import datetime
import fastapi
from payment_gateway import getgatewayName

router = fastapi.APIRouter(prefix='/payments',  tags=['Payments'])

@router.post("/createPayment") 
async def createPayment(data: PaymentCreatePayment):
    auth_user = context.context.get('auth_user', {})
    if not auth_user.get("user_data", {}):
        return {"status": False, "msg": "No user found"}
    auth_user = auth_user["user_data"]
    data = data.model_dump()
    query = {"userData.uid": auth_user["user_id"], "status": "InCart"}
    cartItems =  await CartItem.get_all(QueryParams(q=json.dumps(query), limit=10000))
    cart_price = 0.0
    products_ref = []
    if not cartItems.get("data", []):
        return {"status": False, "msg": "No items found"}
    cartItems = cartItems["data"]
    for item in cartItems:
        cart_price += item["productData"]["price"]
        products_ref.append({
            "id": item["productData"]["id"], 
            "name": item["productData"]["name"],  
            "price": item["productData"]["price"], 
            "cart_id": item["id"]
        })
    if data["gateway_name"] == "PayPal":
        paypal_fee_percent = 0.029
        fixed_fee = 0.30
        paypal_fee = round(cart_price * paypal_fee_percent + fixed_fee, 2)
        tax = round(cart_price * 0.075, 2)
    user_ref = {
        "uid": auth_user["user_id"], 
        "firstName": auth_user["firstName"],
        "lastName": auth_user["lastName"],
        "email": auth_user["email"],
        "phoneNumber": auth_user["phoneNumber"]
    }

    create_order_data = {
        "gateway_name": data["gateway_name"],
        "payment_status": "CHECKEDOUT",
        "order_amt": data["totla_price"],
        "cart_amt": cart_price,
        "tax": tax,
        "shipping_amt": 5,
        "paypal_fees": paypal_fee,
        "paid_amt": 0.0,
        "refunded_amt": 0.0,
        "products": products_ref,
        "userData": user_ref,
        "currency": "usd",
        "c": datetime.utcnow(),
        "u": datetime.utcnow(),
        "tid": str(bson.ObjectId()) 
    }
    order_details = await Payments(**create_order_data).create()
    gateway =  getgatewayName(data["gateway_name"])
    order_details = order_details.model_dump()
    createGatewayOrder = await gateway().createOrder(order_details)
    if not createGatewayOrder.get("status"):
        return {"status": False, "msg": "Payment not created"}
    
    update_doc = {
        "id": order_details["id"], 
        "order_id": createGatewayOrder["data"]["id"], 
        "approve_url": createGatewayOrder["data"]["links"][1]["href"],
        "payment_url": createGatewayOrder["data"]["payment_url"],
        "c": order_details["created"],
        "u": datetime.utcnow(),
        "tid": order_details["id"],
        "gateway_name": order_details["gateway_name"],
        # "products": 
    }
    return await Payments(**update_doc).update()