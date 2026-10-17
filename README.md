# Nuclear Morphometry Evaluation

Repository: https://github.com/Sh1lovskiy/nuclear-morphometry-evaluation
(currently private; anonymous reviewer access is not established).

How does the choice of evaluated objects change the interpretation of nuclear
segmentation quality? This CPU package evaluates **saved instance masks**, distinguishes
whole-population from matched-survivor measurements, and replays compact derived
results from an empirical-methodological histology study. It does not train models.

## Quick start

Python 3.12 and [uv](https://docs.astral.sh/uv/) are required for the locked environment.

```sh
uv sync --locked --group dev --no-config --default-index https://pypi.org/simple
uv run --locked nucmorph demo
uv run --locked nucmorph reproduce
```

The offline demo constructs three **synthetic** equal-area objects from masks.
Deleting a square or an elongated rectangle gives the same PQ, instance F1 and
foreground Dice (0.8), but different whole-population eccentricity discrepancies.
This is an executable illustration, not a histological observation or a new metric.

```sh
uv run --locked nucmorph demo --write-masks /tmp/nucmorph-example
uv run --locked nucmorph evaluate /tmp/nucmorph-example/reference.npy /tmp/nucmorph-example/square_deleted.npy
uv run --locked nucmorph explain /tmp/nucmorph-example/reference.npy --remove 3
```

Use a new directory for `--write-masks`; existing files are never overwritten.
`explain` deletes the specified eligible native IDs from an initially exact
reference prediction and recomputes the joint measurements. It does not explain
a neural model or accept an observed prediction as its counterfactual baseline.
See the [measurement contracts](docs/methods.md) for missing-population semantics.

## Study findings and scope

- On 658 eligible NuInsSeg fields, requested 25% low-eccentricity deletion had mean
  eccentricity W1 0.0663 versus 0.0209 for equal-count random deletion. Realized
  integer doses vary by field. Equal count fixes the detection control, not generally
  foreground overlap; omitted pixel area is a separate control.
- The fixed-configuration NuInsSeg HoVer-NeXt-derived minus LSP-derived mean
  contrast remains negative: approximately -0.0069 for all objects and -0.0026
  for matched survivors. There is **no primary cohort-mean ranking reversal**.
  Individual-field signs differ in 196/570 fields; requiring both magnitudes to
  exceed 0.005 leaves 96/570 original fields or 96/357 qualified fields.
- The paired change is approximately +0.004263. Its conditional field interval
  excludes zero, whereas the tissue-composition sensitivity interval includes zero.
  These describe different resampling questions, not independent confirmations.

The [canonical scalar results](src/nuclear_morphometry/results/manifest.json) preserve
all oriented pairs, margins and adverse outcomes. See [results](docs/results.md),
[methods](docs/methods.md), [data access](docs/data.md) and
[reproduction limits](docs/reproduction.md). Historical 27-fit benchmarks, fixed-fit
shape reanalysis and annotation-only CryoNuSeg answer different questions.

The local fitted packages are not optimized official baseline implementations.
Patient/slide links are incomplete, field outputs reuse tissue context, and
historically consumed cohorts support exploratory fixed-output comparisons.
Historical task checkpoints are unavailable. There is no clinical validation,
annotation-free quality predictor, pretrained model download or complete retraining
claim. `reproduce` checks saved scalar contrasts; it does not rerun original masks,
bootstrap intervals, neural inference or training.

## Quality and citation

See [reproduction commands](docs/reproduction.md), [architecture](docs/architecture.md)
and [CITATION.cff](CITATION.cff). No publication DOI or passing-CI badge is asserted.
Original code has no open-source reuse grant at present; see [LICENSE](LICENSE).
Dataset and dependency terms are separate in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
