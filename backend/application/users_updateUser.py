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

@router.post('/updateUser' ,response_model=Users)
async def updateUser():
    # print(upload_to_s3bucket())
    # st, msg = await upload_to_s3bucket()
    # print(msg)
    # print(restapi.set_user)
    return {"status": "success", "msg": "File uploaded"}
