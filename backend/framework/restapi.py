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
from redispool import RedisModel
# from fastapi.middleware.cors import CORSMiddleware
# from firebase_admin import credentials,firestore, initialize_app
# from firebase_admin import auth as fs_admin
# dir_path = os.path.dirname(os.path.realpath(__file__))
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
firebase_auth = firebase.auth()


# cred_path = os.path.join(dir_path + "/framework", "vsystech-users-firebase-adminsdk-w3tk9-f514a70a29.json")
# cred = credentials.Certificate(cred_path)
# default_app = initialize_app(cred)



package_dir = os.getcwd() + "/application"
# print(dir_path)
# print(package_dir)
# package_dir = "/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/application"
# package_dir = "/opt/vsystech-users-backend/backend/application"
sys.path.append(os.path.abspath(package_dir))
@app.on_event("startup")
def onStart():
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f'{module_info.name}')#routers.
        if hasattr(module, 'router'):
            app.include_router(module.router, prefix="/api")


@app.middleware('http')
async def authMiddleware(request: fastapi.Request, call_next):
    if request.url.path in ['/docs', '/openapi.json', '/api/login', '/api/logout', '/ping', '/api/me', "/api/users/createUSerWithEmail", "/api/users/loginWithEmail"] :#+ framework.settings.noauth_urls:
        return await call_next(request)
    if not request.headers.get('authtoken'):
        redirect_url = f'https://{request.base_url.hostname}/api/login'
        response = fastapi.responses.JSONResponse({'url': redirect_url}, 401)
        return response
    return await call_next(request)   

@app.middleware('http')
async def contextMiddleware(request: fastapi.Request, call_next):
    data = {}
    data['domain'] = request.base_url
    data['oauth_redirect'] = f'{request.base_url}api/login'.replace('http://', 'https://')
    authtoken = request.headers.get('authtoken')
    if authtoken:
        userdata = await authenticate(authtoken)
        if userdata:
            data["rpt"] = {"user_data": userdata}
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
        errFormat = error
        # '''Error:
        # Stack Trace:
        # %s
        # ''' % (traceback.format_exc())
        return fastapi.responses.JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred.", "error": str(errFormat)}
        )
class loginWithEmail(pydantic.BaseModel):
    email: str
    password: str

@app.post("/api/loginWithEmail")
async def loginWithEmail(data: loginWithEmail, response: fastapi.Response):
    data = data.model_dump()
    # result =  await userLogin(data)
    # # response.headers["Authorization"] = f"Bearer {result['token']}"
    # # headers_dict = dict(response.headers.items())
    # print(result)
    # return result
# async def userLogin(data):
    if data.get("email", ""):
        emai, password = data["email"], data["password"]
        user = firebase.auth().sign_in_with_email_and_password(emai, password)
        token = user["idToken"]
        if RedisModel().get(user["localId"] + "_token"):
            RedisModel().delete(user["localId"] + "_token")
        RedisModel().post(user["localId"] + "_token", token)
    if data.get("phoneNumber", ""):
        user = firebase.auth().sign_in_with_email_and_password(data["email", data["password"]])
        token = user["idToken"]
        RedisModel().hset(user.uid + "_token", 3600, token)
    return {"status": "login success", "token": token}

async def authenticate(authtoken):
    user = firebase.auth().get_account_info(authtoken)
    uid = user['users'][0]['localId']  # Get the UID from the account info
    data = {"uid": uid}
    return {"status": "success", "data": data}
    # decoded_token = fs_admin.verify_id_token(authtoken)
    # data = {}
    # data["uid"] = decoded_token['uid']
    # return {"status": "success", "data": data}
