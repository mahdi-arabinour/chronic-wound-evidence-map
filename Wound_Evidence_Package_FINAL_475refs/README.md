# Chronic-wound evidence-map reproducibility data

**Manuscript-matched release candidate: 475-reference bibliography, supplementary Tables S1–S5, Figures S1–S11.**

The companion package supports a *narrative, decision-oriented* review; it is not a systematic search, meta-analysis, clinical prediction benchmark, or independent validation of the original study-level classifications. Counts describe only the cited source cohorts. Codes (0/1) record whether a selected feature was documented in the authors’ curated extraction; a zero does not establish that a full paper lacks that feature.

## Rebuilding and verification

Install requirements in `requirements.txt`. Run `python verify_release.py` to check the reference-cohort joins, all matrix values, and spreadsheet's cross-check cell count. Run `python rebuild_all_11.py` to reconstruct all eleven PNG/SVG diagrams without network access.

The source reference register (`Current_Main_475_References.csv`) is matched by source title/bibliographic entry to the supplied final main document. Supplementary source membership (`Current_SI_Table_References.csv`) is re-extracted from the revised Supplementary Information. The per-figure `coding/` CSV files contain the selected study-level descriptors, `matrices/` contains output tallies, `figures/` the regenerated visualizations, and the workbook preserves coded inputs and formula-based checks. The Figure-number crosswalk maps the retained original figures onto sequential S1–S11 names.
