# Naming policy

Use lower camelCase for new owned multiword repository, path, configuration, function, and variable names, such as `fastApiTemplate`, `createApp`, and `templateSource`. Classes, types, and exceptions use PascalCase. Constants and environment names use UPPER_SNAKE_CASE. Branches use `type/shortCamelCaseIntent`; commit and PR titles use `type(scope): clear intent`. Prose remains ordinary language.

Preserve required and published spellings: `README.md`, `AGENTS.md`, `SERVICE.md`, `CONTRIBUTING.md`, `pyproject.toml`, `uv.lock`, `Dockerfile`, `CMakeLists.txt`, `conftest.py`, `test_*.py`, tool discovery names, dunder methods, external keyword arguments, imports, JSON fields, migration IDs, scopes, CLI commands, and C++ public APIs. Python camelCase is a project choice, not a PEP 8 mandate; keep Ruff and strict mypy enabled.

Derive distribution, image, and DNS labels from a valid lowercase slug. Do not force camelCase where package normalization, OCI, or Kubernetes syntax rejects it. A rename updates all imports, entrypoints, CI, docs, and consumers through the owning source or generator, with a compatibility decision for published names.
