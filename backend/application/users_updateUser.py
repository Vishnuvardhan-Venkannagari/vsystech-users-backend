import asyncio
import fastapi
import pydantic
import vsystech_users_models
import sys
import os
# from .utilities import upload_to_s3bucket
# sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/")
# import restapi
sys.path.append(os.getcwd() + "/framework")
import restapi
from vsystech_users_models import Users



router = fastapi.APIRouter(prefix='/users',  tags=['Users'])

@router.post('/updateUser')
async def updateUser(data: vsystech_users_models.UpdateUsers):
    update_doc = {}
    data = data.model_dump()
    data["country"] = "USA"
    if data.get("firstName"):
        update_doc["firstName"] = data["firstName"]
    if data.get("lastName"):
        update_doc["lastName"] = data["lastName"]
    if data.get("gender"):
        update_doc["gender"] = data["gender"]
    if data.get("dob"):
        update_doc["dob"] = data["dob"]
    if data.get("state"):
        update_doc["state"] = data["state"]
    if data.get("phoneNumber"):
        update_doc["phoneNumber"] = data["phoneNumber"]
    if data.get("country"):
        update_doc["country"] = data["country"]
    if data.get("profilePicture"):
        update_doc["profilePicture"] = data["profilePicture"]
    else:
        print("insdie else")
        update_doc["profilePicture"] = "https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"
    if update_doc:
        restapi.db.child("users").child(data["uid"]).update(update_doc)
    user_data = restapi.db.child("users").child(data["uid"]).get()
    return {"status": "success", "data":dict(user_data.val())}
