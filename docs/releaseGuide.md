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

Automated publication remains blocked until a reviewed shared provider supports
the native Python build adapter and metadata acceptance. Keep the provider as the
single allocator/publisher; do not create a parallel release system or rename a
prerelease distribution as stable. Registry publication and production deployment
require separate configuration and authorization.

## 🔄 Recovery

Recover a partial release through the shared provider's original event identity
and recovery contract. Do not substitute the current branch head, move an existing
tag or invent a missing source event. Confirm the final tag target, release state,
channel, native metadata and asset checksums after publication.

For an application rollback, select the previously approved artifact digest and
assess database compatibility separately. A template update recovers from the
prior pinned source and a backup of the generated project; it never automatically
downgrades a live migration.
