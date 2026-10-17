# Measurement contracts

Inputs are exclusive nonnegative integer instance-label maps. Zero is background.
Native positive IDs remain objects, including disconnected parts with one ID.
Each field is processed separately; masks are bounded to 1,048,576 pixels.
The default eligibility threshold is area >=16 pixels squared. Small objects are
removed independently on each side before both object and foreground scoring.
Border-touching and disconnected objects are retained and counted explicitly;
neither flag is silently treated as an invalid or ambiguous label.

Provider ambiguity handling is an explicit adapter responsibility before this
one-field API: when a provider declares pixels invalid for scoring on both sides,
zero those same registered pixels in **both** reference and prediction maps.
The package does not infer ambiguity from a zero reference label or accept an
implicit ignore mask. NuInsSeg's supplied ambiguity regions were symmetrically
excluded in the retained study. The historical PanNuke policy instead excluded
conflicting reference pixels during native-channel conversion and left predictions
unchanged. This documented asymmetric adapter policy is preserved in the frozen
results; do not claim that a different symmetric preprocessing reruns the same
historical population. Kernel parity is conditional on identical prepared inputs.

Pixel area and second-moment eccentricity are extracted using scikit-image 0.26.0
`regionprops`. Eccentricity is dimensionless. Native pixels have no assumed
micrometre conversion. The package's area W1 is available both in pixels squared
and divided by the reference median eligible area. It implements the primary
eccentricity endpoint; it does not claim to reproduce every historical contour
or spatial descriptor.

Matching uses strict IoU >0.5 between exclusive eligible objects. The exact tie
at 0.5 is excluded. This threshold guarantees one-to-one uniqueness; arbitrary
lower thresholds require a different assignment policy and are not implemented.
Only observed intersection pairs are counted, rather than an all-object dense
matrix. Sparse IDs are compacted before accumulation.

PQ = sum(matched IoU)/(0.5*(reference count + predicted count)). Instance F1 has
the same denominator with matched count in the numerator. Empty/empty masks have
PQ/F1/Dice/IoU=1 by the explicit identity convention. Precision with no predictions,
recall with no references, SQ with no matches, and either distributional error
with an empty required population are undefined (`null`), never zero error.

All-object W1 compares all eligible objects on each side. Survivor W1 compares
only the matched reference and prediction subsets. Identical survivor features
can give zero survivor error while omitted compositions change all-object W1.
For exact whole-object deletions, fixed count k fixes PQ and count error. Equal
foreground Dice additionally requires equal omitted area U. Foreground Dice and
IoU are monotone transforms, not independent discoveries.

Contrasts use error(a)-error(b) on one common field roster. A negative contrast
means lower error for a. The conditioning change is survivor contrast minus
all-object contrast. Sign-discordance margins apply strictly to both magnitudes;
the original and qualified denominators and exact ties remain distinct.

The CDF selection identity uses fixed features and nonempty retention. Deletion
explanations recompute the actual joint measurement, not an additive attribution,
Shapley value, neural explanation or biological interaction. The independent
test suite uses direct coordinates, raster counts and stdlib sums without importing
the production functions being verified.

The `explain` command uses the supplied reference mask as an initially exact
prediction and removes a distinct set of eligible native IDs. Its omitted area
and recomputed metrics describe that precise joint counterfactual. It does not
take a saved model prediction or estimate how a network would respond. Removing
all eligible objects gives undefined distributional measurements (`null`);
it must not be interpreted as zero morphology error. No stochastic deletion or
clinical threshold is chosen by this command.
