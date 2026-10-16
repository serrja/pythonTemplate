# projectTemplates

Generic Copier scaffolds for a Python CLI, library, independent web service, or native extension. The template has one shared base and small profile-specific files; it contains no Pokerlost SDK, domain entities, credentials, or post-generation hooks.

## 🚀 Generate

Requires Python 3.12+, `uv`, and Copier 9.17.2. Choose a short camelCase project name; its import package and CLI keep that spelling, while the distribution name is lowercase for package metadata.

```bash
uvx --from 'copier==9.17.2' copier copy . /tmp/notesCli -d projectName=notesCli -d profile=cli
cd /tmp/notesCli
uv lock
uv sync --locked
uv run notesCli --help
```

Profiles are `cli`, `library`, `service`, and `native`. New names follow camelCase; existing API names are never renamed by this template.

The `service` profile starts without a database. Add `-d withPersistence=true` to render optional PostgreSQL connection, readiness, and Alembic wiring. See the [service design](docs/serviceDesign.md); no domain schema or credentials are generated.

## 🧭 Ownership

The shared template owns packaging, quality configuration, CI, and the initial documentation structure. The generated project's `PROJECT.md` or `SERVICE.md`, implementation, tests, and lockfile belong to that project. Copier skips its owner document during updates. Review the patch before applying an update; no generated file is an ongoing dependency on this checkout.

## 🛠 Development

Run `uvx --from 'copier==9.17.2' copier update --help` in a generated Git project to see the update interface. Record a template Git tag or commit in `.copier-answers.yml` when generating from a committed source. The initial local version is `0.1.0`; use Git tags for releases after publication.

The [documentation guide](docs/documentation.md) gives writing rules. [Contributing](docs/contributing.md) and the [release policy](docs/releaseGuide.md) own the shared process; the [verification guide](docs/verification.md) records profile checks and known limits.
