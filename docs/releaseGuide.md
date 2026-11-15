# Release and recovery procedure

Follow the [shared release policy](https://github.com/serrja/baseRules/blob/8434509933feaa71ba312f8d02caad7362766d5a/docs/releases.md)
and [versioning policy](versioning.md). Every new `dev` or `main` push, including
documentation changes, requires checks and a GitHub Release at its exact event
SHA. Tags are `vX.Y.Z-dev.N` on dev and `vX.Y.Z` on main; Python metadata maps to
`X.Y.Z.devN` and `X.Y.Z`. Preserve every existing tag and its target.

## 📦 Checks and publication

Run locked checks, applicable Copier render/update scenarios and native builds.
Review the full diff, compatibility, artifact contents and current hosted checks.
Promote working branch → `test` → `dev` → `main`, preserving ancestry and permanent
branches. An unavailable mandatory check blocks merge and publication.

The source and generated CI workflows check each permanent-branch push without
canceling an earlier push. They do not publish GitHub Releases. The generated
manual `Release candidate` workflow verifies an existing reviewed tag and uploads
candidate artifacts; this does not satisfy exact-event publication policy.

The published [H02 Python contract](https://github.com/pokerlost/.github/blob/e5cac33af228224af9deaef308e39c1b9f788033/docs/python_release_contract.md)
defines the shared allocator, verifier and publisher for native wheel/sdist
packages. The canonical `template/docker/python_release.py` implements only the
unprivileged native builder and receipt step described below. This source bundle
has `tool.uv.package = false` and no build backend; it cannot use the wheel/sdist
contract. Source-bundle publication needs a compatible shared-provider capability,
without adding a second version source or a fictitious package backend.

Keep the provider as the single allocator/publisher. Do not rename a prerelease
distribution as stable. Registry publication and production deployment require
separate configuration and authorization. Local adapter checks do not constitute
hosted acceptance or a published release.

## Native Python adapter

Run the portable `docker/python_release.py` from a clean, exact source Git root
using the project's locked interpreter, with its declared build backend already
installed. `--source-pyproject` is the unmodified source file (or an identical
provider-fetched copy). Allocation JSON must retain the provider's exact compact
bytes and SHA-256. The provider pin must match the reviewed reusable workflow.

```bash
python docker/python_release.py build \
  --allocation "$ALLOCATION_FILE" --allocation-sha256 "$ALLOCATION_SHA256" \
  --provider-ref "$PROVIDER_REF" --destination "$STAGING" --output "$DIST" \
  --evidence "$BUILD_EVIDENCE" --source-pyproject pyproject.toml
```

Staging, output and evidence must be new, nonoverlapping paths outside the source
checkout, with existing parent directories. The helper validates the full
schema-2 allocation, available GitHub identity, clean source SHA, package name,
static version target and declared installed backend. It rejects dynamic versions,
in-tree backends, archive links, special files and case-colliding paths. Export
limits are 20,000 members, 256 MiB per member and 1 GiB total. It exports exact HEAD,
uses `uv version ALLOCATED --frozen --offline --directory STAGING`, and builds
offline with `uv build --no-build-isolation --python <current interpreter>`.
`--no-create-gitignore` keeps output limited to native artifacts. Original source
and lock bytes remain unchanged. Credential and GitHub/OIDC variables are removed
from backend subprocess environments; this is an unprivileged native build, not
a sandbox for untrusted source.

The stable source version target is an allocation floor; a provider-selected
later patch version is supported. Exact wheel tags come from the allocation.
Compiled profiles require their reviewed real Python/ABI/platform tags; do not
substitute `py3-none-any`. No build requirement is downloaded or resolved.

Run the pinned provider's `scripts/python_artifacts.py verify` against the original
source pyproject and completed dist directory. Save its ordered JSON result as
`$NATIVE_METADATA`, then issue the receipt before attestation/upload:

```bash
python docker/python_release.py receipt \
  --allocation "$ALLOCATION_FILE" --allocation-sha256 "$ALLOCATION_SHA256" \
  --metadata "$NATIVE_METADATA" --build-evidence "$BUILD_EVIDENCE" \
  --job-id "$BUILDER_JOB_ID" --run-attempt "$GITHUB_RUN_ATTEMPT" \
  --output "$DIST/python-build-receipt.json"
```

The receipt binds the allocation, original source, actual build tools, current
artifact hashes and original run/attempt/job identity. It preserves the provider's
ordered metadata. Existing/stale outputs fail rather than being overwritten.
The provider remains responsible for independent metadata verification,
attestations, allocation, publication and recovery. The helper never discovers
job IDs, grants credentials, creates tags or publishes assets.

## 🔄 Recovery

Recover a partial release through the shared provider's original event identity
and recovery contract. Do not substitute the current branch head, move an existing
tag or invent a missing source event. Confirm the final tag target, release state,
channel, native metadata and asset checksums after publication.

For an application rollback, select the previously approved artifact digest and
assess database compatibility separately. A template update recovers from the
prior pinned source and a backup of the generated project; it never automatically
downgrades a live migration.
