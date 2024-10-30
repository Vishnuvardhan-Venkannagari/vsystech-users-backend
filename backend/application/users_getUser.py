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
    if not user_data.get("photo_url", ""):
        user_data["photo_url"] = "https://media.istockphoto.com/id/1495088043/vector/user-profile-icon-avatar-or-person-icon-profile-picture-portrait-symbol-default-portrait.jpg?s=612x612&w=0&k=20&c=dhV2p1JwmloBTOaGAtaA3AW1KSnjsdMt7-U_3EZElZ0="

    return user_data
    # return await Use.get(id)
