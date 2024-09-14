import fastapi
import sys
import datetime
import requests
import os
import uuid
import json
import glob
import httpx
import base64
import typing
import importlib
from redispool import RedisModel
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials,auth,firestore, initialize_app
# sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework")
dir_path = os.path.dirname(os.path.realpath(__file__))
import pyrebase

app = fastapi.FastAPI(version='1.0.0',
                      description=f"RestAPI for VSYSTECH Platform",
                      title="RestApi")


firebase_config = {
    "apiKey": "AIzaSyCKc8gJG-6MP5aU3Hme7hSVdkziP6nGlo4",
    "authDomain": "vsystech-users.firebaseapp.com",
    "databaseURL": "https://vsystech-users-default-rtdb.firebaseio.com",
    "projectId": "vsystech-users",
    "storageBucket": "vsystech-users.appspot.com",
    "messagingSenderId": "525115781661",
    "appId": "1:525115781661:web:46706dd6a4ab20712bccf4"
}
firebase = pyrebase.initialize_app(firebase_config)
cred_path = os.path.join(dir_path, "vsystech-users-firebase-adminsdk-w3tk9-f514a70a29.json")
cred = credentials.Certificate(cred_path)
default_app = initialize_app(cred)

async def createInternalErrorMessage(errFormat):
    try:
        id = str(uuid.uuid4()).replace("-", "")
        # conn = await framework.redispool.get_redis_connection()
        # await conn.setex("internalerror_" + id, 60, errFormat)
        print(errFormat)
        return True, id
    except:
        return False, ""

# async def createSession(id_token):
#     session = requests.Session()
#     session.headers.update({
#         "Authorization": f"Bearer {id_token}",
#         "Content-Type": "application/json"
#     })
#     url = "http://127.0.0.1:8000/api/secure-data"
#     response = session.get(url)

#     print(response.json())
#     print(response.headers)

async def userLogin(data):
    if data.get("email", ""):
        request = fastapi.Request
        # password = data["password"]
        emai, password = data["email"], data["password"]
        user = firebase.auth().sign_in_with_email_and_password(emai, password)
        token = user["idToken"]
        # print(user)
        if RedisModel().get(user["localId"] + "_token"):
            RedisModel().delete(user["localId"] + "_token")
        RedisModel().post(user["localId"] + "_token", token)
        # print(request.headers.get("Authorization"))
        # await createSession(token)
    if data.get("phoneNumber", ""):
        user = auth.sign_in_with_email_and_password(data["email", data["password"]])
        token = user["idToken"]
        RedisModel().hset(user.uid + "_token", 3600, token)
    return {"status": "login success", "token": token}

async def authenticate(request: fastapi.Request):
    authtoken = request.headers.get("authtoken")
    decoded_token = auth.verify_id_token(authtoken)
    uid = decoded_token['uid']

# @app.on_event("startup")
# def onStart():
#     for filename in glob.glob("**/**/*.py", recursive=True):
#         print(filename)
#         if filename.startswith("_"):
#             continue
#         modname = os.path.splitext(filename)[0].replace(os.sep, '.')
#         # print("Loading:",modname)
#         mod = importlib.import_module(modname)
        
#         # If a variable by name "roter" is defined load that directly
#         # Else go through the module and if any of the variable is a router load that...
#         symbol = getattr(mod, 'router', None)
#         if isinstance(symbol, fastapi.APIRouter):
#             app.include_router(symbol, prefix="/api")
#         else:
#             for attr in dir(mod):
#                 if not attr.startswith("_"):
#                     symbol = getattr(mod, attr)
#                     if isinstance(symbol, fastapi.APIRouter):
#                         # print("Loading module:", modname, " Route:",attr, [(x.path, x.name)  for x in symbol.routes])
#                         app.include_router(symbol, prefix="/api")

