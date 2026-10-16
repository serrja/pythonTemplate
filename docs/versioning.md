# Versioning policy

This page owns compatibility and version rules for the two generic Copier sources and new Python applications. Existing published projects retain their own version source and compatibility contract.

## 📦 Independent identities

`pythonTemplate` is the logical name of this repository while its current remote remains `serrja/projectTemplates`. `fastApiTemplate`, Pokerlost `serviceTemplate`, and each generated application have independent revisions. Copier answers, managed paths, minimum Copier/Python versions, and enabled capabilities are part of template compatibility. Record each parent by immutable content SHA-256 or published Git commit, plus the derivative version and answer schema. A parent update is reviewed and propagated; it is not an automatic downstream release.

The SDK runtime package, SDK generator, and schema/manifest have separate versions. OpenAPI/wire compatibility is assessed separately from package version. Alembic revision IDs identify schema transitions, not application releases. Docker deployments select an immutable digest; Helm chart `version` and `appVersion` are distinct when a project actually uses Helm.

Current minimum Python versions differ by owner: this Python base and the generic FastAPI base support 3.12+, while `pokerengine` supports 3.12+ and the pinned `pypokerlost` SDK and Pokerlost `serviceTemplate` require 3.14+. A specialized service therefore does not inherit a 3.12 runtime guarantee from its generic parent. Check the actual package metadata before changing any minimum.

## 🔒 Changes

For stable public APIs, breaking changes increment major, compatible features minor, and compatible fixes patch. For a `0.y.z` project, a breaking change increments minor and carries a migration note; compatible small changes may increment patch. This is a project policy, not a universal stability promise for all `0.x` releases.

Python distributions use PEP 440: package `1.2.3` and tag `v1.2.3`; prerelease `1.3.0rc1`. Compare parsed versions rather than strings. A new generated application uses `[project].version` in `pyproject.toml` as its sole version source. Existing SCM-derived mechanisms remain where already established. Installed code reads package metadata, not a neighboring checkout. Published tags and artifacts are never rewritten for cosmetic alignment.

An application version does not automatically change after a template update. Record the template source identity in Copier answers and derivative provenance; review answer migration, managed-file deletions, optional features, and user-owned conflicts before deciding whether a downstream release is needed.

The [release procedure](releaseGuide.md) covers checks, publication authorization, and recovery. The [contribution guide](contributing.md) describes the review workflow.
