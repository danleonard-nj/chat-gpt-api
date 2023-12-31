from typing import Tuple
from framework.rest.blueprints.meta import MetaBlueprint
from quart import request

from services.chat_gpt_proxy_service import ChatGptProxyService

chatgpt_bp = MetaBlueprint('chatgpt_bp', __name__)


def get_history_args() -> Tuple[str, str, str]:
    return (
        request.args.get('start_timestamp'),
        request.args.get('end_timestamp'),
        request.args.get('endpoint')
    )


def get_usage_args() -> Tuple[str, str]:
    return (
        request.args.get('start_date'),
        request.args.get('end_date')
    )


@chatgpt_bp.configure('/api/chatgpt/completions', methods=['POST'], auth_scheme='write')
async def post_completions(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    body = await request.get_json()

    return await service.proxy_request(
        endpoint='/v1/completions',
        method='POST',
        request_body=body)


@chatgpt_bp.configure('/api/chatgpt/chat/completions', methods=['POST'], auth_scheme='write')
async def post_chat_completions(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    body = await request.get_json()

    return await service.proxy_request(
        endpoint='/v1/chat/completions',
        method='POST',
        request_body=body)


@chatgpt_bp.configure('/api/chatgpt/engines', methods=['GET'], auth_scheme='read')
async def get_engines(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    return await service.proxy_request(
        endpoint='/v1/engines',
        method='GET')


@chatgpt_bp.configure('/api/chatgpt/models', methods=['GET'], auth_scheme='read')
async def get_models(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    return await service.proxy_request(
        endpoint='/v1/models',
        method='GET')


@chatgpt_bp.configure('/api/chatgpt/images/generations', methods=['POST'], auth_scheme='write')
async def post_generate_images(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    body = await request.get_json()

    return await service.proxy_request(
        endpoint='/v1/images/generations',
        method='POST',
        request_body=body)


@chatgpt_bp.configure('/api/chatgpt/images/edits', methods=['POST'], auth_scheme='write')
async def post_generate_image_edit(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    body = await request.get_json()

    return await service.proxy_request(
        endpoint='/v1/images/edits',
        method='POST',
        request_body=body)


@chatgpt_bp.configure('/api/chatgpt/usage', methods=['GET'], auth_scheme='read')
async def get_usage(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    start_date, end_date = get_usage_args()

    return await service.get_usage(
        start_date=start_date,
        end_date=end_date)


@chatgpt_bp.configure('/api/chatgpt/history', methods=['GET'], auth_scheme='read')
async def get_history(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    (start_timestamp,
     end_timestamp,
     endpoint) = get_history_args()

    return await service.get_history(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        endpoint=endpoint)


@chatgpt_bp.configure('/api/chatgpt/history/endpoints', methods=['GET'], auth_scheme='read')
async def get_history_grouped(container):
    service: ChatGptProxyService = container.resolve(
        ChatGptProxyService)

    (start_timestamp,
     end_timestamp,
     endpoint) = get_history_args()

    return await service.get_endpoint_history(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        endpoint=endpoint)
