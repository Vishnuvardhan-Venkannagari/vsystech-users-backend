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
    firstName: typing.Optional[str] = pydantic.Field("")
    lastName: typing.Optional[str] = pydantic.Field("")
    gender: typing.Optional[str] = pydantic.Field("")
    profilePicture: typing.Optional[str] = pydantic.Field("")
    dob: typing.Optional[str] = pydantic.Field("")
    state: typing.Optional[str] = pydantic.Field("")
    country: typing.Optional[str] = pydantic.Field("")
    phoneNumber: typing.Optional[str] = pydantic.Field("")

class loginWithEmail(pydantic.BaseModel):
    email: str
    password: str

class AttributesRef(pydantic.BaseModel):
    color: typing.Optional[str] = pydantic.Field("")
    model: typing.Optional[str] = pydantic.Field("")
    material: typing.Optional[str] = pydantic.Field("")

class Products(mongomodel.MongoModel):
    # id: str = Field(None, alias="_id")  
    id: typing.Optional[str] = pydantic.Field("")
    name: typing.Optional[str] = pydantic.Field("")
    brand: typing.Optional[str] = pydantic.Field("")
    status: typing.Optional[vsystech_users_enum.ProductStatus] = pydantic.Field("")
    category: typing.Optional[str] = pydantic.Field("")
    sku_id: typing.Optional[str] = pydantic.Field("")
    description: typing.Optional[str] = pydantic.Field("")
    short_description: typing.Optional[str] = pydantic.Field("")
    stock_quantity: typing.Optional[int] = pydantic.Field(0)
    price: typing.Optional[int] = pydantic.Field("")
    img_url: typing.Optional[str] = pydantic.Field("")
    thumbnail_image_url: typing.Optional[str] = pydantic.Field("")
    attributes: typing.Optional[AttributesRef] = pydantic.Field({})

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
    img_url: typing.Optional[str] = pydantic.Field(**{})

class CartItem(mongomodel.MongoModel):
    id: typing.Optional[str] = pydantic.Field("")
    userData: UserRef = pydantic.Field({})
    status: vsystech_users_enum.CartStatus = pydantic.Field(**{})
    is_selected: bool  = pydantic.Field(False)
    productData: ProductRef = pydantic.Field("")
    
    class Config:
        db_collection = 'vsystech'
        collection_name = 'cart'

class CartItemResponse(pydantic.BaseModel):
    data: typing.List[CartItem]
    total: int = pydantic.Field(0)
    count: int = pydantic.Field(0)


class AddCartItemParams(pydantic.BaseModel):
    product_id: str

class RemoveCartItemParams(pydantic.BaseModel):
    cart_item_id: str

class GatewayRef(pydantic.BaseModel):
    gateway_name: str = pydantic.Field("")
    base_url: str = pydantic.Field("")
    api_key: str = pydantic.Field("")
    api_secret: str = pydantic.Field("")

class PaymentGateway(mongomodel.MongoModel):
    id: typing.Optional[str] = pydantic.Field("")
    gateway: GatewayRef = pydantic.Field("")
    is_verified: bool = pydantic.Field(False)
    veifiedBy: UserRef = pydantic.Field(**{})

    class Config:
        db_collection = 'vsystech'
        collection_name = 'paymentgateway'

class PaymentGatewayParams(pydantic.BaseModel):
    gateway_name: str = pydantic.Field("")
    api_key: str = pydantic.Field("")
    api_secret: str = pydantic.Field("")


class PaymentProductRef(pydantic.BaseModel):
    id: str = pydantic.Field(**{})
    name: str = pydantic.Field(**{})
    price: float = pydantic.Field(**{})

class RefundedByUserRef(pydantic.BaseModel):
    uid: typing.Optional[str] = pydantic.Field("")
    firstName: typing.Optional[str] = pydantic.Field("")
    lastName: typing.Optional[str] = pydantic.Field("")
    email: typing.Optional[str] = pydantic.Field("")
    phoneNumber: typing.Optional[str] = pydantic.Field("")


class Payments(mongomodel.MongoModel):
    id: typing.Optional[str] = pydantic.Field("")
    gateway_name: str = pydantic.Field("")
    order_id: typing.Optional[str] = pydantic.Field("")
    payment_url: typing.Optional[str] = pydantic.Field("")
    approve_url: typing.Optional[str] = pydantic.Field("")
    payment_id: typing.Optional[str] = pydantic.Field("")
    payment_status: typing.Optional[vsystech_users_enum.PaymentStatus] = pydantic.Field("")
    order_amt: float = pydantic.Field(0.0)
    shipping_amt: typing.Optional[float] = pydantic.Field(0.0)
    cart_amt: typing.Optional[float] = pydantic.Field(0.0)
    tax: typing.Optional[float] = pydantic.Field(0.0)
    paypal_fees: typing.Optional[float] = pydantic.Field(0.0)
    paid_amt: typing.Optional[float] = pydantic.Field(0.0)
    is_refunded: bool = pydantic.Field(False)
    refund_id: typing.Optional[str] = pydantic.Field("")
    refunded_amt: float = pydantic.Field(0.0)
    refunded_on: typing.Optional[str] = pydantic.Field("")
    refunded_by: typing.Optional[RefundedByUserRef] = None
    products: typing.Optional[typing.List[PaymentProductRef]] = pydantic.Field({})
    userData: typing.Optional[UserRef] = pydantic.Field({})
    currency: typing.Optional[str] = pydantic.Field("")

    class Config:
        db_collection = 'vsystech'
        collection_name = 'payments'


class PaymentCreatePayment(pydantic.BaseModel):
    gateway_name: str = pydantic.Field(**{})
    totla_price: float = pydantic.Field(0.0)
    # order_amt: float = pydantic.Field(**{})

class PaymentVerifyPayment(pydantic.BaseModel):
    payment_id: str = pydantic.Field("")
    # order_amt: float = pydantic.Field(**{})

class UserPurchase(mongomodel.MongoModel):
    id: typing.Optional[str] = pydantic.Field("")
    payment_id: str = pydantic.Field("")
    order_date: typing.Optional[datetime.datetime] = pydantic.Field("")
    delivery_date: typing.Optional[datetime.datetime] = pydantic.Field("")
    returned: bool = pydantic.Field(False)
    is_delivered: bool = pydantic.Field(False)
    product_image: str = pydantic.Field("")
    tracking_id: typing.Optional[str] = pydantic.Field("")
    product: typing.Optional[PaymentProductRef] = pydantic.Field({})
    userData: typing.Optional[UserRef] = pydantic.Field({})

    class Config:
        db_collection = 'vsystech'
        collection_name = 'userpurchase'
