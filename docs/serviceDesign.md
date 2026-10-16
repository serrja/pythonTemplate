# Generic service foundation

The `service` profile renders an independent FastAPI project. It has no Pokerlost package, credential, operation, or private checkout dependency.

## 🧭 Ownership

The template owns the initial package, typed environment boundary, ASGI lifespan, liveness and readiness, quality settings, Dockerfile, and CI scaffold. The generated project owns `SERVICE.md`, API behavior, data model, migrations, deployment target, and its lockfile. Copier skips `SERVICE.md` on update. Review every managed-file diff before accepting an update.

`/health/live` reports only an HTTP process response. `/health/ready` checks the enabled database when `withPersistence=true`; otherwise it reports that the empty service has no required external resource. Neither endpoint claims product behavior.

## 🗄️ Optional persistence

`withPersistence=false` is the default. It requires no database credentials and omits SQLAlchemy, asyncpg, Alembic, and their files. `withPersistence=true` adds an async PostgreSQL engine, per-operation session factory, and an Alembic environment. `DATABASE_URL` is then required at lifespan/migration time. No connection is opened during module import, schema is not created at startup, and no domain table or migration revision is generated. Add actual model metadata and review a forward migration before using Alembic against a disposable database.

The pristine service has no Redis, RabbitMQ, telemetry, authentication, or protected route. Add an integration only with a real owner, settings, readiness contract, and failure behavior. A missing authentication implementation does not create an allow-all route.

## 🔒 Compatibility

The service package version begins at `0.1.0`; the template's revision is separate. A template update does not automatically change a generated service version. The generated project records Copier source/ref/answers in `.copier-answers.yml`. Its wheel and image must be built from that project's own locked dependencies.
