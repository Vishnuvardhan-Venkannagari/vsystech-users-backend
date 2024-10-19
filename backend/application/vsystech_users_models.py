import typing
import datetime
import fastapi
import pydantic
import shutil
import os
import vsystech_users_enum
from pydantic import BaseModel, Field
import sys
sys.path.append(os.getcwd() + "framework/")
import mongomodel


class Users(pydantic.BaseModel):
    uid:  str
    name: typing.Optional[str]
    email: typing.Optional[str]
    phoneNumber: typing.Optional[str]
    profilePicture: typing.Optional[str]
    dob: typing.Optional[str]
    state: typing.Optional[str]


class loginWithEmail(pydantic.BaseModel):
    email: str
    password: str

class Products(mongomodel.MongoModel):
    # id: str = Field(None, alias="_id")  
    id: str = pydantic.Field(**{})
    name: str = pydantic.Field(**{})
    description: typing.Optional[str] = pydantic.Field(**{})
    short_description: typing.Optional[str] = pydantic.Field(**{})
    price: typing.Optional[int] = pydantic.Field(**{})
    img_url: typing.Optional[str] = pydantic.Field(**{})

    class Config:
        db_collection = 'vsystech'
        collection_name = 'products'
        
class ProductsResponse(pydantic.BaseModel):
    data: typing.List[Products]
    total: int = pydantic.Field(0)
    count: int = pydantic.Field(0)