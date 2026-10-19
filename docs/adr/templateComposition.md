# ADR: pinned source composition

This decision defines source ownership and reproducible template composition.

## Context

Copier does not implicitly inherit a remote template. Layering independent templates over one answers file obscures provenance and creates conflicts for `pyproject.toml`, README, and CI.

## Decision

A derivative carries a content-addressed snapshot of its parent Copier source, a small overlay, `composition.toml`, and `composition.lock.json`. The parent-owned `tools/compose_template.py` copies only declared source paths, rejects undeclared collisions or modified managed source, records a SHA-256 identity covering the parent, overlay, composition contract, and the derivative's own `copier.yml`, and assigns one owner per output file. It invokes actual Copier for a smoke render. Jinja inheritance handles deliberate whole-file specializations such as `pyproject.toml`; Copier remains the only renderer. The final generated application has no template checkout dependency.

A new parent revision is deliberately refreshed into the derivative snapshot, reviewed, assembled, rendered, and then propagated downstream. A dirty parent is identified by content hash and marked dirty; its old clean HEAD is never represented as the changed source. Release/tag decisions remain separate. The two generic repositories and Pokerlost specialization remain separate Git histories.

The composition command itself is owned by this Python base. Typer and FastAPI are sibling specializations; Pokerlost serviceTemplate derives only from FastAPI. Typer owns CLI source and CliRunner tests, while the base owns common engineering policy. A derivative's root `tools/compose_template.py`, when present, is a checked mirror of the pinned parent tool. Refresh updates that mirror only if it still matches the previous snapshot; clean rebuilds reject a divergent mirror. The specialized service invokes the tool from its pinned FastAPI snapshot.

## Consequences

Snapshots increase repository size but make clean checkouts reproducible without a private parent at render time. The `include` and `allowOverride` lists are reviewed ownership contracts. Copier updates require actual prior and new committed source refs. Disposable repositories with real local commits verified historical Python and service updates and controlled FastAPI evolution; no working-repository release ref was created by that check.
