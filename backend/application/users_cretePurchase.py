import asyncio
import fastapi
import pydantic
import vsystech_users_models
import sys
import os
sys.path.append(os.getcwd() + "/framework")
import restapi
from vsystech_users_models import UserPurchase



router = fastapi.APIRouter(prefix='/users',  tags=['Users'])

@router.get('/createPurchase', tags=['Users']) #response_model=Users
async def createPurchase(data):
    created_purchases = []
    print(data)
    for prod in data["products"]:
        print(prod)
        create_data = {
            "payment_id": data["payment_id"],
            "order_date": data["c"],
            "delivery_date": data["c"],
            "returned": False,
            "is_delivered": False,
            "product_image": "",
            "tracking_id": "",
            "userData": data["userData"],
            "product": prod
        }
        created_purchases.append(await UserPurchase(**create_data).create())
    print(created_purchases)
    return created_purchases
    # return await Use.get(id)
