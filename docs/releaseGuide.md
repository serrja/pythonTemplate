# Release and recovery procedure

Read the [shared release policy](https://github.com/serrja/baseRules/blob/main/docs/releases.md) and [versioning policy](versioning.md) before deciding a release number. This procedure does not grant tag, package publication, merge, or deployment authority.

1. Identify the changed contract and consumers. Decide compatibility and write a focused release note, including migrations or answer changes.
2. Change the single canonical version source only when a release is warranted. Preserve existing SCM-derived schemes.
3. Run the actual locked checks and build wheel/sdist, container, and Copier render/update where relevant. Inspect artifact contents and record failures or unavailable infrastructure.
4. Review the complete diff, sensitive files, outgoing commits, and downstream update order in a PR. Obtain the review available to the project.
5. After required checks and review, integrate the exact commit into main. Inspect tag-triggered workflows, then create one annotated `v<PEP440-version>` tag on that checked clean commit when authorized. Push that tag alone and read back its peeled SHA. Package publication and deployment are separate operations; billing-blocked checks prevent merge and tagging.

Generated projects with CI include a manual `Release candidate` workflow. After a separately authorized tag exists on the default branch, provide its full `reviewed_sha`, `v`-prefixed `tag`, and reviewed `release_notes`. The workflow checks the tag and commit against the default branch, compares the package version with a PEP 440 parser, calls `make ci-local` for locked checks and artifacts, and `make image` where enabled, then uploads notes and SHA-256 artifact identities. Publication and deployment are explicitly `notConfigured` until a registry, destination, narrow authentication, and environment gate are selected and reviewed. Do not treat its artifact upload as a package release.

For an application rollback, select the previously approved artifact digest and separately assess database compatibility. A template update recovers from the prior pinned source and backup of the generated project; it never auto-downgrades a live migration. Do not treat a Git push as package or production deployment permission.
