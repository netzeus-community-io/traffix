from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from bson.objectid import ObjectId

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, collection: AsyncIOMotorCollection, model: Type[ModelType]):
        self.collection = collection
        self.model = model

    async def get(self, db: AsyncIOMotorDatabase, id: str) -> Optional[ModelType]:
        """Get a single Record from the Mongo Database

        Args:
            db:     Database Session
            id:     Mongo Record _id
        """
        result = await db[self.collection].find_one({"_id": ObjectId(id)})
        if not result:
            return None
        return self.model(**result)

    async def get_multi(
        self,
        db: AsyncIOMotorDatabase,
        skip: int = 0,
        limit: int = 100,
        query: dict = {},
    ) -> Optional[List[ModelType]]:
        """Gets multiple Records from the Database

        Args:
            db:     Database Session
            skip:   Offsets number of documents to skip
            limit:  Maximum number of documents to return
            query:  Optional query to filter the collection
        """
        results = await db[self.collection].find(query).skip(skip).to_list(length=limit)
        if not results:
            return []

        return [self.model(**result) for result in results]

    async def create(
        self, db: AsyncIOMotorDatabase, obj_in: CreateSchemaType
    ) -> ModelType:
        """Create a record in the database

        Note that jsonable_encoder is used to handle non-jsonable fields which
        are not handled by the pydantic model

        Args:
            db:     Database Session
            obj_in: Pydantic Object to create in Database
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        result = await db[self.collection].insert_one(
            # db_obj.model_dump(by_alias=True, exclude_unset=True) #Looks like a V2 code change
            db_obj.dict(by_alias=True, exclude_unset=True)
        )
        refreshed_object = await self.get(db=db, id=result.inserted_id)
        return refreshed_object

    async def create_many(
        self, db: AsyncIOMotorDatabase, objs_in: List[CreateSchemaType]
    ) -> ModelType:
        """Creates multiple records in the database (bulk)

        Note that jsonable_encoder is used to handle non-jsonable fields which
        are not handled by the pydantic model

        Args:
            db:         Database Session
            objs_in:    Pydantic Object(s) to create in Database
        """
        objs = []
        for obj_in in objs_in:
            obj_in_data = jsonable_encoder(obj_in)
            objs.append(self.model(**obj_in_data))

        result = await db[self.collection].insert_many([obj.dict() for obj in objs])
        return result

    async def update(
        self,
        *,
        db: AsyncIOMotorDatabase,
        id: str,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Updates an existing record if it exist, doesn't create if not found

        Args:
            db:     Database Session
            id:     _id of existing MongoDB record
            db_obj: Existing DB Object to update fields from
            obj_in: Pydantic Object with new data in
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_none=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        updated_result = await db[self.collection].update_one(
            {"_id": ObjectId(id)}, {"$set": db_obj.dict()}
        )

        if updated_result.matched_count == 0:
            return None

        refreshed_object = await self.get(db=db, id=id)
        return refreshed_object

    async def delete(self, db: AsyncIOMotorDatabase, id: str) -> ModelType:
        """Delete a MongoDB record based on the _id

        Args:
            db:     Database Session
            id:     _id of existing MongoDB record
        """
        obj = await db[self.collection].delete_one({"_id": ObjectId(id)})
        return obj
