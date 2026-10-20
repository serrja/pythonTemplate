# Developing the Python foundation

`make install` prepares the existing Docker toolchain. `make ci-local` runs the
native lint, types and source tests once, reports coverage, builds a deterministic
template bundle and verifies its source and version metadata. Real Copier render
and update cases belong to the source suite; installed application acceptance is a
different scenario. Individual `make check`, `test`, `coverage`, `build`, `verify`,
`version` and `release-check` targets remain available.

Reports live under ignored `coverage/`; artifacts retain `dist/`. `ci-local.json`
contains source commit/dirty/content identity, commands, tool versions, statuses
and artifact checksums. Changing inputs invalidates prior evidence. Coverage below
100% warns; missing or corrupt reports, tests, types and build failures fail.

`OFFLINE=1 make ci-local` needs the previously prepared exact quality image. The
source bundle has no additional network inputs. Runtime consumers declare their
own cached acceptance/build inputs; missing inputs are blocked. No GitHub token,
Actions artifact or hosted cache is needed by the local command.

See [versioning](versioning.md), [release and recovery](releaseGuide.md), and the
[shared development policy](https://github.com/serrja/baseRules/blob/main/docs/development.md).
