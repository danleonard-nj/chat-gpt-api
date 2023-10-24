import hashlib
import json
import time
import uuid
from datetime import datetime
from hashlib import md5

import urllib3
from framework.logger.providers import get_logger

# Image request headers
IMAGE_ENDPOINT = '/v1/images/generations'
HOST = 'oaidalleapiprodscus.blob.core.windows.net'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
CONTENT_TYPE_ALL = '*/*'

IMAGE_HEADERS = {
    'Host': HOST,
    'User-Agent': USER_AGENT,
    'Accept': ACCEPT,
    'Content-Type': CONTENT_TYPE_ALL
}

logger = get_logger(__name__)


def decode_url(url: str) -> str:
    return urllib3.parse.unquote(url)


class DateTimeUtil:
    IsoDateTimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
    IsoDateFormat = '%Y-%m-%d'

    @staticmethod
    def timestamp() -> int:
        return int(time.time())

    @classmethod
    def get_iso_date(
        cls
    ) -> str:
        return (
            datetime
            .now()
            .strftime(cls.IsoDateFormat)
        )

    @staticmethod
    def iso_from_timestamp(timestamp: int) -> str:
        return (
            datetime
            .fromtimestamp(timestamp)
            .isoformat()
        )


class KeyUtils:
    @staticmethod
    def create_uuid(**kwargs):
        digest = hashlib.md5(json.dumps(
            kwargs,
            default=str).encode())

        return str(uuid.UUID(digest.hexdigest()))


# class ValueConverter:
#     MegabyteInBytes = 1048576

#     @classmethod
#     def bytes_to_megabytes(
#         cls,
#         bytes,
#         round_result=True
#     ) -> Union[int, float]:

#         if bytes == 0:
#             return 0

#         result = bytes / cls.MegabyteInBytes

#         return (
#             round(result) if round_result
#             else result
#         )


# def parse_bool(value):
#     return value == 'true'


# def contains(source_list, substring_list):
#     for source_string in source_list:
#         for substring in substring_list:
#             if substring in source_string:
#                 return True
#     return False


def create_uuid(data):
    text = json.dumps(data, default=str)
    hash_value = md5(text.encode()).hexdigest()
    return str(uuid.UUID(hash_value))


# def get_sort_key(obj, key):
#     if isinstance(obj, dict):
#         return obj[key]
#     return getattr(obj, key)


# def sort_by(items, key):
#     if any(items):
#         logger.info(f'Sort type: {type(items[0]).__name__}: Key: {key}')
#         return sorted(items, key=lambda x: get_sort_key(x, key))
