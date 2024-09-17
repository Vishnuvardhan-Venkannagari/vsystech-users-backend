# import fastapi
# import sys
# import datetime
# import requests
# import time
# import os
# import uuid
# import json
# import httpx
# import base64
# import typing
# import importlib
# from fastapi.middleware.cors import CORSMiddleware
# from firebase_admin import credentials,auth,firestore,initialize_app
# sys.path.append("../framework")
# # cred = credentials.Certificate("/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/framework/vsystech-users-firebase-adminsdk-w3tk9-f514a70a29.json")
# # default_app = initialize_app(cred)


# async def createUserWithEmailAndPassword(data):
#     data = data
#     # password = await generatePassword()
#     password = "password"
#     user = auth.create_user(
#         email = data["email"],
#         email_verified = False,
#         password = password,
#         display_name = data["name"],
#         disabled = False
#     )
#     db = firestore.client()
#     dob = datetime.datetime.strptime(data.get("dob", ""), '%d-%m-%Y')
#     epoch_dob = dob.timestamp() * 1000
#     created_time = datetime.datetime.now() #+ datetime.timedelta(hours=5,minutes=30)
#     created_time = time.mktime(created_time.timetuple())
#     user_data = {
#         "email": data["email"],
#         "isEmailVerified": False,
#         "user_id": user.uid,
#         "name": data["name"],
#         "disabled": False,
#         "state": data["state"],
#         "dob": epoch_dob,
#         "role": "user",
#         "phone_number": data.get("phone_number", ""),
#         "country": data.get("country", "USA"),
#         "photo_url": data.get("photo_url", ""),
#         "created_time": created_time,
#     }
#     db.collection('users').document(user.uid).set(user_data)
#     return {"status": "success", "result": user.uid}

import boto3
from dotenv import load_dotenv
import os
import typing
import uuid

load_dotenv('/Users/vishnureddy/Documents/MyProjects/vsystech-user-app/opt/backend/application/.env')

async def upload_to_s3bucket(bucketName, filedata, file_extension, Acls: str = 'public-read'):#, metadata: typing.Any = None, ):
    # Creating Session With Boto3.
    session = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key"),
        aws_secret_access_key=os.getenv("aws_secret_key")
    )
    # Creating S3 Resource From the Session.
    client = session.client('s3')
    s3 = session.resource('s3')
    extra_args = {}
    # if metadata:
    #     extra_args["Metadata"] = metadata
    if Acls:
        extra_args.update(Acls)
    object_name = f'{str(uuid.uuid4()).replace("-", "")}.{file_extension}'
    s3object = s3.Object(bucketName, object_name)
    response = s3object.put(Body=filedata, ACL=Acls)
    if not response or response['ResponseMetadata']['HTTPStatusCode'] != 200:
        return False, "Error in saving file content"
    location = client.get_bucket_location(Bucket=bucketName)[
        'LocationConstraint']
    return True, f"https://{bucketName}.s3.{location}.amazonaws.com/{object_name}"
