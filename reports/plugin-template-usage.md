# napari-plugin-template usage

Generated 2026-08-26 from npe2api `extended_summary.json` (662 plugins), GitHub repo inspection, and PyPI descriptions. The napari-plugin-template used **cookiecutter** until 2024-06-13, then switched to **copier**.

## Summary

**503 of 662 plugins (76%)** show evidence of having used the napari-plugin-template.

| era | count |
|---|---|
| cookiecutter | 291 |
| copier | 92 |
| template | 120 |
| no | 115 |
| no_github | 36 |
| unavailable | 8 |

New plugins since 2025-09-01: **128**, of which **69 (54%)** use the template.

## Methodology

Each plugin's GitHub repo (from `github_repos.csv`) is checked for template fingerprints; plugins with no reachable repo are checked via their PyPI long description. Evidence is ranked:

- **`.copier-answers.yml`** — copier-generated (napari template keys / `_src_path` -> napari-plugin-template).
- **`.cookiecutter.json`** — cookiecutter-generated (napari template keys).
- **README** — generation statement ("generated with [copier|cookiecutter] using the [napari-plugin-template|cookiecutter-napari-plugin]"), the template badge block (napari-hub shields + codecov), or the template README footer.
- **`.napari-hub/` + `.github/workflows/test_and_deploy.yml`** — weak signal.
- **PyPI description** — same markers, used as fallback for no_github / deleted / private repos.

Eras: **cookiecutter** (pre-2024-06), **copier** (2024-06+), **template** (evidence but era ambiguous), **no** (no evidence found), **no_github** (no GitHub URL in metadata), **unavailable** (repo gone).

## New plugins since 2025-09-01 using the template

**69** of 128 new plugins.

| name | first_release | template_era | evidence |
|---|---|---|---|
| ndev-settings | 2025-09-04 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-omero-downloader-cci | 2025-09-04 | copier | .copier-answers.yml |
| orchardseg | 2025-09-10 | template | README template badge block |
| orseg | 2025-09-10 | copier | .copier-answers.yml; README template badge block |
| cryovit-napari | 2025-09-23 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-orientation | 2025-10-10 | copier | pypi description: generated with copier via napari-plugin-template |
| patchlabel | 2025-10-13 | copier | pypi description: generated with copier via napari-plugin-template |
| ndevio | 2025-10-14 | template | README template badge block |
| napari-orthogonal-views | 2025-10-15 | copier | README: generated with copier via napari-plugin-template |
| segment-any-confocal-images | 2025-10-31 | copier | pypi description: generated with copier via napari-plugin-template |
| secondharmonic | 2025-11-01 | copier | README: generated with copier via napari-plugin-template |
| napari-synaptogram | 2025-11-06 | copier | .copier-answers.yml; README template badge block |
| napari-musa | 2025-11-10 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-multi-channel-surface | 2025-11-12 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-micromorph | 2025-11-19 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-signal-classifier | 2025-11-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-piscis | 2025-11-28 | template | pypi description: template badge block |
| napari-stream | 2025-12-02 | copier | pypi description: generated with copier via napari-plugin-template |
| morphodeep | 2025-12-08 | copier | pypi description: generated with copier via napari-plugin-template |
| nagini3d-napari | 2025-12-08 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-3d-label-eraser | 2025-12-09 | template | pypi description: template badge block |
| napari-segmentation-toolbox | 2025-12-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| ndev-workflows | 2025-12-22 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-plugin-test-ferrinm | 2025-12-23 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| pyphenix | 2026-01-02 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| gfap-segmenter | 2026-01-08 | template | pypi description: template badge block |
| napari-ft | 2026-01-19 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-metadata | 2026-01-20 | template | README template badge block |
| napari-mlarray | 2026-01-30 | template | pypi description: template badge block |
| napari-bbox-fix | 2026-02-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-myelin-quantifier | 2026-02-06 | copier | .copier-answers.yml |
| deepphenotree | 2026-02-09 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-ortho | 2026-02-18 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-etminflux-data-viewer | 2026-02-20 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-yolopt | 2026-02-23 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-TopoStats | 2026-02-25 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-resview | 2026-02-26 | copier | .copier-answers.yml; README template badge block |
| napari-grid-curator | 2026-03-03 | template | none; pypi description: template README footer |
| ome-zarrpari | 2026-03-11 | template | README template badge block |
| napari-mouse-tumour-annotation | 2026-03-17 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-layer-statistics | 2026-03-26 | copier | README: generated with copier via napari-plugin-template |
| emcfsys | 2026-03-31 | template | pypi description: template README footer |
| tomopari | 2026-04-03 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-clipping-planes-controls | 2026-04-08 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-pyvertexmodel | 2026-04-09 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| ellipse-nuclei-segmentation | 2026-04-13 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-saveas-dtype | 2026-04-14 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-iss-tdflim-reader | 2026-04-26 | copier | .copier-answers.yml; README template badge block |
| napari-colocalization | 2026-04-30 | copier | .copier-answers.yml; README template badge block |
| napari-spam | 2026-05-08 | template | pypi description: template README footer |
| napari-morans-i | 2026-05-09 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| microglia-analyzer | 2026-05-11 | template | .napari-hub/ + test_and_deploy.yml |
| filament-toolbox | 2026-05-17 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-czi | 2026-05-19 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-cci-annotator2 | 2026-05-27 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-persistent-homology | 2026-06-01 | copier | .copier-answers.yml; README template badge block |
| napari-isbem | 2026-06-09 | template | README template badge block |
| napari-hdf5-reader | 2026-06-24 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-n5 | 2026-06-26 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| aiod-napari | 2026-06-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| w-seg-napari | 2026-07-07 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-dm4topng | 2026-07-13 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-gribberish | 2026-07-14 | copier | .copier-answers.yml; README template badge block |
| napari-microscopy-metrics | 2026-07-15 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-segmencolo | 2026-07-27 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-flopa | 2026-07-28 | copier | .copier-answers.yml |
| focus-3d | 2026-08-16 | template | pypi description: template badge block |
| napari-volume-spin | 2026-08-24 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-storm | 2026-08-25 | template | none; pypi description: template README footer |

### New plugins NOT flagged

| name | first_release | template_era |
|---|---|---|
| napari-mcp | 2025-09-15 | no |
| napari-unet | 2025-10-09 | no |
| quanti-fret | 2025-10-27 | no_github |
| napari-ome-arrow | 2025-11-15 | no |
| napari-voxtell | 2025-12-27 | no |
| napari-bruce | 2026-01-05 | no_github |
| napari-easytrack | 2026-01-07 | no_github |
| napari-rosettasciio | 2026-01-19 | no_github |
| WellMapper | 2026-01-26 | no_github |
| napari-hydra | 2026-01-29 | no |
| senoquant | 2026-01-31 | no |
| neuro-sam | 2026-02-02 | no |
| confusius | 2026-02-11 | no_github |
| napari-molecular-cartography-viewer | 2026-02-21 | no_github |
| napari-mask-curator | 2026-02-21 | no_github |
| napari-manual-labels-editor | 2026-02-22 | no_github |
| napari-bacteria-density | 2026-03-04 | unavailable |
| napari-npifile | 2026-03-14 | no_github |
| napari-padbound | 2026-03-15 | no |
| simple-napari-cci-annotator | 2026-03-20 | no_github |
| napari-nd2-spectral-ome-zarr | 2026-03-22 | no |
| napari-chat-assistant | 2026-03-25 | no |
| napari-reco-plugin | 2026-04-03 | no |
| napari-simple-tracker | 2026-04-08 | no |
| napari-sam3-assistant | 2026-04-18 | no |
| napari-fenestra | 2026-04-22 | no |
| napari-hardware-monitor | 2026-04-25 | no |
| napari-atlas-stitch | 2026-04-28 | no |
| napari-cotrack | 2026-05-01 | no |
| napari-unet-assistant | 2026-05-03 | no |
| napari-training-assistant | 2026-05-03 | no_github |
| napari-em-assistant | 2026-05-05 | no |
| napari-cilia-assistant | 2026-05-08 | no |
| napari-fungiform | 2026-05-14 | unavailable |
| napari-demo-assistant | 2026-05-16 | no |
| napari-harpy | 2026-05-19 | no |
| napari-racc | 2026-05-29 | no |
| biopb-mcp | 2026-05-29 | no |
| micro-sam | 2026-06-04 | no |
| napari-macrophage | 2026-06-05 | no_github |
| napari-vipp | 2026-06-25 | no |
| pentachrome-plugin | 2026-06-26 | unavailable |
| napari-pdr | 2026-06-26 | no |
| bio_oct | 2026-06-30 | no_github |
| napari-chunked-regionprops | 2026-07-02 | no |
| openuc2-processor | 2026-07-05 | no |
| napasserelle | 2026-07-15 | no_github |
| napari-zarrnii | 2026-07-16 | no_github |
| napari-microplate | 2026-07-17 | no |
| divisualisation | 2026-07-23 | no |
| napari-atlas-cci | 2026-07-24 | no_github |
| myopari | 2026-07-29 | no_github |
| napari-worm-neuron-annotator | 2026-07-30 | no |
| napari-flowreg-formats | 2026-08-08 | no |
| frontvegV2 | 2026-08-09 | unavailable |
| napari-quantem | 2026-08-10 | no |
| HaemoLynx | 2026-08-10 | no |
| napari-cta | 2026-08-13 | no |
| napari-nucleation-analyzer | 2026-08-20 | no_github |

## All plugins

| name | first_release | template_era | evidence |
|---|---|---|---|
| LSFM-destripe-napari | 2024-12-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| LSFM-fusion-napari | 2024-12-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| MMV-playground | 2025-01-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| PartSeg-smfish | 2022-10-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| PlatyMatch | 2021-05-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| PoseR-napari | 2023-02-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| aiod-napari | 2026-06-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| arcos-gui | 2022-02-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| avidaq | 2022-07-21 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| bbii-decon | 2021-12-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| brainglobe-registration | 2025-01-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| brainglobe-stitch | 2024-10-16 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| brainrender-napari | 2023-10-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| cellpose-napari | 2021-04-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| cochlea-synapseg | 2024-11-07 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| cut-detector | 2023-10-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| disease-classifier | 2022-06-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| fish-scan | 2024-08-14 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| generate-dense-patches | 2023-09-12 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| grabber-ift | 2021-12-12 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| guanine-crystal-analysis | 2022-07-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| hesperos | 2022-05-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| iacs-ipac-reader | 2022-01-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| iterseg | 2023-12-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| koopa-viz | 2022-09-29 | cookiecutter | none; pypi description: generated with cookiecutter via cookiecutter-napari-plug |
| lasso-3d | 2025-01-09 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| manini | 2023-11-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| mmv-h4cells | 2024-10-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| mmv-h4tracks | 2024-03-22 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| morphometrics | 2022-03-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| morphometrics-engine | 2022-10-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| multireg | 2023-06-09 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napam | 2024-04-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-3D-registration | 2025-07-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-3d-counter | 2023-10-18 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-3d-ortho-viewer | 2021-12-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-DeepSpot | 2021-11-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-EMD | 2023-08-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-IDS | 2022-02-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-IP-workflow | 2022-05-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-J | 2022-01-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-PHILOW | 2022-05-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-PixSeq | 2024-02-29 | cookiecutter | none; pypi description: generated with cookiecutter via cookiecutter-napari-plug |
| napari-SAM4IS | 2023-04-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-TopoStats | 2026-02-25 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-accelerated-pixel-and-object-classification | 2021-10-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-affinities | 2022-06-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-aideveloper | 2022-05-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-allencell-annotator | 2022-07-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-allencell-segmenter | 2021-06-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-amdtrk | 2023-04-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-animated-gif-io | 2021-12-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-annotatorj | 2022-05-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-aphid | 2023-01-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-apple | 2022-06-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-apr-viewer | 2021-11-30 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bacseg | 2023-02-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-basicpy | 2022-01-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bbox | 2023-03-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bbox-fix | 2026-02-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bfio | 2023-08-18 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bigfish | 2023-04-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bigwarp | 2022-01-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bil-data-viewer | 2022-01-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bio-sample-data | 2022-07-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-biomag-annotator | 2024-01-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bleach-correct | 2022-09-22 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-blender | 2024-07-03 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-blob-detection | 2022-04-22 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-blosc2 | 2024-07-11 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-blossom | 2022-06-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-boardgame-maker | 2023-08-13 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-boids | 2022-08-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-boxmanager | 2022-09-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-brainbow-diagnose | 2023-01-25 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-brightness-contrast | 2021-08-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-brushsettings | 2021-08-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-bud-cell-segmenter | 2022-11-14 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-buds | 2022-08-16 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-calibration | 2022-08-23 | cookiecutter | none; pypi description: generated with cookiecutter via cookiecutter-napari-plug |
| napari-ccp4map | 2021-10-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cell-centroid-annotator | 2023-03-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cellseg3d | 2022-06-25 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-checkerboard | 2021-05-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-clemreg | 2021-06-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-clipboard | 2023-08-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-compressed-labels-io | 2021-02-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-conference | 2023-09-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-conidie | 2022-12-15 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-console | 2021-01-21 | cookiecutter | none; pypi description: generated with cookiecutter via cookiecutter-napari-plug |
| napari-cookiecut | 2022-10-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-copick | 2025-07-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-crop | 2021-10-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cryoet-data-portal | 2023-08-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cryofibsem-imgproc | 2024-09-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cryofibsem-monitor | 2021-11-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cupy-image-processing | 2021-10-22 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-cursor-tracker | 2023-10-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-curtain | 2021-11-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-curviewer | 2023-12-25 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-czann-segment | 2022-07-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-deepfinder | 2022-07-25 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-deeplabcut | 2022-06-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-deepmeta | 2021-06-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-dexp | 2021-07-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-dmc-brainmap | 2025-02-18 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-dvid | 2021-06-09 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-dzi-zarr | 2020-08-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-easy-augment-batch-dl | 2024-08-18 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-ehooke | 2023-03-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-em-reader | 2021-02-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-exodeepfinder | 2024-06-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-fast4dreg | 2024-07-03 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-features-selector | 2023-03-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-figure | 2023-06-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-filament-annotator | 2022-10-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-filaments | 2022-07-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-file2folder | 2024-10-28 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-folder-browser | 2021-10-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-generic-SIMulator | 2022-06-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-grid-cropping | 2024-10-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-h5 | 2023-08-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-hdf5-labels-io | 2021-03-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-help | 2022-07-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-hierarchical | 2022-12-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-image-stacker | 2022-01-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-imaris-loader | 2021-10-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-imodmodel | 2024-04-16 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-imsmicrolink | 2021-12-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-indices | 2023-05-30 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-input-visualizer | 2022-10-10 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-k2-WaveBreaker | 2024-12-02 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-kics | 2022-05-02 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-label-interpolator | 2022-09-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-labelimg4classification | 2021-12-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-labeling | 2022-05-09 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-labelling-assistant | 2022-01-19 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-labelprop | 2023-06-19 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-labels-overlap | 2021-11-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-large-image-importer | 2023-02-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-layer-details-display | 2021-11-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-layer-table | 2022-04-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-lazy-openslide | 2020-07-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-listener | 2023-03-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-live-flim | 2022-11-09 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-live-recording | 2021-10-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-locan | 2023-10-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-locpix | 2023-01-16 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-macrokit | 2023-01-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-manual-registration | 2024-08-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mat-file-reader | 2022-11-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mat-images | 2020-03-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-math | 2022-01-18 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-merge-stardist-masks | 2022-08-31 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-meshio | 2023-03-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-metroid | 2022-03-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-micromorph | 2025-11-19 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-microtubule-analyzer | 2023-10-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mm3 | 2022-06-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-molecule-reader | 2021-12-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-moltrack | 2024-05-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mouse-controls | 2021-10-30 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mrcfile-handler | 2021-08-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mrcfile-reader | 2020-10-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-mzarr | 2023-06-02 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nD-annotator | 2022-06-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nanopyx | 2023-05-10 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-napari | 2023-04-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nasa-samples | 2022-07-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nd2-folder-viewer | 2022-08-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-ndev | 2023-01-31 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-ndtiffs | 2020-05-06 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nibabel | 2023-02-10 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nifti | 2023-04-18 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-nikon-nd2 | 2021-02-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-obj | 2023-04-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-omaas | 2022-08-09 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-ome-zarr | 2021-06-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-openfibsem | 2023-09-22 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-opt-handler | 2024-07-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-organoid-counter | 2022-04-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-parallel | 2023-09-20 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-patchcreator | 2022-08-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pdr-reader | 2022-07-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pixel-correction | 2022-09-19 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-plot | 2022-01-09 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-plot-profile | 2021-08-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-plugin-search | 2021-08-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-points2regions | 2024-01-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pointslayer-projection | 2023-02-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-potential-field-navigation | 2024-02-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-power-spectrum | 2022-04-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-power-widgets | 2022-11-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pram | 2022-04-29 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-properties-plotter | 2021-05-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-properties-viewer | 2021-04-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-psf-analysis | 2022-03-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-psf-simulator | 2022-04-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pssr | 2022-11-18 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pyav | 2024-10-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pymeshlab | 2022-01-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-pystackreg | 2022-07-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-qrcode | 2023-02-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-quoll | 2022-08-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-rembg | 2023-09-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-result-stack | 2023-01-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-rioxarray | 2022-09-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-roi-manager | 2024-02-25 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-roi-registration | 2022-05-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sairyscan | 2022-06-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sc3D-viewer | 2022-06-21 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-script-editor | 2021-11-06 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sdeconv | 2021-09-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-seedseg | 2023-05-09 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-segment-anything | 2023-04-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-segment-anything-2 | 2024-07-30 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-segment-blobs-and-things-with-membranes | 2021-09-25 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-segment-everything | 2024-04-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-segmentation-overlap-filter | 2024-06-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-segmentation-toolbox | 2025-12-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-shape-odyssey | 2023-08-31 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sif-reader | 2022-11-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sift-registration | 2022-07-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-signal-classifier | 2025-11-26 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sim-processor | 2022-05-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-simpleannotate | 2023-10-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-sketchpose | 2023-11-07 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-skimage | 2024-05-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-skimage-regionprops | 2021-06-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-solarized | 2023-01-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-spacetx-explorer | 2021-09-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-spatial-correlation-plotter | 2024-08-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-spatial-omics | 2021-12-10 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-splinebox | 2024-10-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-splinedist | 2022-10-18 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-splineit | 2022-07-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-spofi | 2024-02-07 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-spreadsheet | 2022-08-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-stable-diffusion | 2022-10-27 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-stl-exporter | 2021-10-06 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-stracking | 2021-08-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-superres | 2023-06-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-svetlana | 2022-11-22 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-svg | 2020-04-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tabu | 2021-10-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tapenade-processing | 2024-08-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tiff | 2024-02-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tiler | 2021-12-13 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-time-series-plotter | 2021-12-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-time-slicer | 2021-11-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-timelapse-processor | 2024-07-15 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-timeseries-opener-plugin | 2022-02-28 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tomocube-data-viewer | 2023-03-06 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-toska | 2024-07-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tracks-reader | 2021-05-11 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-trait2d | 2022-07-09 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-turing | 2022-08-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-tyssue | 2022-10-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-ufish | 2023-09-30 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-ui-tracer | 2023-03-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-umap | 2022-11-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-unicell | 2022-11-12 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-utrack-loader | 2024-05-31 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-validate-random-label-predictions | 2022-11-23 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-vedo-bridge | 2023-07-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-vesicles-segmentation | 2022-07-08 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-video-cvdask | 2022-02-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-vodex | 2023-01-04 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-workflow-optimizer | 2021-12-24 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-workshop-browser | 2023-07-05 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-workshop-plugin | 2023-09-06 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-yapic-prediction | 2021-04-19 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-yolo5-mitosis-detector | 2023-12-15 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-yolov5 | 2021-12-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-zelda | 2021-10-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| napari-zplane-depth-colorizer | 2024-10-14 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| natari | 2021-10-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| okapi-em | 2022-10-19 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| ortho-view-napari | 2021-06-15 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| palmari | 2022-05-06 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| platelet-unet-watershed | 2021-07-01 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| set-calibration | 2023-11-03 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| snouty-viewer | 2022-08-31 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| spots-in-yeasts | 2023-08-29 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| test-detect-spots | 2023-04-20 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| tomopari | 2026-04-03 | cookiecutter | pypi description: generated with cookiecutter via cookiecutter-napari-plugin |
| vollseg-napari-mtrack | 2022-12-20 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| vollseg-napari-trackmate | 2022-12-31 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| workshop-demo | 2021-12-15 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| yt-napari | 2022-05-02 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| zarpaint | 2021-06-17 | cookiecutter | README: generated with cookiecutter via cookiecutter-napari-plugin |
| AppleT3 | 2025-04-19 | copier | README: generated with copier via napari-plugin-template |
| brendan-beads | 2025-05-20 | copier | pypi description: generated with copier via napari-plugin-template |
| cryovit-napari | 2025-09-23 | copier | pypi description: generated with copier via napari-plugin-template |
| deepphenotree | 2026-02-09 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| ellipse-nuclei-segmentation | 2026-04-13 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| filament-toolbox | 2026-05-17 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| frontveg | 2025-04-20 | copier | README: generated with copier via napari-plugin-template |
| fspi-analysis | 2025-05-18 | copier | README: generated with copier via napari-plugin-template |
| mmv-regionseg | 2025-03-21 | copier | README: generated with copier via napari-plugin-template |
| mobiofox | 2025-07-21 | copier | README: generated with copier via napari-plugin-template |
| morphodeep | 2025-12-08 | copier | pypi description: generated with copier via napari-plugin-template |
| nagini3d-napari | 2025-12-08 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-animation | 2021-04-23 | copier | .copier-answers.yml; README template badge block |
| napari-annotator | 2022-03-07 | copier | README: generated with copier via napari-plugin-template |
| napari-automatic-range | 2025-07-15 | copier | README: generated with copier via napari-plugin-template |
| napari-bioio-reader | 2025-07-04 | copier | README: generated with copier via napari-plugin-template |
| napari-bluesky | 2024-11-29 | copier | README: generated with copier via napari-plugin-template |
| napari-camera | 2025-03-26 | copier | README: generated with copier via napari-plugin-template |
| napari-cci-annotator | 2025-05-26 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-cci-annotator2 | 2026-05-27 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-clipping-planes-controls | 2026-04-08 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-colocalization | 2026-04-30 | copier | .copier-answers.yml; README template badge block |
| napari-czi | 2026-05-19 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-czitools | 2025-08-20 | copier | README: generated with copier via napari-plugin-template |
| napari-data-inspection | 2025-06-16 | copier | README: generated with copier via napari-plugin-template |
| napari-dm4topng | 2026-07-13 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-etminflux-data-viewer | 2026-02-20 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-filter-labels-by-prop | 2025-01-24 | copier | README: generated with copier via napari-plugin-template |
| napari-flopa | 2026-07-28 | copier | .copier-answers.yml |
| napari-fluoresfm | 2025-07-22 | copier | README: generated with copier via napari-plugin-template |
| napari-ft | 2026-01-19 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-geff | 2025-07-23 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-gribberish | 2026-07-14 | copier | .copier-answers.yml; README template badge block |
| napari-gruvbox | 2022-12-14 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-hdf5-reader | 2026-06-24 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-himena | 2025-04-08 | copier | README: generated with copier via napari-plugin-template |
| napari-hsi-analysis | 2025-03-12 | copier | README: generated with copier via napari-plugin-template |
| napari-iss-tdflim-reader | 2026-04-26 | copier | .copier-answers.yml; README template badge block |
| napari-kld | 2024-07-31 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-kldeconv | 2025-08-04 | copier | README: generated with copier via napari-plugin-template |
| napari-label-manager | 2025-07-10 | copier | none; pypi description: generated with copier via napari-plugin-template |
| napari-labels | 2025-03-26 | copier | README: generated with copier via napari-plugin-template |
| napari-laber-manager | 2025-07-07 | copier | none; pypi description: generated with copier via napari-plugin-template |
| napari-layer-divider | 2025-07-29 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-layer-statistics | 2026-03-26 | copier | README: generated with copier via napari-plugin-template |
| napari-mask-density | 2025-04-11 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-mass | 2025-06-30 | copier | README: generated with copier via napari-plugin-template |
| napari-memmap-tiff | 2025-06-10 | copier | README: generated with copier via napari-plugin-template |
| napari-microscopy-metrics | 2026-07-15 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-morans-i | 2026-05-09 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-mouse-tumour-annotation | 2026-03-17 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-multi-channel-surface | 2025-11-12 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-musa | 2025-11-10 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-myelin-quantifier | 2026-02-06 | copier | .copier-answers.yml |
| napari-n5 | 2026-06-26 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-nninteractive | 2025-03-11 | copier | README: generated with copier via napari-plugin-template |
| napari-noise2vst | 2025-08-03 | copier | README: generated with copier via napari-plugin-template |
| napari-nuclephaser | 2025-04-02 | copier | README: generated with copier via napari-plugin-template |
| napari-omero-downloader-cci | 2025-09-04 | copier | .copier-answers.yml |
| napari-orientation | 2025-10-10 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-ortho | 2026-02-18 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-orthogonal-views | 2025-10-15 | copier | README: generated with copier via napari-plugin-template |
| napari-persistent-homology | 2026-06-01 | copier | .copier-answers.yml; README template badge block |
| napari-plugin-test-ferrinm | 2025-12-23 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-proofread-brainbow | 2022-08-30 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-psfgenerator | 2025-02-05 | copier | README: generated with copier via napari-plugin-template |
| napari-pyvertexmodel | 2026-04-09 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-resview | 2026-02-26 | copier | .copier-answers.yml; README template badge block |
| napari-roxas-ai | 2025-05-17 | copier | README: generated with copier via napari-plugin-template |
| napari-sam2long | 2025-04-14 | copier | README: generated with copier via napari-plugin-template |
| napari-saveas-dtype | 2026-04-14 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-segmencolo | 2026-07-27 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-segselect | 2025-01-31 | copier | README: generated with copier via napari-plugin-template |
| napari-stream | 2025-12-02 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-swc-editor | 2024-12-03 | copier | README: generated with copier via napari-plugin-template |
| napari-swc-reader | 2024-11-14 | copier | README: generated with copier via napari-plugin-template |
| napari-synaptogram | 2025-11-06 | copier | .copier-answers.yml; README template badge block |
| napari-tree-rings | 2025-08-11 | copier | pypi description: generated with copier via napari-plugin-template |
| napari-vector-graphics | 2025-01-02 | copier | README: generated with copier via napari-plugin-template |
| napari-vectorizer | 2025-02-28 | copier | README: generated with copier via napari-plugin-template |
| napari-volume-spin | 2026-08-24 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| napari-yolopt | 2026-02-23 | copier | pypi description: generated with copier via napari-plugin-template |
| ndev-settings | 2025-09-04 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| ndev-themes | 2025-08-29 | copier | README: generated with copier via napari-plugin-template |
| ndev-workflows | 2025-12-22 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| orseg | 2025-09-10 | copier | .copier-answers.yml; README template badge block |
| patchlabel | 2025-10-13 | copier | pypi description: generated with copier via napari-plugin-template |
| pyphenix | 2026-01-02 | copier | .copier-answers.yml; README: generated with copier via napari-plugin-template |
| secondharmonic | 2025-11-01 | copier | README: generated with copier via napari-plugin-template |
| segment-any-confocal-images | 2025-10-31 | copier | pypi description: generated with copier via napari-plugin-template |
| segment-embryo | 2024-11-27 | copier | README: generated with copier via napari-plugin-template |
| w-seg-napari | 2026-07-07 | copier | pypi description: generated with copier via napari-plugin-template |
| AxonDeepSeg | 2017-12-09 | no | none |
| HaemoLynx | 2026-08-10 | no | none |
| PartSeg | 2019-01-14 | no | none |
| RedLionfish | 2021-11-19 | no | none |
| acquifer-napari | 2023-07-07 | no | none |
| affinder | 2021-02-04 | no | none |
| allencell-segmenter-ml | 2024-09-20 | no | none |
| anchor-droplet-chip | 2023-03-13 | no | none |
| annotrack | 2023-12-01 | no | none |
| beetlesafari | 2021-06-04 | no | none |
| biopb-mcp | 2026-05-29 | no | none |
| blik | 2021-06-15 | no | none |
| brillouin-imaging | 2025-08-13 | no | none |
| btrack | 2020-05-27 | no | none |
| cellcanvas | 2024-03-10 | no | none |
| cryocanvas | 2024-02-02 | no | none |
| divisualisation | 2026-07-23 | no | none |
| domb-napari | 2023-11-22 | no | none |
| empanada-napari | 2022-03-04 | no | none |
| epicure | 2024-10-18 | no | none |
| epitools | 2023-05-04 | no | none |
| faser | 2022-05-23 | no | none |
| fishfeats | 2025-08-19 | no | none |
| hipocount-napari | 2024-02-05 | no | none |
| ilastik-napari | 2023-02-28 | no | none |
| micro-sam | 2026-06-04 | no | none |
| microscope-napari | 2024-06-21 | no | none |
| midi-app-controller | 2024-06-05 | no | none |
| mikro-napari | 2021-09-30 | no | none |
| motile-tracker | 2024-12-18 | no | none |
| mousechd-napari | 2023-11-18 | no | none |
| movement | 2020-04-02 | no | none |
| napari | 2018-07-30 | no | none |
| napari-UniSPAC | 2025-02-07 | no | none |
| napari-afmreader | 2025-06-07 | no | none |
| napari-aicsimageio | 2020-03-26 | no | none |
| napari-arboretum | 2021-05-11 | no | none |
| napari-atlas-stitch | 2026-04-28 | no | none |
| napari-bioformats | 2021-06-25 | no | none |
| napari-chat-assistant | 2026-03-25 | no | none |
| napari-chatgpt | 2023-05-03 | no | none |
| napari-chunked-regionprops | 2026-07-02 | no | none |
| napari-cilia-assistant | 2026-05-08 | no | none |
| napari-cosmos-ts | 2024-04-11 | no | none |
| napari-cotrack | 2026-05-01 | no | none |
| napari-cta | 2026-08-13 | no | none |
| napari-czi-reader | 2025-05-27 | no | none |
| napari-czifile2 | 2021-02-02 | no | none |
| napari-demo-assistant | 2026-05-16 | no | none |
| napari-dinosim | 2025-03-05 | no | none |
| napari-dv | 2020-02-02 | no | none |
| napari-em-assistant | 2026-05-05 | no | none |
| napari-epyseg | 2025-02-12 | no | none |
| napari-error-reporter | 2022-02-13 | no | none |
| napari-event-monitor | 2025-07-16 | no | none |
| napari-features | 2021-06-17 | no | none |
| napari-fenestra | 2026-04-22 | no | none |
| napari-file-watcher | 2023-01-16 | no | none |
| napari-flowreg | 2025-08-22 | no | none |
| napari-flowreg-formats | 2026-08-08 | no | none |
| napari-gemspa | 2023-05-29 | no | none |
| napari-hardware-monitor | 2026-04-25 | no | none |
| napari-harpy | 2026-05-19 | no | none |
| napari-hydra | 2026-01-29 | no | none |
| napari-imc | 2021-01-19 | no | none |
| napari-lattice | 2022-07-19 | no | none |
| napari-mcp | 2025-09-15 | no | none |
| napari-micromanager | 2021-08-15 | no | none |
| napari-microplate | 2026-07-17 | no | none |
| napari-nd2-spectral-ome-zarr | 2026-03-22 | no | none |
| napari-nucleaizer | 2021-09-08 | no | none |
| napari-nyxus | 2023-05-05 | no | none |
| napari-ome-arrow | 2025-11-15 | no | none |
| napari-omero | 2020-06-24 | no | none |
| napari-padbound | 2026-03-15 | no | none |
| napari-pdf-reader | 2021-11-05 | no | none |
| napari-pdr | 2026-06-26 | no | none |
| napari-pitcount-cfim | 2025-04-24 | no | none |
| napari-quantem | 2026-08-10 | no | none |
| napari-racc | 2026-05-29 | no | none |
| napari-reco-plugin | 2026-04-03 | no | none |
| napari-roi | 2021-11-19 | no | none |
| napari-sam3-assistant | 2026-04-18 | no | none |
| napari-save-transformed | 2024-07-02 | no | none |
| napari-simple-tracker | 2026-04-08 | no | none |
| napari-spotiflow | 2024-02-02 | no | none |
| napari-tardis-em | 2024-07-22 | no | none |
| napari-unet | 2025-10-09 | no | none |
| napari-unet-assistant | 2026-05-03 | no | none |
| napari-update-checker | 2024-12-23 | no | none |
| napari-vipp | 2026-06-25 | no | none |
| napari-voxtell | 2025-12-27 | no | none |
| napari-worm-neuron-annotator | 2026-07-30 | no | none |
| napari-wsi | 2023-02-01 | no | none |
| napari_video | 2021-02-27 | no | none |
| napping | 2021-02-02 | no | none |
| nellie | 2024-03-21 | no | none |
| neuro-sam | 2026-02-02 | no | none |
| neurofly | 2024-10-30 | no | none |
| neurogenesis-napari | 2025-07-29 | no | none |
| nfinder | 2021-12-06 | no | none |
| openuc2-processor | 2026-07-05 | no | none |
| platetrack | 2023-12-03 | no | none |
| psf-analysis-CFIM | 2025-02-11 | no | none |
| psfmodels | 2019-09-15 | no | none |
| pssr | 2024-04-17 | no | none |
| pycudadecon | 2022-08-10 | no | none |
| recOrder-napari | 2022-04-19 | no | none |
| samcell-napari | 2025-04-02 | no | none |
| senoquant | 2026-01-31 | no | none |
| seu-3d | 2025-05-26 | no | none |
| skan | 2016-11-08 | no | none |
| smo | 2021-09-21 | no | none |
| stardist-napari | 2021-06-01 | no | none |
| unet-lungs-segmentation | 2025-03-12 | no | none |
| AlveolEye | 2024-05-22 | no_github | nan |
| WellMapper | 2026-01-26 | no_github | nan |
| bio_oct | 2026-06-30 | no_github | nan |
| cell-AAP | 2024-05-28 | no_github | nan |
| cellpose-counter | 2024-11-21 | no_github | nan |
| confusius | 2026-02-11 | no_github | nan |
| myopari | 2026-07-29 | no_github | nan |
| napari-3dtimereg | 2024-04-05 | no_github | nan |
| napari-annotate | 2022-11-03 | no_github | nan |
| napari-atlas-cci | 2026-07-24 | no_github | nan |
| napari-bioimageio | 2022-07-05 | no_github | nan |
| napari-bootstrapper | 2025-05-23 | no_github | nan |
| napari-bruce | 2026-01-05 | no_github | nan |
| napari-easytrack | 2026-01-07 | no_github | nan |
| napari-findaureus | 2024-04-20 | no_github | nan |
| napari-hello | 2023-04-16 | no_github | nan |
| napari-hippo | 2024-01-31 | no_github | nan |
| napari-hough-circle-detector | 2023-04-03 | no_github | nan |
| napari-macrophage | 2026-06-05 | no_github | nan |
| napari-manual-labels-editor | 2026-02-22 | no_github | nan |
| napari-mask-curator | 2026-02-21 | no_github | nan |
| napari-mclabel | 2023-07-09 | no_github | nan |
| napari-microscope | 2021-01-22 | no_github | nan |
| napari-molecular-cartography-viewer | 2026-02-21 | no_github | nan |
| napari-multitask | 2021-12-06 | no_github | nan |
| napari-npifile | 2026-03-14 | no_github | nan |
| napari-nucleation-analyzer | 2026-08-20 | no_github | nan |
| napari-rosettasciio | 2026-01-19 | no_github | nan |
| napari-text-layer | 2021-10-30 | no_github | nan |
| napari-training-assistant | 2026-05-03 | no_github | nan |
| napari-zarrnii | 2026-07-16 | no_github | nan |
| napasserelle | 2026-07-15 | no_github | nan |
| qhyccd-capture | 2024-10-23 | no_github | nan |
| quanti-fret | 2025-10-27 | no_github | nan |
| simple-napari-cci-annotator | 2026-03-20 | no_github | nan |
| ultrack | 2023-06-07 | no_github | nan |
| Image-Composer | 2022-01-10 | template | none; pypi description: template README footer |
| Image-Part-Selecter | 2022-01-12 | template | none; pypi description: template README footer |
| Label-Creator | 2022-01-12 | template | none; pypi description: template README footer |
| Large-Image-Viewer | 2023-08-08 | template | pypi description: template badge block |
| Layer-Data-Replace | 2022-01-13 | template | none; pypi description: template README footer |
| MSI-Explorer | 2023-07-20 | template | README template badge block |
| Offset-Subtraction | 2022-01-13 | template | none; pypi description: template README footer |
| Partial-Aligner | 2022-01-14 | template | none; pypi description: template README footer |
| World2Data | 2022-01-14 | template | none; pypi description: template README footer |
| arcosPx-napari | 2025-03-27 | template | .napari-hub/ + test_and_deploy.yml |
| brainglobe-napari-io | 2021-03-12 | template | README template badge block |
| brainglobe-segmentation | 2023-11-06 | template | README template badge block |
| brainglobe-utils | 2023-06-23 | template | README template badge block |
| brainreg | 2020-05-26 | template | README template badge block |
| brainways | 2023-05-26 | template | README template badge block |
| careamics-napari | 2024-10-20 | template | .napari-hub/ + test_and_deploy.yml |
| cellfinder | 2020-01-17 | template | README template badge block |
| cylindra | 2024-05-01 | template | pypi description: template badge block |
| darth-d | 2023-10-26 | template | README template badge block |
| devbio-napari | 2021-06-08 | template | README template badge block |
| elastix-napari | 2021-03-24 | template | none; pypi description: template README footer |
| emcfsys | 2026-03-31 | template | pypi description: template README footer |
| featureforest | 2024-10-10 | template | README template badge block |
| fitellipsoid | 2025-04-08 | template | pypi description: template badge block |
| focus-3d | 2026-08-16 | template | pypi description: template badge block |
| gfap-segmenter | 2026-01-08 | template | pypi description: template badge block |
| imaxt-multiscale-plugin | 2022-07-27 | template | pypi description: template README footer |
| in-silico-fate-mapping | 2023-02-27 | template | README template badge block |
| microglia-analyzer | 2026-05-11 | template | .napari-hub/ + test_and_deploy.yml |
| mitoclass | 2025-07-30 | template | .napari-hub/ + test_and_deploy.yml |
| motile-plugin | 2024-05-23 | template | none; pypi description: template badge block |
| napari-3d-label-eraser | 2025-12-09 | template | pypi description: template badge block |
| napari-ISM | 2022-05-26 | template | none; pypi description: template README footer |
| napari-LF | 2022-07-21 | template | README template badge block |
| napari-PICASSO | 2022-06-01 | template | README template badge block |
| napari-annotation-project | 2023-11-01 | template | README template badge block |
| napari-argos-archive-reader | 2024-01-03 | template | README template badge block |
| napari-assistant | 2022-03-05 | template | README template badge block |
| napari-bee-annotator | 2024-01-09 | template | README template badge block |
| napari-biopb | 2025-02-02 | template | none; pypi description: template badge block |
| napari-blender-bridge | 2023-04-07 | template | README template badge block |
| napari-caphid | 2023-07-30 | template | README template badge block |
| napari-clusters-plotter | 2021-11-15 | template | README template badge block |
| napari-convpaint | 2023-11-01 | template | none; pypi description: template README footer |
| napari-correct-drift | 2023-04-26 | template | README template badge block |
| napari-ctc-io | 2024-06-04 | template | README template badge block |
| napari-denoiseg | 2022-10-31 | template | README template badge block |
| napari-elementary-numpy-operations | 2022-01-12 | template | none; pypi description: template README footer |
| napari-feature-classifier | 2022-02-12 | template | README template badge block |
| napari-feature-visualization | 2024-07-25 | template | README template badge block |
| napari-flim-phasor-plotter | 2023-08-17 | template | README template badge block |
| napari-geojson | 2021-12-27 | template | README template badge block |
| napari-grid-curator | 2026-03-03 | template | none; pypi description: template README footer |
| napari-griottes | 2023-03-09 | template | README template badge block |
| napari-imagegrains | 2025-06-26 | template | README template badge block |
| napari-imagej | 2023-05-24 | template | none; pypi description: template badge block |
| napari-intensity-plotter | 2024-10-20 | template | README template badge block |
| napari-isbem | 2026-06-09 | template | README template badge block |
| napari-isolate-cell | 2025-08-06 | template | .napari-hub/ + test_and_deploy.yml |
| napari-itk-io | 2021-04-28 | template | none; pypi description: template README footer |
| napari-mAIcrobe | 2025-08-01 | template | .napari-hub/ + test_and_deploy.yml |
| napari-manual-transforms | 2022-04-28 | template | none; pypi description: template README footer |
| napari-matplotlib | 2022-05-02 | template | README template badge block |
| napari-medical-image-formats | 2021-04-24 | template | none; pypi description: template README footer |
| napari-melt-pool-tracker | 2023-11-02 | template | README template badge block |
| napari-metadata | 2026-01-20 | template | README template badge block |
| napari-mlarray | 2026-01-30 | template | pypi description: template badge block |
| napari-molseeq | 2024-07-25 | template | none; pypi description: template README footer |
| napari-morphodynamics | 2023-11-08 | template | README template badge block |
| napari-n2v | 2022-10-24 | template | README template badge block |
| napari-nd-cropper | 2022-01-12 | template | none; pypi description: template README footer |
| napari-nlm | 2022-07-25 | template | README template badge block |
| napari-ome-zarr-navigator | 2024-07-19 | template | .napari-hub/ + test_and_deploy.yml |
| napari-open-ctc | 2024-06-03 | template | README template badge block |
| napari-owncloud | 2022-11-16 | template | README template badge block |
| napari-phasors | 2024-11-22 | template | README template badge block |
| napari-piscis | 2025-11-28 | template | pypi description: template badge block |
| napari-prism | 2024-11-14 | template | README template badge block |
| napari-process-points-and-surfaces | 2022-02-05 | template | README template badge block |
| napari-pyclesperanto-assistant | 2020-12-19 | template | README template badge block |
| napari-sam | 2023-04-06 | template | README template badge block |
| napari-samv2 | 2024-10-08 | template | .napari-hub/ + test_and_deploy.yml |
| napari-sediment | 2024-09-23 | template | README template badge block |
| napari-segment | 2022-10-05 | template | README template badge block |
| napari-serialcellpose | 2022-07-28 | template | README template badge block |
| napari-signal-selector | 2023-10-17 | template | README template badge block |
| napari-simple-orthoviewer | 2024-10-08 | template | .napari-hub/ + test_and_deploy.yml |
| napari-simpleitk-image-processing | 2021-11-28 | template | README template badge block |
| napari-spam | 2026-05-08 | template | pypi description: template README footer |
| napari-spatialdata | 2022-07-06 | template | README template badge block |
| napari-steinpose | 2022-11-17 | template | README template badge block |
| napari-stitcher | 2024-10-18 | template | README template badge block |
| napari-storm | 2026-08-25 | template | none; pypi description: template README footer |
| napari-stress | 2022-06-02 | template | README template badge block |
| napari-subboxer | 2021-11-22 | template | none; pypi description: template README footer |
| napari-tiledb-bioimg | 2023-05-12 | template | .napari-hub/ + test_and_deploy.yml |
| napari-tissuumaps | 2021-09-02 | template | pypi description: template badge block |
| napari-tmidas | 2025-03-05 | template | .napari-hub/ + test_and_deploy.yml |
| napari-tomotwin | 2023-03-24 | template | .napari-hub/ + test_and_deploy.yml |
| napari-tracing | 2023-04-23 | template | README template badge block |
| napari-trackastra | 2024-05-30 | template | README template badge block |
| napari-trackpy | 2023-11-07 | template | .napari-hub/ + test_and_deploy.yml |
| napari-vascilia | 2024-06-28 | template | .napari-hub/ + test_and_deploy.yml |
| napari-vemseg | 2023-03-14 | template | pypi description: template badge block |
| napari-workflow-inspector | 2021-12-04 | template | README template badge block |
| napari-wsireg | 2022-04-27 | template | none; pypi description: template README footer |
| napari-xgboost | 2024-07-05 | template | README template badge block |
| napari-zulip | 2023-04-22 | template | README template badge block |
| ndev-sampledata | 2025-07-05 | template | .napari-hub/ + test_and_deploy.yml |
| ndevio | 2025-10-14 | template | README template badge block |
| ome-zarrpari | 2026-03-11 | template | README template badge block |
| orchardseg | 2025-09-10 | template | README template badge block |
| organelle-segmenter-plugin | 2023-05-13 | template | README template badge block |
| quantpunc | 2025-07-30 | template | .napari-hub/ + test_and_deploy.yml |
| the-segmentation-game | 2022-05-27 | template | README template badge block |
| tootapari | 2023-07-03 | template | README template badge block |
| vessel-express-napari | 2022-05-17 | template | README template badge block |
| vessqc | 2025-02-18 | template | README template badge block |
| vollseg-napari | 2021-12-10 | template | README template badge block |
| waver | 2021-05-15 | template | none; pypi description: template README footer |
| frontvegV2 | 2026-08-09 | unavailable | nan |
| misic-napari | 2021-12-07 | unavailable | nan |
| napari-bacteria-density | 2026-03-04 | unavailable | nan |
| napari-data-preview | 2023-02-17 | unavailable | nan |
| napari-fungiform | 2026-05-14 | unavailable | nan |
| napari-nifti-viewer | 2025-06-28 | unavailable | nan |
| napari-serverkit | 2025-01-07 | unavailable | nan |
| pentachrome-plugin | 2026-06-26 | unavailable | nan |
