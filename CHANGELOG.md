# Changelog

Notable source and tooling changes are recorded below.

## 0.3.0.dev2

Generated offline CI validates prepared artifacts and installed-image identity, then reruns tests without dependency or image builds. Missing or changed inputs remain blocked. Application versions and runtime contracts are unchanged.


## 0.3.0.dev1

Compatible tooling prerelease: add source-bound local CI receipts, native version
and release checks, and deterministic template bundles. Root packaging metadata
now owns the template version; Copier renders full source SHA/ref provenance.
Application versions, imports, supported profiles and answer schema 1 are retained.
Updates preserve owner code, settings, tests, migrations and local Make commands.
