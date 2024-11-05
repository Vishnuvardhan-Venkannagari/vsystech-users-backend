import asyncio
import fastapi
import pydantic
from vsystech_users_models import *
import sys
import os
sys.path.append(os.getcwd() + "/framework")
import restapi
import context
from vsystech_users_models import CartItem
from datetime import datetime
import bson

router = fastapi.APIRouter(prefix='/cart',  tags=['Cart'])

@router.post('/addToCart')
async def addToCart(data: AddCartItemParams, response_model=CartItem):
    auth_user = context.context.get('auth_user', {})
    if not auth_user:
        return {"satus": False, "msg": "No user found"}
    auth_user = auth_user["user_data"]
    data = data.model_dump()
    productdata = await Products.get(data["product_id"])
    productdata = productdata.dict()
    if not productdata:
        return {"satus": False, "msg": "No product found"}
    user_ref = {
        "uid": auth_user["user_id"], 
        "firstName": auth_user["firstName"],
        "lastName": auth_user["lastName"],
        "email": auth_user["email"],
        "phoneNumber": auth_user["phoneNumber"]
    }
    product_ref = {
        "id": productdata["id"],
        "name": productdata["name"],
        "price": float(productdata["price"]),
        "img_url": productdata["img_url"]
    }
    create_data = {
        "status": "InCart",
        "is_selected": True,
        "userData": user_ref,
        "productData": product_ref,
        "c": datetime.utcnow(),
        "u": datetime.utcnow(),
        "tid": str(bson.ObjectId()) 
    }
    return await CartItem(**create_data).create()