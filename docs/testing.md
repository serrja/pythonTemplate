# Testing and coverage

The maintenance suite verifies composition, provenance, failure cleanup, real Copier renders, and updates. Generated foundation tests belong under `tests/foundation/`; application tests remain project-owned.

## Run maintenance checks

```bash
make install
make check
make test-unit
make test-integration
```

`uv.lock` owns the maintenance dependency versions. `make test` runs the whole suite with statement and branch measurement, a strict 100% gate, missing counts, and JSON/XML output under `coverage/`. The denominator includes all canonical executable tooling under `tools/`, including modules that were never imported. Tests, Jinja, vendored snapshots, and generated output are not Python tooling coverage.

The suite uses temporary directories and real local Git refs for Copier update tests. It verifies source identity, owned-file preservation, overlap conflicts, rejected snapshot edits, and failed subprocess propagation. It never changes a source repository's refs or working data. `tools/test_composition.py` is the canonical shared composition suite; explicit parent refresh propagates it alongside the composition tool, with the same provenance and local-edit protection. Derivatives run that managed suite against their own pinned tool rather than maintaining independent copies.

## Verify a generated project

```bash
uv lock
make install
make check
make build
```

Fresh renders resolve their first lock; an existing application must use its committed lock without silently updating dependencies. Every testing-enabled profile includes package-boundary tests. CLI renders also exercise command/module entry points; native renders import their installed adapter. A library or empty adapter has no generated domain behavior: import checks do not prove application correctness or native algorithm coverage.

Generated coverage includes every module in the application's package, also when never imported. The path mapping supports both a source environment and an installed wheel. Report their executions separately and identify the tested source/artifact; do not let a checkout shadow the wheel.

Pytest uses `importlib` mode so a project-owned test and a foundation test may share a basename without colliding. Use fixture discovery or explicit package imports; do not rely on pytest adding test directories to `sys.path`.

## HTTP and external resources

Ordinary HTTP tests use `with TestClient(application) as client`, so startup and shutdown belong to the same test. Assert resource state before, during, and after the context. Disable exception propagation only for the individual handled-500 test. The retained legacy service profile has technical tests; new HTTP projects use the FastAPI derivative's maintained foundation.

Use an async HTTPX client and explicit lifespan only when the assertion must await a resource in that same event loop. Simulated dependency faults are unit checks, not PostgreSQL acceptance. Database integration uses an explicitly supplied disposable database with bounded readiness and cleanup; never a workstation or production DSN.

## Interpret failures

`fail_under = 100` rejects every result below 100, regardless of display rounding. No tests collected, a missing mandatory dependency, cancellation, or a skipped required job is not success. Report statement/branch totals and missing counts. For a denominator with no branches, report branch coverage as N/A. Native C++ and client languages require their own tools; Python coverage does not measure them.
