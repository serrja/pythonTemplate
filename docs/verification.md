# Verification

Render each profile into a disposable directory with Copier 9.17.2. The generated project must parse as TOML, contain no `{{` placeholders, have no Pokerlost dependency, and build with its available toolchain. Run `uv lock`, `uv sync --locked`, `uv run ruff check .`, `uv run mypy`, and `uv build` after rendering. The service's ASGI object is checked by import; native needs a compiler and CMake. These are infrastructure checks, not subject tests.

No generated project contains a `test_*` body. `uv run pytest` keeps exit code 5 until a project adds tests. CI reports `NOT_CONFIGURED` for that stage and still checks package build. A test job added later must fail on zero collection.

Copier updates require a committed template revision. Preserve the generated owner's `PROJECT.md` or `SERVICE.md`, inspect the update diff, and reject any conflict that would overwrite project behavior.
