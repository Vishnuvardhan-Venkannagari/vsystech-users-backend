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



router = fastapi.APIRouter(prefix='/users')

@router.post('/updateUser')
async def updateUser():
    # print(upload_to_s3bucket())
    # st, msg = await upload_to_s3bucket()
    # print(msg)
    # print(restapi.set_user)
    return {"status": "success", "msg": "File uploaded"}