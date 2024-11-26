import asyncio
import fastapi
import pydantic
import vsystech_users_models
import sys
import os
sys.path.append(os.getcwd() + "/framework")
import restapi
from vsystech_users_models import UserPurchase, Products, CartItem
from datetime import datetime, timedelta
import bson


router = fastapi.APIRouter(prefix='/users',  tags=['Users'])

@router.get('/createPurchase', tags=['Users']) #response_model=Users
async def createPurchase(data):
    created_purchases = []
    for prod in data["products"]:
        product_data = await Products.get(prod["id"])
        product_data = product_data.dict()
        create_data = {
            "payment_id": data["payment_id"],
            "order_date": data["created"],
            "delivery_date": data["created"] + timedelta(days=7),
            "returned": False,
            "is_delivered": False,
            "product_image": product_data["thumbnail_image_url"],
            "tracking_id": "",
            "userData": data["userData"],
            "product": prod,
            "c": datetime.utcnow(),
            "u": datetime.utcnow(),
            "tid": str(bson.ObjectId()) 
        }
        created_purchases.append(await UserPurchase(**create_data).create())
        update_data = {
            "id": prod["cart_id"],
            "status": "Purchased",
            "c": datetime.utcnow(),
            "u": datetime.utcnow(),
            "tid": prod["cart_id"]
        }
        await CartItem(**update_data).update()
    print(created_purchases)
    return created_purchases
    # return await Use.get(id)
