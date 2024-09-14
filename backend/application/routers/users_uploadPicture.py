import asyncio
import fastapi
import pydantic
import vsystech_users_models
import sys
import os
from .utilities import upload_to_s3bucket
# sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/")
# import restapi



router = fastapi.APIRouter(prefix='/users')

@router.post('/uploadProfile')
async def uploadProfile():
    # print(upload_to_s3bucket())
    st, msg = await upload_to_s3bucket()
    print(msg)
    return {"status": "success", "msg": "File uploaded"}
