# Data access, units and rights

Original images, labels and predictions are not distributed in this repository.
The shipped data are compact numerical study outputs with source hashes, not a
replacement dataset or a promise of full model-training reproduction.

| Dataset | Provider | Study role and units | Terms |
|---|---|---|---|
| PanNuke | [University of Warwick](https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke/) | 7,901 original fields; historical cross-fold outputs and fixed-configuration reanalysis; pixel units | Respect the provider's research/noncommercial/share-alike conditions and both dataset citations. No RGB or native label masks are redistributed here. |
| NuInsSeg | [Official dataset release](https://www.kaggle.com/datasets/ipateam/nuinsseg) | 665 original fields; external saved-output analysis; pixel units | CC BY 4.0 according to the dataset provider. Attribution is required. No native RGB or masks are included here. |
| CryoNuSeg | [Official dataset release](https://www.kaggle.com/datasets/ipateam/cryonuseg) | 30 fields from ten organs; two observers and one repeat annotation; annotation-only measurement sensitivity | Provider version 7 records MIT terms. This is not a model-transfer evaluation. No original images or masks are included here. |

The user must acquire datasets directly from providers and comply with the exact
version's terms. Copyright permission does not establish clinical validation,
new consent or an ethics waiver. No new institutional ethics opinion was issued
for this study; it reuses published data.

For a new field, export **registered** reference and prediction labels separately
as uncompressed two-dimensional integer `.npy` arrays of equal shape, e.g.
`data/example/reference.npy` and `data/example/prediction.npy`. Pass both paths
explicitly to `nucmorph evaluate`; no machine-specific dataset root is assumed.
Object IDs must be nonnegative int64-compatible labels, not semantic classes.
An RGB image, probability map, one-hot stack or compressed archive is not accepted.

The complete original raster prediction archives and original training data are
not downloadable through this repository. Dataset roots and private archives
remain external. Scalar replay is available offline; raw-mask regeneration needs
the separately retained authenticated predictions as well as provider data.
