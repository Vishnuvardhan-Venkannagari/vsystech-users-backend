import typing
import json
import framework.redispool
import framework.queryparams
import pymongo
from pydantic.fields import Field
import pydantic
from datetime import datetime, date
import bson
import motor.motor_asyncio

class BaseMongoModel(pydantic.BaseModel):
    
    @classmethod
    def client(cls) -> motor.motor_asyncio.AsyncIOMotorClient:
        return motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    
    @classmethod
    def db(cls) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        return cls.client()[cls.database_name()]

    @classmethod
    def collection(cls) -> motor.motor_asyncio.AsyncIOMotorCollection:
        return cls.db()[cls.collection_name()]

    @classmethod
    def collection_name(cls) -> str:
        return cls.Config.collection_name if hasattr(cls.Config, 'collection_name') else cls.__name__.lower()
        # return cls.__config__.db_collection if cls.__config__.db_collection else cls.__name__.lower()

    @classmethod
    def database_name(cls) -> str:
        return cls.Config.db_collection if hasattr(cls.Config, 'db_collection') else cls.__name__.lower()
        # return cls.__config__.collection_name if cls.__config__.collection_name else cls.__name__.lower()
    
    @classmethod
    def from_mongo(cls, data: dict):
        """We must convert _id into "id". """
        if not data:
            return data
        # id = data.pop('_id', None)
        if '_id' in data:
            data['_id'] = str(data['_id'])
        if 'id' in data:
            data['id'] = str(data['id'])
        if 'tid' in data:
            data['tid'] = str(data['tid'])
    
        return cls(**dict(data))

    def to_mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', True)
        by_alias = kwargs.pop('by_alias', True)
        exclude = kwargs.pop('exclude', set())
        exclude.union({'created', 'updated', 'tenantId'})

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            exclude=exclude,
            **kwargs,
        )

        # Mongo uses `_id` as default key. We should stick to that as well.
        # if '_id' not in parsed and 'id' in parsed:
        #     parsed['_id'] = parsed.pop('id')

        return parsed

    async def create(self):
        try:
            data = self.to_mongo(exclude_unset=False, exclude_none=True)
            print(data)
            data['c'] = data['u'] = datetime.utcnow()
            data['tid'] = bson.ObjectId()
            data["id"] = data["tid"]
            data["_id"] = data["tid"]
            inserted_doc = await self.collection().insert_one(data)
            collection = self.collection().with_options(read_preference=pymongo.ReadPreference.PRIMARY)
            resp = await collection.find_one(inserted_doc.inserted_id)
            return self.from_mongo(resp)
        except pymongo.errors.DuplicateKeyError as e:
            print("Duplicate")


    async def update(self):
        try:
            data = self.to_mongo()
            data['u'] = datetime.utcnow()
            updated_doc = await self.collection().update_one({'_id':bson.ObjectId(self.id)}, {'$set': data})
            collection = self.collection().with_options()
            resp = await collection.find_one(self.id)
            return self.from_mongo(resp)
        except pymongo.errors.DuplicateKeyError as e:
            print("Duplicate")
    
    @classmethod
    async def get(cls, id):
        resp = await cls.collection().find_one(bson.ObjectId(id))
        return cls.from_mongo(resp)
    
    @classmethod
    async def get_all(cls, params: framework.queryparams.QueryParams):
        mongoquery = {"collation": {"locale": "en"}}
        if params.q:
            mongoquery["filter"] = json.loads(params.q)
        else:
            mongoquery["filter"] = {}
        if params.fields:
            mongoquery['projection'] = list(set(json.loads(params.fields) + ["tid"]))
        cursor = cls.collection().find(**mongoquery, sort=None)
        resp = {}
        cursor.skip(params.skip)
        cursor.limit(params.limit)
        data = await cursor.to_list(length=None)
        resp["total"] = await cursor.collection.count_documents(**mongoquery)
        resp["current"] = len(data)
        for index, rec in enumerate(data):
            data[index]['tid'] = str(data[index]['tid'])
            data[index]['_id'] = str(data[index]['_id'])
            data[index]['id'] = str(data[index]['id'])
        resp['data'] = data
        return resp
    
    @classmethod
    async def delete(cls, id):
        resp = await cls.collection().delete_one({'_id': bson.ObjectId(id)})
        return True

    @classmethod
    async def createIndex(cls, fieldSpec, unique=False):
        return await cls.collection().create_index(fieldSpec, background=True, unique=unique)

    class Config:
        populate_by_name = True
        json_encoders = {
            bson.ObjectId: str
        }
        collection_name: None

class MongoModel(BaseMongoModel):
    id: typing.Optional[str] = Field(alias='_id')
    created: typing.Optional[datetime] = Field(alias='c')
    updated: typing.Optional[datetime] = Field(alias='u')
    tenantId: typing.Optional[str] = Field(alias='tid')

