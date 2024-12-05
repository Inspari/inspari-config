import os
import azure.keyvault.secrets
import azure.core.exceptions


class MockSecretClient:
    """
    Mock client that returns secrets from a dictionary.
    """

    def __init__(self, vault_url: str, credential=None):  # pylint: disable=unused-argument
        self.vault = vault_url.replace("https://", "").replace(".vault.azure.net", "")

    def get_secret(self, secret_name: str):
        _mock_secrets = {
            "VaultA": {"SecretA": "foo", "SecretB": "bar"},
            "VaultB": {"SecretA": "very_secret"},
        }
        if self.vault not in _mock_secrets:
            raise azure.core.exceptions.ServiceRequestError("Vault not found (mock)")
        return azure.keyvault.secrets._models.KeyVaultSecret(
            None,  # type: ignore
            _mock_secrets[self.vault].get(secret_name, None),
        )


def test_resolve_key_vault_secret():
    azure.keyvault.secrets.SecretClient = MockSecretClient
    from inspari.config.keyvault import resolve_key_vault_secrets

    os.environ["AA"] = "@Microsoft.KeyVault(VaultName=VaultA;SecretName=SecretA)"
    os.environ["AB"] = "@Microsoft.KeyVault(VaultName=VaultA;SecretName=SecretB)"
    os.environ["BA"] = "@Microsoft.KeyVault(VaultName=VaultB;SecretName=SecretA)"
    os.environ["BB"] = "@Microsoft.KeyVault(VaultName=VaultB;SecretName=SecretB)"
    os.environ["CA"] = "@Microsoft.KeyVault(VaultName=VaultC;SecretName=SecretA)"
    resolve_key_vault_secrets()
    # Test EXISTING secrets.
    assert os.environ["AA"] == "foo"
    assert os.environ["AB"] == "bar"
    assert os.environ["BA"] == "very_secret"
    # Test MISSING secret.
    assert (
        os.environ["BB"] == "@Microsoft.KeyVault(VaultName=VaultB;SecretName=SecretB)"
    )
    # Test MISSING vault.
    assert (
        os.environ["CA"] == "@Microsoft.KeyVault(VaultName=VaultC;SecretName=SecretA)"
    )


def test_load_appsettings():
    from inspari.config.appsettings import load_app_settings

    os.environ["APPSETTING_FOO"] = "bar"
    load_app_settings()
    assert os.environ["FOO"] == "bar"
