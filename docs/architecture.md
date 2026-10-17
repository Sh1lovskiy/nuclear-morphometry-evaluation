# Architecture and refactoring boundary

One installable CPU package is a modular monolith. The dependency direction is:

```text
CLI -> adapters / replay / analysis -> evaluation -> domain
                                  -> scalar result store
```

`domain.py` owns native IDs, validation, object profiles and strict sparse matching.
`evaluation.py` owns established scores and measurement populations.
`analysis.py` owns same-roster contrasts and explicit object interventions.
`adapters.py` owns bounded NPY and checksummed scalar-table reads.
`replay.py` recalculates saved scalar means and margin counts.
The CLI only parses arguments, coordinates these modules and serializes JSON.
No numerical module depends on a CLI, plotter, host path, network service or GPU.

Area/eccentricity extraction, native-ID compaction, strict matching and W1 semantics
were extracted from the archived shape kernel. The core source SHA256 and table
input hashes are recorded in the result manifest. The extension adds a working
interface, foreground overlap controls and explicit scope reporting. It does not
replace the archival analysis or regenerate historical optimization results.

Accidental duplicate production calculations are shared. Independent numerical
verifiers and their historical records are preserved in the private research
archive outside this repository; they remain separate from the production kernel.
The distributed CLI provides the synthetic mask demonstration and scalar replay.
There are no empty success stubs, plugins, implicit downloads, checkpoint
deserializers or background indexers.
