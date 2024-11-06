from firebase_admin import auth,firestore
import sys
import os
import context
sys.path.append(os.getcwd() + "framework/")
from queryparams import QueryParams
from vsystech_users_models import CartItem, CartItemResponse
import pyrebase
import json
router = fastapi.APIRouter(prefix='/cart',  tags=['Cart'])

@router.get("/getCartItem") 
async def getCartItem():
    # if params.download:
    #     response.headers['Content-Disposition'] = f'attachment; filename="reviews.html"'
    auth_user = context.context.get('auth_user', {})
    print(auth_user)
    if not auth_user.get("user_data", {}):
        return {"satus": False, "msg": "No user found"}
    auth_user = auth_user["user_data"]
    query = {"userData.uid": auth_user["user_id"]}
    return await CartItem.get_all(QueryParams(q=json.dumps(query), limit=10000))
