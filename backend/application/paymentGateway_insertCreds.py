import sys
import os
import requests.auth
sys.path.append(os.getcwd() + "framework/")
from queryparams import QueryParams
from vsystech_users_models import PaymentGatewayParams, PaymentGateway
from datetime import datetime
import fastapi
import context
import requests
import bson

router = fastapi.APIRouter(prefix='/paymentgateway',  tags=['PaymentGateway'])

@router.post("/insertCreds") 
async def insertCreds(data: PaymentGatewayParams):
    auth_user = context.context.get('auth_user', {})
    if not auth_user.get("user_data", {}):
        return {"satus": False, "msg": "No user found"}
    auth_user = auth_user["user_data"]
    data = data.model_dump()

    base_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    reqdata = {
        "grant_type": "client_credentials"
    }

    sendRequest = requests.post(base_url, 
                    headers=headers, 
                    data=reqdata, 
                    auth=requests.auth.HTTPBasicAuth(data["api_key"], data["api_secret"])
    )
    if not sendRequest.status_code == 200:
        return {"status": False, "msg": "Invalid creds"}
    input_doc = {
        "gateway": {
            "gateway_name": data["gateway_name"],
            "base_url": "https://api-m.sandbox.paypal.com/v2",
            "api_key": data["api_key"],
            "api_secret": data["api_secret"]
        },
        "is_verified": True,
        "veifiedBy": {
            "uid": auth_user["user_id"],
            "firstName": auth_user["firstName"],
            "lastName": auth_user["lastName"],
            "email": auth_user["email"],
            "phoneNumber": auth_user["phoneNumber"]
        },
        "c": datetime.utcnow(),
        "u": datetime.utcnow(),
        "tid": str(bson.ObjectId()) 
    }
    return await PaymentGateway(**input_doc).create()