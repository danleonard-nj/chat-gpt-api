from framework.mongo.mongo_repository import MongoRepositoryAsync
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DATABASE_NAME = 'ChatGPT'
MONGO_COLLECTION_NAME = 'Internal'


class ChatGptInternalRepository(MongoRepositoryAsync):
    def __init__(
        self,
        client: AsyncIOMotorClient
    ):
        super().__init__(
            client=client,
            database=MONGO_DATABASE_NAME,
            collection=MONGO_COLLECTION_NAME)
