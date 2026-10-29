# Chronic-wound evidence-map reproducibility data

**Manuscript-matched release candidate: 475-reference bibliography, supplementary Tables S1–S5, Figures S1–S11.**

The companion package supports a *narrative, decision-oriented* review; it is not a systematic search, meta-analysis, clinical prediction benchmark, or independent validation of the original study-level classifications. Counts describe only the cited source cohorts. Codes (0/1) record whether a selected feature was documented in the authors’ curated extraction; a zero does not establish that a full paper lacks that feature.

## Rebuilding and verification

Install requirements in `requirements.txt`. Run `python verify_release.py` to check the reference-cohort joins, all matrix values, and spreadsheet's cross-check cell count. Run `python rebuild_all_11.py` to reconstruct all eleven PNG/SVG diagrams without network access.

The source reference register (`Current_Main_475_References.csv`) is matched by source title/bibliographic entry to the supplied final main document. Supplementary source membership (`Current_SI_Table_References.csv`) is re-extracted from the revised Supplementary Information. The per-figure `coding/` CSV files contain the selected study-level descriptors, `matrices/` contains output tallies, `figures/` the regenerated visualizations, and the workbook preserves coded inputs and formula-based checks. The Figure-number crosswalk maps the retained original figures onto sequential S1–S11 names.

## Explicit source-set changes

The latest main bibliography has 475 records, not the earlier 477. In Figure S8–S9's source cohort, the earlier unpublished diabetic-foot-ulcer tissue-segmentation preprint (original ref 279) is no longer in the cited table; the retained published WSNet conference paper maps from original 282 to current 284. The Figure S10–S11 source cohort excludes the earlier WEABM preprint (original ref 404) and three earlier DFU-derived disease-model sources (original refs 371, 372, 376) that are not cited in the *current* Supplementary Table S5. Their prior coded rows have not been reassigned to unrelated papers. Cohort sizes are: S1 28, S2 20, S3 41, S4 45, S5 34 (S6 mechanism-defined subset 37). All other selected categories remain the author's original coded assessments.

The original three proposed ordinal/hypothetical figures (former S3, S11 and S13) remain excluded because the earlier scoring could not support comparative claims. No previously removed plot has been reintroduced.

Reproducibility means code/matrix agreement, not original-study full-text adjudication, causal evidence, clinical utility or regulatory qualification. Authors should perform the final scientific sign-off and select a license before public deposition. No repository URL or DOI is asserted by this package.
