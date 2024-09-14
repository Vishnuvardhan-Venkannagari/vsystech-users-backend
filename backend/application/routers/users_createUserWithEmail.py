import asyncio
import fastapi
import pydantic
import vsystech_users_models
from firebase_admin import auth,firestore
import datetime
import time
import sys
import os
# sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/")
# import restapi



router = fastapi.APIRouter(prefix='/users')
@router.post("/createUser")
async def createUSerWithEmail(data: vsystech_users_models.Users):
    data = data.model_dump()
    data = data
    # password = await generatePassword()
    password = "password"
    user = auth.create_user(
        email = data["email"],
        email_verified = False,
        password = password,
        display_name = data["name"],
        disabled = False
    )
    db = firestore.client()
    dob = datetime.datetime.strptime(data.get("dob", ""), '%d-%m-%Y')
    epoch_dob = dob.timestamp() * 1000
    created_time = datetime.datetime.now() #+ datetime.timedelta(hours=5,minutes=30)
    created_time = time.mktime(created_time.timetuple())
    user_data = {
        "email": data["email"],
        "isEmailVerified": False,
        "user_id": user.uid,
        "name": data["name"],
        "disabled": False,
        "state": data["state"],
        "dob": epoch_dob,
        "role": "user",
        "phone_number": data.get("phone_number", ""),
        "country": data.get("country", "USA"),
        "photo_url": data.get("photo_url", ""),
        "created_time": created_time,
    }
    db.collection('users').document(user.uid).set(user_data)
    return {"status": "success", "result": user.uid}

