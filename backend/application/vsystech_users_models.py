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
    firstName: str
    lastName: str
    email: str
    phoneNumber: typing.Optional[str]
    gender: typing.Optional[str]
    profilePicture: typing.Optional[str]
    dob: typing.Optional[str]
    state: typing.Optional[str]
    country: typing.Optional[str]

class CreateUsers(pydantic.BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    # phoneNumber: typing.Optional[str]
    # profilePicture: typing.Optional[str]
    # dob: typing.Optional[str]
    # state: typing.Optional[str]

class UpdateUsers(pydantic.BaseModel):
    uid:  str
    firstName: typing.Optional[str] = None
    lastName: typing.Optional[str] = None
    gender: typing.Optional[str] = None
    profilePicture: typing.Optional[str] = None
    dob: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country: typing.Optional[str] = None
    phoneNumber: typing.Optional[str] = None

class loginWithEmail(pydantic.BaseModel):
    email: str
    password: str

class Products(mongomodel.MongoModel):
    # id: str = Field(None, alias="_id")  
    id: typing.Optional[str] = pydantic.Field(**{})
    name: typing.Optional[str] = pydantic.Field(**{})
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

class UserRef(pydantic.BaseModel):
    uid: str
    firstName: str
    lastName: str
    email: str
    phoneNumber: typing.Optional[str] = None

class ProductRef(pydantic.BaseModel):
    id: str = pydantic.Field(**{})
    name: str = pydantic.Field(**{})
    price: float = pydantic.Field(**{})
    img_url: str = pydantic.Field(**{})

class CartItem(mongomodel.MongoModel):
    id: typing.Optional[str] = None
    userData: UserRef
    status: vsystech_users_enum.CartStatus
    is_selected: bool = pydantic.Field()
    productData: ProductRef
    
    class Config:
        db_collection = 'vsystech'
        collection_name = 'cart'

class AddCartItemParams(pydantic.BaseModel):
    product_id: str