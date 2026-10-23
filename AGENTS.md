# pythonTemplate

Read the selected [baseRules engineering policy](https://raw.githubusercontent.com/serrja/baseRules/bafcb63ed94b9769a0ca098e5db4b33c55dbc1b9/docs/engineering.md),
then the local contracts below. The URL is a pinned reading source, not an automatic
loader or permission grant. Updates require a reviewed source diff, explicit full-SHA
link change and documentation checks; no runtime/CI fetch of `latest`.

This repository owns the common Python Copier foundation and Python tooling policy. Owned Python follows PEP 8: snake_case modules, functions, variables, and internal fields; CapWords classes; UPPER_SNAKE_CASE constants. Preserve established repository names, Copier answers, CLI and wire contracts. CLI scaffolding belongs to typerTemplate; HTTP scaffolding belongs to fastApiTemplate. Historical service/native profiles remain for compatibility. Do not introduce product contracts, credentials, post-generation hooks, or business behavior. Add focused technical and regression tests for composition, packaging, and generated mechanisms. Run a disposable render for each retained profile and verify generated metadata, links, and available build commands. Keep user-owned files intact during updates. Follow docs/engineering.md for tool ownership.

Selected rules: `v0.2.0-dev.0` resolved to the full SHA above; verification is lint-only.
Template render/update and full acceptance are manual, not implicit in generation or push.
