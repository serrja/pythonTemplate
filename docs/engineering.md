# Engineering and tooling policy

General engineering norms come from [baseRules at the selected commit](https://github.com/serrja/baseRules/blob/730418d3cc480b4f05b88b4c8275296c4845a75a/docs/engineering.md). This Python base owns the Python tooling mechanisms below. Specializations own their
boundary mechanisms; generated applications depend on installed packages, not
template checkouts. Before writing glue, inspect existing tool features, then
the official API, then a maintained library. Add only the missing concrete step.

## 🧭 Owners and verification

| Task | Tool and native mechanism | Configuration owner and scope | Version / lock | Verification |
| --- | --- | --- | --- | --- |
| Packaging and environments | uv, PEP 517 and pyproject | pythonTemplate; Python projects | uv 0.12.15, project uv.lock | locked sync, wheel/sdist, installed process outside checkout |
| CLI parsing | Typer app, explicit command names, Annotated Argument/Option and completion | typerTemplate; real Python CLIs | Typer 0.27.3, project lock | pytest and typer.testing.CliRunner; real executable and python -m |
| Structured data | Pydantic v2 BaseModel, Field, aliases, TypeAdapter and model validation/dump | nearest format owner; actual API/config/manifest/receipt boundaries | compatible 2.x in project lock | valid/invalid input, serialization, JSON Schema, no secret leakage |
| Settings | Pydantic Settings BaseSettings and SettingsConfigDict | application / specialized template | compatible locked 2.x | explicit CLI > env > selected file > defaults for new CLI; preserve existing priority |
| HTTP | FastAPI routers, Depends/Security, exception handlers and lifespan | fastApiTemplate; generic HTTP | project lock | with TestClient(app), actual OpenAPI and isolated async integration |
| Pokerlost operations | FastAPI operation_id and external paths | serviceTemplate only | SDK and template immutable refs | path/verb/tag/operation identity and SDK compatibility |
| DB migrations | Alembic ScriptDirectory and MigrationContext APIs; SQLAlchemy | fastApiTemplate capability, application schema owner | project lock; unchanged historical revisions | disposable DB upgrade, expected/current head sets, readiness |
| Source generation/update | Copier plus Jinja; content-addressed composition | pythonTemplate composition tool, specialized overlays | Copier 9.17.2, composition lock, exact Git source refs | fresh render, real update, owner-file retention and conflicts |
| Python quality | Ruff, mypy, pytest, coverage.py | Python base; domain tests stay application-owned | Ruff 0.16.4 and uv.lock | types/lint/tests fail; coverage below 100% warns; corrupt reports fail |
| Workflow validation | actionlint and ShellCheck | shared action / workflow owner | pinned checksums and action commits | native actionlint, no custom YAML analyzer |
| Docker cache/build | BuildKit / Buildx cache mounts and GHA scopes | shared Docker recipes; application Dockerfile | pinned toolchain/image digests | same graph, fresh tests, verified artifacts and immutable image identity |
| Local composition / Kubernetes | Docker Compose and Helm | platformInfra / chart owner | locks and immutable images | rendered config, lint, disposable local Kind; no custom orchestrator |
| Client / web | Dart/Flutter, Vue/TypeScript and browser tools | pokerClient / pokerWeb | ecosystem locks and pinned SDK images | web-only tests/builds; no Python client runtime |
| Version comparison | packaging.version or the owning tool's parser | owning Python tool | project lock | ordering and prerelease regressions |

## 🔒 Boundaries and exceptions

Typer is the only Python CLI parser. Do not enable Pydantic Settings cli_parse_args
or CliApp. Assemble structured models explicitly after native argument parsing.
Keep application settings, operation input and result models separate. Missing
options do not overwrite env/config; false and zero are explicit values. Decide
null, aliases, strictness, unknown fields and serialization at each boundary.

Validators are pure: no file/network/DB/subprocess/business effects. Authorization,
freshness, filesystem containment and transactional constraints remain separate.
Load settings/resources at the composition point, never during import. Help and
version do not require secrets, downloads or a live DB. Do not print raw validation
input, errors(), repr, DSNs or traceback locals at user-facing boundaries.

Stdlib types, dataclasses, TypedDict and Enum remain appropriate for simple
internal values. A library with no validation boundary does not acquire Pydantic.
Do not replace SQLAlchemy, add a runtime template package, or introduce a framework
for DI, command registration, repositories or events without a concrete need.

The dependency-free setupSystem bootstrap is a small installer/delegator; it does
not import Typer/Pydantic before dependencies exist. Its read-only plan/help path
must not download. Historical Python-base CLI refs remain renderable; new CLI
source belongs only to typerTemplate. Legacy service/native profiles remain pinned
compatibility paths, with new HTTP development in fastApiTemplate. Existing
project-specific settings and tests survive updates. Python names follow PEP 8;
Pokerlost external camelCase conventions do not change generic Python/HTTP names.

## 🧩 Typed contracts and values

The nearest boundary owner defines meaningful states, events, operation names and
settings. Prefer an enum or discriminated union for a closed vocabulary, a typed
configuration for deployment choices, and a schema for untrusted messages. Keep
wire encodings explicit and stable. Test unknown variants, serialization and
exhaustive handling; a type assertion is not runtime validation. Small local
literals and independent protocol fixtures do not need a global constants file.
Timeouts and retry limits carry units and remain with the policy that uses them.
Frontend-specific syntax and lifecycle rules belong to pokerWeb/pokerClient.

Imports that cross a parent directory use an absolute package name or the project's
native alias. Local imports within a directory remain valid. Python enforces the
boundary with Ruff TID252 (`parents`); do not change external or historical vendored
sources to satisfy an owned-source rule. Validate executable and installed imports
outside the checkout, not only the editor's path resolution.
