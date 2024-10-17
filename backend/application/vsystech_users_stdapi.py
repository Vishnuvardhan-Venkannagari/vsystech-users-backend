import asyncio
import fastapi
import pydantic
# from bson import ObjectId
import vsystech_users_models
# import application.routers.usermanagement as usermanagement
import sys
import os
import pkgutil
import importlib
import traceback
sys.path.append(os.getcwd()+'/framework')
# sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/")
import framework
# sys.path.append("/opt/vsystech-users-backend/backend/framework")
import restapi
from vsystech_users_models import *

router = fastapi.APIRouter(prefix='')
# app = fastapi.FastAPI(version='1.0.0',
#                       description=f"RestAPI for VSYSTECH Platform",
#                       title="RestApi")
# package_dir = os.getcwd() #+ "/application"
# sys.path.append(os.path.abspath(package_dir))
# @app.on_event("startup")
# def onStart():
#     for module_info in pkgutil.iter_modules([str(package_dir)]):
#         module = importlib.import_module(f'{module_info.name}')#routers.
#         if hasattr(module, 'router'):
#             app.include_router(module.router, prefix="/api")


# @router.get("/secure-data")
# async def secure_data():
#     return {"status": "success", "msg": "This is a secured data"}

# router = fastapi.APIRouter(prefix='/users')

@router.get('/products', response_model=ProductsResponse, tags=['Products'])
async def get_all(response: fastapi.Response, params = fastapi.Depends(framework.queryparams.QueryParams)):
    if params.download:
        response.headers['Content-Disposition'] = f'attachment; filename="reviews.html"'
    return await Products.get_all(params)

@router.get('/products/{id}', response_model=Products, tags=['Products'])
async def get(id: str):
    return await Products.get(id)

@router.post('/products', response_model=Products, tags=['Products'])
async def create(inputObj: Products):
    return await Products.create(inputObj)
