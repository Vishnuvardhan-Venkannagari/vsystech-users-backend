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
import pkgutil
import traceback
import pydantic
import contextvars
import context
from redispool import get_redis_connection
from fastapi.middleware.cors import CORSMiddleware
# from firebase_admin import credentials,firestore, initialize_app
# from firebase_admin import auth as fs_admin
import pyrebase

app = fastapi.FastAPI(version='1.0.0',
                      description=f"RestAPI for VSYSTECH Platform",
                      title="RestApi")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"] ,  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

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
firebase_auth = firebase.auth()


# cred_path = os.path.join(dir_path + "/framework", "vsystech-users-firebase-adminsdk-w3tk9-f514a70a29.json")
# cred = credentials.Certificate(cred_path)
# default_app = initialize_app(cred)



package_dir = os.getcwd() + "/application"
sys.path.append(os.path.abspath(package_dir))

@app.on_event("startup")
def onStart():
    print("Onstart", package_dir)
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f'{module_info.name}')#routers.
        # print(hasattr(module, 'router'))
        if hasattr(module, 'router'):
            app.include_router(module.router, prefix="/api")


@app.middleware('http')
async def authMiddleware(request: fastapi.Request, call_next):
    if request.url.path in ['/docs', '/docs/', '/openapi.json', '/api/login', '/api/logout', '/ping', '/api/me', "/api/users/createUSerWithEmail", "/api/loginWithEmail"] :#+ framework.settings.noauth_urls:
        return await call_next(request)
    if not request.headers.get('authtoken'):
        redirect_url = f'https://{request.base_url.hostname}/api/login'
        response = fastapi.responses.JSONResponse({'url': redirect_url}, 401)
        return response
    auth_user = context.context.get('auth_user', {})
    if not auth_user:
        response = fastapi.Response(None, 403)
    else:
        response: fastapi.responses.Response  = await call_next(request)   
    return response

async def authenticate(authtoken):
    
    redisIns = await get_redis_connection()
    if await redisIns.exists(authtoken) and await redisIns.get(authtoken):
        auth_user = json.loads(await redisIns.get(authtoken))
        return auth_user
    user = firebase.auth().get_account_info(authtoken)
    uid = user['users'][0]['localId']  # Get the UID from the account info
    auth_user = {"uid": uid}
    await redisIns.setex(authtoken, 3600, json.dumps(auth_user))
    return auth_user


@app.middleware('http')
async def contextMiddleware(request: fastapi.Request, call_next):
    data = {}
    data['domain'] = request.base_url
    data['oauth_redirect'] = f'{request.base_url}api/login'.replace('http://', 'https://')
    authtoken = request.headers.get('authtoken')
    if authtoken:
        userdata = await authenticate(authtoken)
        if userdata:
            data["auth_user"] = {"user_data": userdata}
            print(data)
    _starlette_context_token: contextvars.Token = context._request_scope_context_storage.set(data)
    try:
        resp = await call_next(request)
        response_body = b""
        async for chunk in resp.body_iterator:
            response_body += chunk

        return fastapi.Response(content=response_body, status_code=resp.status_code, headers=dict(resp.headers))

    except Exception as error:
        """
        Exception error
        """
        # errFormat = error
        errFormat = '''Error: 
        Stack Trace:
        %s
        ''' % (traceback.format_exc())
        print(errFormat)
        return fastapi.responses.JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred.", "error": str(errFormat)}
        )
    
class logInData(pydantic.BaseModel):
    email: str
    password: str

@app.post("/api/login")
async def logIn(data: logInData, response: fastapi.Response):
    data = data.model_dump()
    rcon = await get_redis_connection()
    if data.get("email", ""):
        emai, password = data["email"], data["password"]
        user = firebase.auth().sign_in_with_email_and_password(emai, password)
        authtoken = user["idToken"]
        auth_user = {"uid": user["localId"]}
        pendingseconds = 3600
        if not await rcon.exists(authtoken) and not await rcon.get(authtoken):
            await rcon.setex(authtoken, pendingseconds, json.dumps(auth_user))
    if data.get("phoneNumber", ""):
        user = firebase.auth().sign_in_with_email_and_password(data["email", data["password"]])
        authtoken = user["idToken"]
        auth_user = {"uid": user["localId"]}
        await rcon.setex(authtoken, pendingseconds, json.dumps(auth_user))
    return {"status": "login success", "token": authtoken}

