from firebase_admin import auth,firestore
import sys
import os
import context
sys.path.append(os.getcwd() + "framework/")
import queryparams
from queryparams import QueryParams
from vsystech_users_models import PaymentVerifyPayment
import pyrebase
import bson
import json
from datetime import datetime
import fastapi
from payment_gateway import getgatewayName

router = fastapi.APIRouter(prefix='/payments',  tags=['Payments'])

@router.get("/verifyPayment") 
async def verifyPayment(params = fastapi.Depends(queryparams.QueryParams)): #: PaymentVerifyPayment
    # if params.download:
    #     response.headers['Content-Disposition'] = f'attachment; filename="reviews.html"'
    # auth_user = context.context.get('auth_user', {})
    # data = data.model_dump()
    print(params.q)
    return {"status": True, "msg": "success"}
    # if not auth_user.get("user_data", {}):
    #     return {"status": False, "msg": "No user found"}
    # auth_user = auth_user["user_data"]
    