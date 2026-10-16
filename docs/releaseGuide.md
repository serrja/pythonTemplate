# Version and release policy

This page owns versioning for new generated projects. Existing projects keep their working version source and published compatibility contracts.

## 🧭 Version sources

The generated Python package has one source in `[project].version`. A service reads its installed distribution version through package metadata when needed; runtime code does not parse checkout `pyproject.toml`. A tag such as `v1.2.3` identifies the matching checked artifact. Python prereleases use PEP 440 syntax, for example package `1.3.0rc1` and tag `v1.3.0rc1`.

Stable public API breaking changes increment major, compatible capabilities minor, and compatible fixes patch. For `0.y.z`, this project's stricter policy uses minor for a breaking change with migration notes and patch for compatible changes. This is a local contract, not a universal guarantee for 0.x. A documentation edit without release need does not force a bump.

The Copier template has its own revision. A generated service's version does not change merely because the template changes. OpenAPI compatibility is assessed separately from app version, Alembic revisions from release version, and immutable image tag/digest from deployment state. Do not use `latest` as a deployment identity or rewrite a published tag.

## 🚀 Release decision

Review public contract impact and deprecation, write the Unreleased note, update the single version source, run actual checks, inspect artifacts, obtain review, then create an immutable tag and publish only with explicit release authorization. Roll back to a prior artifact/digest if needed; database rollback requires a separate compatibility decision. No release, registry, credentials, or deployment target is configured by this scaffold.

### Training release note

```text
1.3.0rc1 — example only
Added: opt-in database readiness.
Compatibility: default database-free startup remains available.
Migration: enabled services must supply DATABASE_URL and a reviewed schema migration.
Checks: record real commands and results before publication.
```
