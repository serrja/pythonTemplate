# Verification

Render each profile and both service persistence choices into a disposable directory with Copier 9.17.2. The generated project must parse as TOML, contain no unrendered placeholders or Pokerlost dependency, and build with its available toolchain. Run `uv lock`, `uv sync --locked`, `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked mypy`, and `uv build` after rendering. For the database-free service, enter the ASGI lifespan with no credentials and check both health routes. For the database-enabled render, verify `DATABASE_URL` is required and no connection occurs on import; a live readiness check requires a disposable database. Native needs a compiler and CMake. These are infrastructure checks, not subject tests.

No generated project contains a `test_*` body. `uv run pytest` keeps exit code 5 until a project adds tests. CI reports `NOT_CONFIGURED` for that stage and still checks package build. A test job added later must fail on zero collection.

Copier updates require a committed template revision. Preserve the generated owner's `PROJECT.md` or `SERVICE.md`, inspect the update diff, and reject any conflict that would overwrite project behavior.
