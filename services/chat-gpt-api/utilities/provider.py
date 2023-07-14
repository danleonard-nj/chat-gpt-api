from typing import List

from framework.auth.azure import AzureAd
from framework.auth.configuration import AzureAdConfiguration
from framework.clients.cache_client import CacheClientAsync
from framework.configuration.configuration import Configuration
from framework.di.service_collection import ServiceCollection
from framework.di.static_provider import ProviderBase
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from clients.event_client import EventClient
from clients.identity_client import IdentityClient
from clients.storage_client import StorageClient
from data.chat_gpt_internal_repository import ChatGptInternalRepository
from data.chat_gpt_repository import ChatGptRepository
from services.chat_gpt_internal_service import ChatGptInternalService
from services.chat_gpt_proxy_service import ChatGptProxyService


class AdRole:
    Read = 'ChatGpt.Read'
    Write = 'ChatGpt.Write'


def has_role(
    token_roles: List[str],
    required_role: str
) -> bool:
    return any([
        role == required_role
        for role in token_roles
    ])


def configure_azure_ad(service_descriptors):
    configuration = service_descriptors.resolve(Configuration)

    # Hook the Azure AD auth config into the service
    # configuration
    ad_auth: AzureAdConfiguration = configuration.ad_auth
    azure_ad = AzureAd(
        tenant=ad_auth.tenant_id,
        audiences=ad_auth.audiences,
        issuer=ad_auth.issuer)

    azure_ad.add_authorization_policy(
        name='read',
        func=lambda t: has_role(
            token_roles=t.get('roles', []),
            required_role=AdRole.Read))

    azure_ad.add_authorization_policy(
        name='write',
        func=lambda t: has_role(
            token_roles=t.get('roles', []),
            required_role=AdRole.Write))

    return azure_ad


def configure_mongo_client(service_provider):
    configuration = service_provider.resolve(Configuration)

    connection_string = configuration.mongo.get('connection_string')
    client = AsyncIOMotorClient(connection_string)

    return client


def configure_http_client(
    container: ServiceCollection
):
    return AsyncClient(timeout=None)


class ContainerProvider(ProviderBase):
    @classmethod
    def configure_container(cls):
        service_descriptors = ServiceCollection()

        service_descriptors.add_singleton(Configuration)
        service_descriptors.add_singleton(
            dependency_type=AzureAd,
            factory=configure_azure_ad)

        service_descriptors.add_singleton(
            dependency_type=AsyncClient,
            factory=configure_http_client)

        service_descriptors.add_singleton(
            dependency_type=AsyncIOMotorClient,
            factory=configure_mongo_client)

        service_descriptors.add_singleton(CacheClientAsync)
        service_descriptors.add_singleton(EventClient)
        service_descriptors.add_singleton(IdentityClient)
        service_descriptors.add_singleton(StorageClient)

        # Repositories
        service_descriptors.add_singleton(ChatGptRepository)
        service_descriptors.add_singleton(ChatGptInternalRepository)

        # Services
        service_descriptors.add_transient(ChatGptProxyService)
        service_descriptors.add_transient(ChatGptInternalService)

        return service_descriptors
