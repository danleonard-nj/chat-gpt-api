from framework.rest.blueprints.meta import MetaBlueprint
from quart import request

from domain.rest import ChatGptInternalChatCompletionRequest
from services.chat_gpt_internal_service import ChatGptInternalService

internal_bp = MetaBlueprint('internal_bp', __name__)


@internal_bp.configure('/api/internal/chat/completions', methods=['POST'], auth_scheme='read')
async def post_completions(container):
    service: ChatGptInternalService = container.resolve(
        ChatGptInternalService)

    body = await request.get_json()

    req = ChatGptInternalChatCompletionRequest(
        data=body)

    return await service.get_chat_completion(
        req=req)
