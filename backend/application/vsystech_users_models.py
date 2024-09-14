import typing
import datetime
import fastapi
import pydantic
import shutil
import os
import vsystech_users_enum



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