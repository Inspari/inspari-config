This repository provides Python configuration utilities.

### Usage

The most common usage patternis to create a `config.py` file that defines the application configuration. The configuration itself is parsed from environment variables. They are typically read from a `.env` file during local development, injected at runtime in pipelines, and passed via application settings in production.

A minimal example is bundled, with the configuration defined in `example_config.py`, a few variables in `example.env`, and the typical access pattern (i.e. how settings are access in application code) illustrated in `example_usage.py`.

### Development

Create a new Python environment with all dependencies installed,

```bash
poetry install
```

That's it! You can validate that the environment is setup correctly by running the tests,

```bash
poetry run coverage run -m pytest
```
