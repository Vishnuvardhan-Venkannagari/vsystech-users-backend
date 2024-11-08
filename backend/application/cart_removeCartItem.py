from firebase_admin import auth,firestore
import sys
import os
import context
sys.path.append(os.getcwd() + "framework/")
from queryparams import QueryParams
from vsystech_users_models import CartItem, RemoveCartItemParams
import pyrebase
import json
from datetime import datetime
import fastapi

router = fastapi.APIRouter(prefix='/cart',  tags=['Cart'])

@router.post("/removeCartItem") 
async def removeCartItem(data: RemoveCartItemParams):
    # if params.download:
    #     response.headers['Content-Disposition'] = f'attachment; filename="reviews.html"'
    auth_user = context.context.get('auth_user', {})
    if not auth_user.get("user_data", {}):
        return {"satus": False, "msg": "No user found"}
    data = data.model_dump()
    cartItemData = await CartItem.get(data["cart_item_id"])
    cartItemData = cartItemData.dict()
    # print(cartItemData)
    if not cartItemData:
        return {"status": False, "msg": "No Item found"}
    # auth_user = auth_user["user_data"]
    update_data = {
        "id": cartItemData["id"],
        "status": "Removed",
        "c": cartItemData["created"],
        "u": datetime.utcnow(),
        "tid": cartItemData["id"]
    }
    return await CartItem(**update_data).update()
