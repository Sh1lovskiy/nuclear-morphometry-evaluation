# Exact finite validation sequence

Run from this repository root in an isolated, bounded CPU session. Commands change
only the local project environment and generated build files. The environment
lock is an installation artifact, not evidence of scientific reproduction.

```sh
uv lock --no-config --default-index https://pypi.org/simple
uv sync --locked --group dev --no-config --default-index https://pypi.org/simple
uv run --locked ruff format .
uv run --locked ruff check . --fix
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked nucmorph demo
uv run --locked nucmorph reproduce
uv build --offline --no-config --default-index https://pypi.org/simple
uv run --locked pip-audit --progress-spinner off
```

The formatting/import-order writes above precede final source review and immutable
packaging. After review, only check mode is used. Run the documented numerical
examples and static checks again from a fresh checkout of the actual pushed commit; do not treat a
local source run as proof of a remotely available revision or passing hosted CI.
