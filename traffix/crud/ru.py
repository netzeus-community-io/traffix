from typing import List
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from traffix.crud.base import CRUDBase
from traffix.models import RU, RUCreate, RUUpdate


class CRUDRU(CRUDBase[RU, RUCreate, RUUpdate]):
    async def get_by_name(self, db: AsyncIOMotorDatabase, name: str) -> RU:
        """Get a Request/Update from a given name

        Args:
            db:         Motor Async Database Session
            name:       Name of Request
        """
        result = await db[self.collection].find_one({"name": name})
        if not result:
            return None

        return self.model(**result)


ru = CRUDRU(collection="ru", model=RU)
