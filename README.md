This repository provides Python configuration utilities.

### Usage

The most common usage pattern is to create a `config.py` file that _defines_ the configuration. The configuration itself
is parsed from environment variables. They are typically read from a `.env` file during local development.

A minimal example is bundled, with the configuration defined in `example_config.py`, a few variables in `example.env`, 
and the typical access pattern (i.e. how settings are access in application code) illustrated in `example_usage.py`.

### Usage with Keyvault

An especially nice features is the ability to refer to secrets in a Keyvault without committing them to git. All you need to do is add a variable to your .env file like

```
MY_SECRET="@Microsoft.KeyVault(VaultName=<keyvaultname>,SecretName=<my-secret>)"
```
where keyvaultname is the name (not fqdn) of a keyvault that you have access to eg. by doing `az login` and my-secret is the relevant name of the secret.
Remember that keys can not have underscores but dashes are allowed, whereas it's the opposite for the environment variables.

### Development

Create a new Python environment with all dependencies installed,

```bash
poetry install
```

That's it! You can validate that the environment is setup correctly by running the tests,

```bash
poetry run coverage run -m pytest
```

### Deployment

Update the version in `pyproject.toml`, run `poetry lock`, and add a new entry in `CHANGELOG.md`.

#### Automatic (preferred)

Merge the changes into master (using PRs). Create a new tag. If the new version is `1.1.1`, the new tag would be `v1.1.1`. 

The tag creation will trigger automated deployment of the package to PyPi, as well as synchronization of the code with the public GitHub mirror repository.

#### Manual (not recommended)

Build the project via Poetry,

```bash
poetry build
```

and push it to pypi,

```bash
poetry publish -u __token__ -p $INSPARI_PYPI_TOKEN
```