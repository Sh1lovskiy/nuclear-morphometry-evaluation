# Canonical derived results

The only canonical numerical store is `src/nuclear_morphometry/results/`.
Its `manifest.json` pins each CSV's bytes, row count, SHA256 and source role.
These files preserve source identifiers exactly; they do not identify patients.

- `field_contrasts.csv`: per-field contrasts for the fixed-configuration
  three-way common eccentricity roster (7,444 PanNuke and 570 NuInsSeg fields).
- `paired_effects.csv`: all six oriented cohort/model-pair effects with direct
  conditioning changes and separate field and tissue-composition intervals.
- `margin_sensitivity.csv`: original and magnitude-qualified denominators, including
  the adverse reduction in apparent discordance at larger descriptive margins.
- `omission_replay.csv`: complete archived policy/dose summaries, including random
  controls. This file alone is not a per-object intervention replay.
- `coverage_counts.csv`, `threshold_sensitivity.csv`, `cryo_summary.csv`: supporting
  population/strict-matching/annotation summaries. Threshold sensitivities are
  preserved outputs; the new mask interface supports strict IoU >0.5 only.

The primary NuInsSeg HoVer-minus-LSP all-object and survivor means stay negative.
The direct change field interval [0.0018120297906784597, 0.006826890127686181]
and tissue-composition interval [-0.0004573517780801078, 0.008423556772871824]
are both retained. Their laws differ; one cannot stand in for the other.
Neither field-level signs nor separate interval crossings establish mean reversal.

The source study included 8,566 original fields, 25,698 canonical field-package
records, and 89,064 historical repeated predictions. These are different accounting
units, not independent biological sample counts. Nuclei, repeated fits, annotation
rounds and deletion draws share tissue and do not create patients. Missing
patient/slide linkage limits the inferential scope of conditional field resampling.

Local package labels identify LSP-DETR-derived and HoVer-NeXt-derived models and a
reduced NuLite-inspired T8 port. Their training and implementation differ; these
are not official leaderboard reproductions. CryoNuSeg analyses use annotations,
not trained segmentation predictions. Complete baseline experimental records are
retained privately; this compact repository does not bundle internal operational QA.

## Complementary metric families and exact-area controls

The complete 30-condition `metric_family_summary.csv` adds foreground pixel overlap
to the archived equal-count omission controls. In this idealized setting, PQ and
instance F1 are algebraically linked, while foreground Dice and IoU are monotone
transforms of the same area-overlap information. Equal removed-object counts do
not generally hold removed pixel area fixed. Random20 sets are averaged within
each field before cohort averaging; they are not independent tissue replicates.

The two-row `equal_count_area_summary.csv` and complete 8,566-row
`equal_count_area_fields.csv` retain every feasible, unsuccessful and ineligible
case from one deterministic restricted search. At requested 25% deletion, start
with the saved eccentricity-low omission set. Among equal integer-area groups,
exchange the lowest-eccentricity omitted nucleus for the highest-eccentricity
retained nucleus; choose the largest positive descriptor gap, then smaller native
IDs. Exactly equal integer area is required; no rounding is used. Feasible-field
Wasserstein differences are conditional counterfactual evidence, not the rate of
natural network errors. An unsuccessful restricted search is not global
infeasibility. Full omission-draw records remain in the private reproducibility
package rather than inflating this compact checkout.

`canonical_effects.csv` is the interval authority: 42 independently replayed
eccentricity effects with denominator, orientation, units, paired bootstrap law,
seed, repetitions and configuration. Main-table means are recomputed from
`field_contrasts.csv`, with intervals from this authority. `paired_effects.csv`
and `omission_replay.csv` remain byte-identical archived independent fixtures;
their overlap is intentional regression evidence, not duplicate production logic.
`exact_ties.csv` records exact zeros, strict sign opposition and both denominators
at the descriptive 0.005 margin. The primary endpoint and unfavorable uncertainty
remain unchanged. None of these tables implies clinical or patient validation.
