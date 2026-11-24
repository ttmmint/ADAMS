# ADAMS Assignment 2: A walk through the multiverse

Does the number of statistics credits predict how well people detect mistakes
in science news? This repository contains the single-pathway analyses
(Parts A and B) and a multiverse analysis of 72 pathways (Parts C and D).

## Files

| File | Description |
|---|---|
| `ADAMS_Assignment2.pdf` | Assignment description |
| `A1_data.csv` | Dataset for Part A |
| `A2_data.csv` | Dataset for Part B, the same as it in `A1_data.csv`.|
| `a2.Rmd` | All analyses: Part A, Part B and the multiverse |
| `a2.html` | Knitted output of `a2.Rmd` |
| `multiverse_results.csv` | Results of the 72 pathways, written by `a2.Rmd` |
| `multiverse_fig.py` | Draws the pathway diagrams from `multiverse_results.csv` |
| `figures/` | Figures used in the report |
| `report/` | Reports for each phase

## Run

1. Open `a2.Rmd` in RStudio and knit it (or run all chunks).
   This writes `multiverse_results.csv` and the specification curve.
2. Run the figure script from this folder:

   ```
   python multiverse_fig.py
   ```

   This creates `multiverse_lattice.png` and `multiverse_full_tree.png`.

## Requirements

- **R**: `ggplot2`, `patchwork`, `knitr`, `rmarkdown`
- **Python**: `matplotlib`, `pandas`

## The multiverse

| Decision | Options |
|---|---|
| D1 Goal guessers | Keep / Exclude (n = 13) |
| D2 Stats grade | Keep all / Exclude < 5.5 (n = 25) / Exclude < 6.0 (n = 54) |
| D3 Comprehension | Keep all / Exclude ≤ 7 (n = 4) / Exclude ≤ 10 (n = 37) / Covariate |
| D4 Control variables | None / ReadNews / ReadNews + Sexe |

2 × 3 × 4 × 3 = 72 pathways. Each pathway regresses `Judgment` on
`StatsCourses` with OLS.