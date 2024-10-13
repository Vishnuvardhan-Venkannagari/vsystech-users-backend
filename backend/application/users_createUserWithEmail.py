import asyncio
import fastapi
import pydantic
import vsystech_users_models
from firebase_admin import auth,firestore
import datetime
import time
import sys
import os
# print(os.getcwd() + "framework")
# print("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/")
sys.path.append(os.getcwd() + "framework/")
import restapi
import pyrebase
from restapi import firebase

auth = firebase.auth()
db = firebase.database()



router = fastapi.APIRouter(prefix='/users')
@router.post("/createUSer")
async def createUSer(data: vsystech_users_models.Users):
    data = data.model_dump()
    password = "password"
    email = data.get("email")
    name = data.get("name")
    dob_str = data.get("dob")
    user = auth.create_user_with_email_and_password(email, password)

    user_id = user['localId']
    dob = datetime.datetime.strptime(dob_str, '%d-%m-%Y')
    epoch_dob = dob.timestamp() * 1000
    created_time = datetime.datetime.now()
    created_time = time.mktime(created_time.timetuple())
    user_data = {
            "email": email,
            "isEmailVerified": False,
            "user_id": user_id,
            "name": name,
            "disabled": False,
            "state": data.get("state"),
            "dob": epoch_dob,
            "role": "user",
            "phone_number": data.get("phone_number", ""),
            "country": data.get("country", "USA"),
            "photo_url": data.get("photo_url", ""),
            "created_time": created_time,
        }
    print(db.child("users").child(user_id).set(user_data))
    # db = firestore.client()
    # db.collection('users').document(user_id).set(user_data)
    return {"status": "success", "result": user_id}
    
    
