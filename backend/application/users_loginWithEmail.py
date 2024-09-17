# import asyncio
# import fastapi
# import pydantic
# import vsystech_users_models
# from firebase_admin import credentials,auth,firestore,initialize_app
# import datetime
# import time
# import sys
# import os
# sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/")
# import restapi

# router = fastapi.APIRouter(prefix='/users')

# @router.post("/loginWithEmail")
# async def loginWithEmail(data: vsystech_users_models.loginWithEmail, response: fastapi.Response):
#     data = data.model_dump()
#     result =  await restapi.userLogin(data)
#     # response.headers["Authorization"] = f"Bearer {result['token']}"
#     # headers_dict = dict(response.headers.items())
#     print(result)
#     return result
