# Naming policy

Owned Python uses PEP 8: lowercase or `snake_case` modules, functions, methods, parameters, variables, and internal fields; `CapWords` classes and exceptions; `UPPER_SNAKE_CASE` constants. New multiword Python modules use `snake_case`. Ruff formats code at the project's chosen 88-character line length and checks targeted `B`, `E`, `F`, `I`, `N`, and `UP` rules. Public docstrings explain contracts in a consistent PEP 257 style.

Repository names such as `pythonTemplate` and `fastApiTemplate`, stable Copier answers (`projectName`, `packageName`, `withPersistence`), CLI names, distribution names, environment variables, serialized fields, SQL identifiers, HTTP paths, operation IDs, and required tool filenames are separate contracts. Do not change their spelling through a code-style replacement. Newly rendered import packages are lowercase; an existing stored `packageName` is retained until its imports and consumers are migrated deliberately.

Branch and PR naming is independent of Python naming. Keep a focused branch, review its diff and outgoing commits, and use a clear `type(scope): intent` title. Any published import or wire change needs its own compatibility decision and regression check.
