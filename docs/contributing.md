# Contributing workflow

This is the canonical process for the generic template. Generated projects receive a concise local `CONTRIBUTING.md` with their actual commands.

Read the [naming policy](naming.md), [versioning policy](versioning.md), and [release procedure](releaseGuide.md) for shared rules. The [composition ADR](adr/templateComposition.md) identifies the owner of derived source files.

## 🔀 Branch and review

Start a short branch from the repository's actual default branch: `feat/addHealthCheck`, `fix/preserveSettings`, `docs/releaseGuide`, or another `type/shortCamelCaseIntent`. Existing default branches are not renamed for style. Keep behavior, rename, dependency updates, and cleanup in separate reviews when their risk differs.

Use `type(scope): intent` for the PR title and focused commits. Describe why, scope, owners and boundaries, compatibility, checks with real results, privacy, version decision, and rollback. A small typo does not need an issue or ADR. A consequential boundary decision deserves a short ADR. Do not pre-check template boxes.

The author checks the full diff and outgoing commits. A reviewer checks correctness, ownership, failure handling, compatibility, and whether complexity is necessary. Mark blocking concerns clearly. A solo maintainer can use a PR and self-review with working checks; it cannot satisfy a rule demanding its own independent approval. Do not enable required checks before they exist on PRs. Merge, tag, package publish, and deploy each require their own authorization.

## 🧪 Checks

Run `make check`, then render each supported profile and run its canonical generated commands. Testing-enabled renders include meaningful package, CLI, or HTTP foundation tests and a complete Python coverage gate. The [testing guide](testing.md) owns the denominator and isolated-resource rules. `pytest` exit 5 is a failure. Never use `pytest || true`, fake passing tests, or blanket skips to hide collection errors. Keep unit checks isolated; run integrations only against disposable dependencies with bounded readiness and cleanup.

## 📝 Training example: PR

**Title:** `feat(service): add optional database wiring`

**Why:** A service that explicitly enables persistence needs a managed connection lifecycle.

**Scope:** Adds a `withPersistence` Copier answer, engine/session factory, and readiness check. No domain table or deployment target is added.

**Compatibility:** Existing default renders remain database-free. Enabling the answer requires `DATABASE_URL`; template revision changes separately from generated service versions.

**Checks to report:** Record the exact render, lock, lint, type, build, and startup results from the actual run. Do not claim CI or a database connection without a run.

**Risk and rollback:** Re-render from the prior template ref and review managed-file diffs; preserve `SERVICE.md` and service-owned code.

## 🐛 Training example: bug report

**Observed:** `/health/ready` returns 503 after an enabled database becomes unreachable.

**Expected:** It returns 200 only when the required dependency is reachable.

**Reproduction:** State the package version, OS, whether persistence is enabled, and a disposable database setup. Include redacted logs and the exact command/result. Never attach `DATABASE_URL`, `.env`, VPN links, credentials, or a working database.
