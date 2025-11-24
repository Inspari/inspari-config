import logging
import os
import re
from typing import TypeVar

import azure.core.exceptions
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic_settings import BaseSettings


"""
This module holds parsing logic for Azure Key Vault secrets.
"""

logger = logging.getLogger(__name__)

_keyvault_pattern = re.compile(
    r"^@Microsoft.KeyVault\(VaultName=(.*);SecretName=(.*)\)$"
)


def resolve_key_vault_secrets(
    credential: DefaultAzureCredential | None = None, client_cache: dict[str, SecretClient] | None = None
) -> None:
    """
    This function replaces azure key vault references in the form of
    "@Microsoft.KeyVault(VaultName=...;SecretName=...)" with the actual secret value.
    """
    credential = DefaultAzureCredential() if credential is None else credential
    for key in os.environ:
        secret = resolve_key_vault_secret(
            os.environ[key], client_cache=client_cache, credential=credential
        )
        if secret is None:
            continue
        os.environ[key] = secret


def resolve_key_vault_secret(
    reference: str,
    client_cache: dict[str, SecretClient] | None = None,
    credential: DefaultAzureCredential | None = None,
) -> str | None:
    match = _keyvault_pattern.match(reference)
    if match is None:
        return None
    vault = match.group(1)
    client = None if client_cache is None else client_cache.get(vault)
    if client is None:
        vault_url = f"https://{vault}.vault.azure.net"
        credential = DefaultAzureCredential() if credential is None else credential
        client = SecretClient(vault_url=vault_url, credential=credential)
        if client_cache is not None:
            client_cache[vault] = client
    secret_name = match.group(2)
    try:
        return client.get_secret(secret_name).value
    except azure.core.exceptions.ServiceRequestError:
        logger.warning(f"Key vault not found during secret resolution: {vault}")
        return None


settings_type = TypeVar("settings_type", bound=BaseSettings)

def parse_keyvault_references_in_settings(
        settings: settings_type, 
        credential: DefaultAzureCredential | None = None, 
        client_cache: dict[str, SecretClient] | None = None,
    ) -> settings_type:
    """This function parses all values in a BaseSettings object and pulls secret references from KeyVaults
    if the setting follows the pattern:
    "@Microsoft.KeyVault(VaultName=...;SecretName=...)"
    """
    replaced_secrets: list[str] = list()
    for f,val in settings:
        secret_val = resolve_key_vault_secret(reference=val, credential=credential, client_cache=client_cache)
        if secret_val is not None:
            setattr(settings, f, secret_val)
            replaced_secrets.append(f)
    logger.info(f"Fetched secrets: {replaced_secrets} from keyvault for {settings.__class__}")
    return settings
