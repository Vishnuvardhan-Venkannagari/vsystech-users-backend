import asyncio
import fastapi
import pydantic
import vsystech_users_models
import sys
import os
# from .utilities import upload_to_s3bucket
sys.path.append(os.getcwd() + "/framework/")
import context



router = fastapi.APIRouter(prefix='/users')

@router.post('/uploadProfile')
async def uploadProfile():
    auth_user = context.context.get('auth_user', {})
    return {"status": "success", "msg": auth_user}
