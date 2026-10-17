# pythonTemplate

`pythonTemplate` is a generic Copier source for Python CLI and library projects. The existing private repository was renamed from `serrja/projectTemplates` to `serrja/pythonTemplate` without changing its Git history. Its canonical Copier source is `git@github.com:serrja/pythonTemplate.git`. The old `service` and `native` profiles remain renderable for compatibility; new FastAPI projects use the separate `fastApiTemplate` derivative. No Pokerlost SDK, credentials, or hooks are included.

## 🚀 Generate

Requires Python 3.12+, `uv`, and Copier 9.17.2. The stable project answer and CLI can remain camelCase; new import packages are lowercase. Existing answers and published imports require a reviewed migration before renaming.

```bash
destination="$(mktemp -d)"
uvx --from 'copier==9.17.2' copier copy . "$destination" -d projectName=notesCli -d profile=cli
cd "$destination"
uv lock
uv sync --locked
uv run notesCli --help
```

The recommended profiles here are `cli` and `library`. The `service` and `native` choices reproduce older projects; do not silently migrate an existing application by re-rendering it as a new profile. The [migration note](docs/serviceDesign.md) describes the handoff. New names follow the [naming policy](docs/naming.md).

The legacy `service` profile starts without a database. Add `-d withPersistence=true` only for an existing legacy workflow; new web foundations use `fastApiTemplate`. `withTesting=false` and `withCi=false` omit those capabilities from a specialized render.

## 🧭 Ownership

The shared template owns packaging, quality configuration, CI, and the initial documentation structure. The generated project's `PROJECT.md` or `SERVICE.md`, implementation, tests, and lockfile belong to that project. Copier skips its owner document during updates. Review the patch before applying an update; no generated file is an ongoing dependency on this checkout.

## 🛠 Development

From a clean generated Git checkout, use `uvx --from 'copier==9.17.2' copier update --defaults --vcs-ref=<reviewed-template-ref>` and inspect Git conflicts and deletions before accepting the result. Copier writes its own source/ref in `.copier-answers.yml`; do not edit that file to simulate an update. Historical and controlled future updates were verified with real local Git refs in disposable repositories. The source stamp declares unreleased worktree version `0.1.0.dev0` and answers schema 1; use reviewed Git tags for releases after authorization.

The [documentation guide](docs/documentation.md), [contribution guide](docs/contributing.md), [naming policy](docs/naming.md), [versioning policy](docs/versioning.md), and [release procedure](docs/releaseGuide.md) each own one topic. The [composition ADR](docs/adr/templateComposition.md) defines pinned derivative sources; the [verification guide](docs/verification.md) records actual checks and limits.
