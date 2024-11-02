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

@router.get('/{id}', tags=['Users']) #response_model=Users
async def get(id: str):
    get_user = restapi.db.child("users").child(id).get()
    user_data = dict(get_user.val())
    if not user_data.get("profilePicture", ""):
        user_data["profilePicture"] = "https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg"

    return user_data
    # return await Use.get(id)
