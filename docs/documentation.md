# Documentation guide

This guide is the canonical style source for generated documents. Keep one H1, a purpose sentence, useful H2 sections, language-tagged fences, and working commands. Use a small emoji only in navigation headings. Link to one owner for each topic; do not repeat a contract in every file.

## 🚀 README and getting started

Write what exists, who uses it, exact prerequisites, a fresh-checkout command sequence, and links to architecture and development. Omit unimplemented features and guessed performance. Verify commands in a clean render. Example: “`uv sync --locked` installs the recorded environment; `uv run notesCli --help` prints the CLI.”

## 🧭 Architecture note and ADR

An architecture note names components, data flow, boundaries, and one canonical owner for each contract. An ADR records context, chosen decision, alternatives considered, and consequences at the time of the decision. Omit speculative implementation details. Example decision: “The CLI parses arguments; application code coordinates operations; adapters own subprocess execution.” Check that the code follows it.

## 🛠 How-to, troubleshooting, and testing

A how-to states prerequisites, ordered steps, expected result, and safe recovery. Troubleshooting begins with a visible symptom and a diagnostic command; distinguish a hypothesis from a confirmed cause. A testing guide lists actual commands and markers, and explicitly says when no tests exist. Do not present pytest exit code 5 as a pass.

## 📚 Contribution and releases

Contributing instructions describe one local quality command, review scope, and where to discuss changes. Issue and PR templates ask for observed behavior, reproduction, and checks without demanding secrets. Release notes list verified changes and compatibility impact; write them only when publishing a version. Preserve existing licenses and notices; do not invent a security email.

## 🔒 Facts to check

Check Python and tool versions, dependencies, commands, anchors, permissions, user-owned files, build artifacts, and external links against the current project. If a fact cannot be checked, state the limitation where it matters.

## 🌐 Portfolio and external readers

Describe the actual problem, implemented scope and known limits. Include a small
architecture diagram when it clarifies ownership, verified prerequisites and
quickstart commands, and the tests/builds a fresh reader can reproduce. Distinguish
public materials from private source and hosted production behavior. Preserve the
actual license; an absent license requires an owner decision before publication.
Keep personal resumes, hiring advice and private infrastructure details outside
project documentation. A successful check proves its stated scenario, not an
unmeasured reliability or commercial outcome.
