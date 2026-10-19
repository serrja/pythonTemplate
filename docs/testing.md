# Testing and coverage

The maintenance suite verifies composition, provenance, failure cleanup, real Copier renders, and updates. Generated foundation tests belong under `tests/foundation/`; application tests remain project-owned.

## Run maintenance checks

```bash
make help
make check
make coverage
```

`uv.lock` owns the maintenance dependency versions. `make test` runs the whole suite with statement and branch measurement, advisory coverage, missing counts, and JSON/XML output under `coverage/`. The denominator includes all canonical executable tooling under `tools/`, including modules that were never imported. Tests, Jinja, vendored snapshots, and generated output are not Python tooling coverage.

The suite uses temporary directories and real local Git refs for Copier update tests. It verifies source identity, owned-file preservation, overlap conflicts, rejected snapshot edits, and failed subprocess propagation. It never changes a source repository's refs or working data. `tools/test_composition.py` is the canonical shared composition suite; explicit parent refresh propagates it alongside the composition tool, with the same provenance and local-edit protection. Derivatives run that managed suite against their own pinned tool rather than maintaining independent copies.

## Verify a generated project

```bash
uv lock
make install
make check
make build
```

Fresh renders resolve their first lock; an existing application must use its committed lock without silently updating dependencies. Every testing-enabled profile includes package-boundary tests. The separate typerTemplate specialization exercises real command/module entry points; native renders import their installed adapter. A library or empty adapter has no generated domain behavior: import checks do not prove application correctness or native algorithm coverage.

Generated coverage includes every module in the application's package, also when never imported. The path mapping supports both a source environment and an installed wheel. Report their executions separately and identify the tested source/artifact; do not let a checkout shadow the wheel.

Pytest uses `importlib` mode so a project-owned test and a foundation test may share a basename without colliding. Use fixture discovery or explicit package imports; do not rely on pytest adding test directories to `sys.path`.

## HTTP and external resources

Ordinary HTTP tests use `with TestClient(application) as client`, so startup and shutdown belong to the same test. Assert resource state before, during, and after the context. Disable exception propagation only for the individual handled-500 test. The retained legacy service profile has technical tests; new HTTP projects use the FastAPI derivative's maintained foundation.

Use an async HTTPX client and explicit lifespan only when the assertion must await a resource in that same event loop. Simulated dependency faults are unit checks, not PostgreSQL acceptance. Database integration uses an explicitly supplied disposable database with bounded readiness and cleanup; never a workstation or production DSN.

## Interpret failures

Coverage below 100% produces a warning and exit 0 when tests and required checks pass. `fail_under = 0` removes only the numerical gate. Missing, corrupt or stale required reports remain errors. No tests collected, a missing mandatory dependency, cancellation, or a skipped required job is not success. Report statement/branch totals and missing counts. For a denominator with no branches, report branch coverage as notApplicable; absent instrumentation is notMeasured. Native C++ and client languages require their own tools; Python coverage does not measure them.

## Docker command contract

Git, Make and Docker suffice for the standard path. `make help` is read-only and offline.
`make install` prepares the locked quality image. `lint` and `typecheck` run native tools in it;
`test` executes the suite once, then validates JSON counters and emits advisory warnings.
`check` runs lint, types and that same suite. `coverage` reads the existing result, checks the
recorded quality image identity and run-start marker, and never reruns tests. Source, test,
lock or recipe changes invalidate the evidence. A missing/stale result says to run `make test`.
`build` exports applicable distributions through the cached builder; `image` creates a local
runtime candidate and `verify` runs the project's installed/runtime acceptance. Maintenance
repositories verify real disposable renders instead of pretending to publish an application.

`docker/quality.mk` and `docker/coverage_report.py` are managed portable snapshots from
`pythonTemplate/template/docker/`. The consuming repository declares its native commands and
Docker stages, with no runtime dependency on a private sibling checkout. Language-specific
Dart/Node reporters use their own toolchains and preserve the same exit-code policy.

Dependency metadata and locks precede source COPY instructions. CI restores BuildKit cache by
repository, image/target, platform and trusted/review role, then runs fresh test processes.
A cached RUN is never test evidence. Artifacts cross jobs explicitly; `needs` alone transfers
no image. Unchanged runtime inputs may reuse their verified digest; documentation or test
changes never relabel an old artifact as a new source build. A cached solve is used where a
safe skip has not been proven. Keep private SDK intermediate caches private and use BuildKit
secret mounts, never build ARG/ENV credentials.

Reports under `coverage/` include safe JSON/XML/HTML and a numeric `summary.md`; CI appends the
summary to `GITHUB_STEP_SUMMARY`. Workflow warning data is escaped. Runtime zero-test collection,
assertion failures, build/types/config/security/access errors and malformed evidence fail.
The isolated `tests/test_coverage_policy.py` suite verifies these distinctions with real pytest
subprocesses and build failures. Coverage gaps alone do not keep an otherwise ready PR Draft.
