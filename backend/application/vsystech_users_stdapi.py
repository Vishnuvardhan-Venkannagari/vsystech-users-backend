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
sys.path.append("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/")
import restapi

app = fastapi.FastAPI(version='1.0.0',
                      description=f"RestAPI for VSYSTECH Platform",
                      title="RestApi")
package_dir = '/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/application/routers'

for module_info in pkgutil.iter_modules([str(package_dir)]):
    module = importlib.import_module(f'routers.{module_info.name}')
    if hasattr(module, 'router'):
        app.include_router(module.router)

router = fastapi.APIRouter(prefix='/secure-data')

@router.get("/")
async def secure_data():
    return {"status": "success", "msg": "This is a secured data"}

app.include_router(router)