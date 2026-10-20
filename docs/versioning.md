# Template and application versions

The shared [compatibility policy](https://github.com/serrja/baseRules/blob/main/docs/versioning.md)
owns major/minor/patch, prereleases and the 0.x policy. This page records the Python
chain's concrete metadata and update boundaries.

Root `[project].version` in `pyproject.toml` is the sole source of this template's
PEP 440 version. The compositor derives `.template-source.json` from it; neither
`composition.toml` nor a Python constant repeats the number. `make version` reads
the metadata and `make release-check` validates the built source bundle.

A generated application's `[project].version` is independent. Changing a template
version does not bump the application. Copier writes `.copier-answers.yml` itself;
`.template-version.json` additionally records the supported full VCS source hash,
selected ref and derived template version. An unversioned local source records a
null hash, not a fabricated publication. Never edit answers to simulate an update.

Python/Typer/FastAPI sources require Python 3.12 or newer. The Pokerlost service
foundation and its pinned SDK require Python 3.14 or newer. Check the actual owner
metadata before changing runtime compatibility. Imports, CLI, HTTP, configuration,
answers, custom files and minimum runtime versions all belong in the compatibility
decision; Alembic revisions remain independent database transitions.

An update follows the pinned parent into its explicit overlay and then runs native
Copier against a committed project. Review conflicts and preserve project code,
settings, tests, migrations, application version and local Make commands. The
source composition contract remains in [the ADR](adr/templateComposition.md).
