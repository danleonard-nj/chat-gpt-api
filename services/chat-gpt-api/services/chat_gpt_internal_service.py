import time
import uuid
from typing import Dict

from framework.configuration import Configuration
from framework.logger import get_logger
from httpx import AsyncClient

from data.chat_gpt_internal_repository import ChatGptInternalRepository
from domain.gpt import ChatGptHistoryRecord, InternalChatCompletionRequest
from domain.rest import (ChatGptInternalChatCompletionRequest,
                         ChatGptProxyResponse)
from services.chat_gpt_proxy_service import ChatGptProxyService
from utilities.utils import DateTimeUtil

CONTENT_TYPE = 'application/json'

logger = get_logger(__name__)


class ChatGptInternalService:
    def __init__(
        self,
        configuration: Configuration,
        repository: ChatGptInternalRepository,
        proxy_service: ChatGptProxyService,
        http_client: AsyncClient
    ):
        self.__repository = repository
        self.__proxy_service = proxy_service
        self.__http_client = http_client

        self.__base_url = configuration.chatgpt.get(
            'base_url')
        self.__auth_token = configuration.chatgpt.get(
            'auth_token')

    def __get_headers(
        self
    ) -> Dict:
        return {
            'Authorization': f'Bearer {self.__auth_token}',
            'Content-Type': CONTENT_TYPE
        }

    async def get_chat_completion(
        self,
        req: ChatGptInternalChatCompletionRequest
    ):
        logger.info(f'Get chat completion: {req.to_dict()}')

        start = time.time()
        req = InternalChatCompletionRequest(
            prompt=req.prompt)

        response = await self.__http_client.request(
            url=f'{self.__base_url}/v1/chat/completions',
            method='POST',
            json=req.to_dict(),
            headers=self.__get_headers())

        logger.info(f'Status: {response.status_code}')

        end = time.time()

        result = ChatGptProxyResponse(
            request_body=req.to_dict(),
            response=response,
            duration=round(end - start, 2))

        logger.info(f'Response: {result.to_dict()}')

        record = ChatGptHistoryRecord(
            history_id=str(uuid.uuid4()),
            endpoint='/v1/chat/completions',
            method='POST',
            response=result.to_dict(),
            created_date=DateTimeUtil.timestamp())

        logger.info(f'Record: {record.to_dict()}')

        inserted = await self.__repository.insert(
            document=record.to_dict())

        logger.info(f'Inserted: {inserted.inserted_id}')

        return result
