# Release and recovery procedure

Read the [versioning policy](versioning.md) before deciding a release number. This procedure does not grant tag, package publication, merge, or deployment authority.

1. Identify the changed contract and consumers. Decide compatibility and write a focused release note, including migrations or answer changes.
2. Change the single canonical version source only when a release is warranted. Preserve existing SCM-derived schemes.
3. Run the actual locked checks and build wheel/sdist, container, and Copier render/update where relevant. Inspect artifact contents and record failures or unavailable infrastructure.
4. Review the complete diff, sensitive files, outgoing commits, and downstream update order in a PR. Obtain the review available to the project.
5. With separate publication authorization, create an immutable tag and publish the same reviewed artifact once. Read back remote SHA, artifact digest, and actual CI result.

For an application rollback, select the previously approved artifact digest and separately assess database compatibility. A template update recovers from the prior pinned source and backup of the generated project; it never auto-downgrades a live migration. Do not treat a Git push as package or production deployment permission.
