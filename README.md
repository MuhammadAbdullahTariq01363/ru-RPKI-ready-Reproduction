# ru-RPKI-ready: the Road Left to Full ROA Adoption — Reproduction

This repository contains a reproduction of selected results from the paper
**"ru-RPKI-ready: the Road Left to Full ROA Adoption"**, published at the
ACM Internet Measurement Conference (IMC 2025) by Deepak Gouda, Romain
Fontugne, and Cecilia Testart.

- Paper: https://dl.acm.org/doi/10.1145/3730567.3764452
- Original dataset repo: https://github.com/ISS-GT/ru-RPKI-ready
- Original code repo: https://github.com/ISS-GT/ru-RPKI-ready-Code

This was done as a course reproduction project for the Networking Research
Reproduction Assignment (Computer Networks course).

## What was reproduced

Three of the paper's main claims were reproduced using the public dataset:

1. **Overall IPv4 vs IPv6 ROA coverage**
2. **RIR-wise IPv4 ROA coverage breakdown**
3. **Low-Hanging Fruit analysis** (prefixes that could be covered by ROAs with minimal effort)

The full write-up, methodology, and comparison against the original paper's
numbers are in [`report/ru-RPKI-ready_Reproduction_Report.pdf`](report/ru-RPKI-ready_Reproduction_Report.pdf).

## Repository structure

```
data/       Dataset snapshot used for the reproduction (April 1, 2025)
scripts/    Scripts used to reproduce each claim
output/     Generated figures from running the scripts
report/     Final report (PDF)
```

## Data

- `data/prefix_tags_2025-04-01_v4.parquet` — IPv4 prefix tags snapshot
- `data/prefix_tags_2025-04-01_v6.parquet` — IPv6 prefix tags snapshot

## Scripts

- `scripts/script1_rir_coverage.py` — Overall coverage and RIR-wise IPv4 coverage
- `scripts/script2_low_hanging.py` — Low-Hanging Fruit analysis
- `scripts/script3_adoption_stages.py` — Rogers Adoption Stage breakdown

Each script reads the parquet files from `../data/` and produces a figure
in `output/`.

## Output

- `output/figure1_rir_coverage.png`
- `output/figure2_overall_coverage.png`
- `output/figure3_low_hanging.png`
- `output/figure4_adoption_stages.png`

## Reproduction by

M Abdullah Tariq
