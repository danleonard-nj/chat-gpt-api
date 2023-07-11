from framework.exceptions.nulls import ArgumentNullException
from framework.mongo.mongo_repository import MongoRepositoryAsync
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_DATABASE_NAME='ChatGPT'
MONGO_COLLECTION_NAME='History'

class ChatGptRepository(MongoRepositoryAsync):
    def __init__(
        self,
        client: AsyncIOMotorClient
    ):
        super().__init__(
            client=client,
            database=MONGO_DATABASE_NAME,
            collection=MONGO_COLLECTION_NAME)

    async def get_history(
        self,
        start_timestamp,
        end_timestamp,
        endpoint: str = None
    ):
        ArgumentNullException.if_none(start_timestamp, 'start_timestamp')
        ArgumentNullException.if_none(end_timestamp, 'end_timestamp')

        query_filter = {
            'created_date': {
                '$gte': start_timestamp,
                '$lt': end_timestamp
            }
        }

        if endpoint is not None:
            query_filter['endpoint'] = endpoint

        results = self.collection.find(
            filter=query_filter)

        return await results.to_list(
            length=None)
