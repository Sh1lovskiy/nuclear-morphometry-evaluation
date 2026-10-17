# Reproduction and quality checks

Use Python 3.12. The locked core uses NumPy 2.5.3, SciPy 1.18.1 and
scikit-image 0.26.0; historical scalar files retain their original provenance and
are never silently recomputed with a new environment.

```sh
uv sync --locked --group dev --no-config --default-index https://pypi.org/simple
uv run --locked nucmorph demo
uv run --locked nucmorph reproduce
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv build --offline --no-config --default-index https://pypi.org/simple
uv run --locked pip-audit --progress-spinner off
```

`demo` and `reproduce` run fully offline once dependencies are installed. Dependency
audit needs its advisory service; network failure is not a clean audit. Source
and wheel builds use the exact backend in `pyproject.toml`, installed in an isolated
build environment by uv; the preceding sync populates its local cache. CI runs the same scientific and
static checks but no current pass is asserted without an observed workflow run.

`reproduce` verifies every scalar-file hash and recalculates all six paired means
and all 24 descriptive-margin rows from saved field-level scalar contrasts. It
fails on missing/corrupt inputs. It does not regenerate confidence intervals,
original mask features, omission per-object records, predictions or trained models.
The independent numerical verifiers and historical verification records are
retained in the private research archive outside this repository. They are not
bundled as commands here. The public interface retains the executable synthetic
mask demonstration and scalar replay; these do not claim independent biological
validation or complete historical experiment reproduction.

Each mask is one field with at most 1,048,576 pixels, processed on CPU. For large
studies call the one-field API sequentially or with externally bounded workers.
Do not pool nuclei or repeated predictions as independent bootstrap units. No
global all-image distance matrix, implicit GPU use or background task is created.
