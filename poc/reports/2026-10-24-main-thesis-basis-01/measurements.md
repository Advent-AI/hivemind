# Basis experiment measurements

Structural validity and observed usage; not semantic accuracy.

| Phase | Attempted | Valid | Mean input tokens | Estimated USD |
|---|---:|---:|---:|---:|
| review | 18 | 18 | 10638.5 | 0.624706 |
| basis_final | 6 | 6 | 10103.166666666666 | 0.130033 |
| direct_final | 6 | 6 | 10746 | 0.142735 |
| basis_probe | 6 | 6 | 10949.333333333334 | 0.110280 |
| direct_probe | 6 | 6 | 3489.3333333333335 | 0.052100 |

Judged source instances: 822. Total estimated USD: 1.059854.

The final-round comparison includes latest-source review + summary + reader for basis, and summary + reader for direct. Earlier historical source reviews are excluded from that comparison.

```json
[
  {
    "sample": 1,
    "scope": "rubin",
    "arm": "basis",
    "estimated_usd": 0.08164199999999999
  },
  {
    "sample": 1,
    "scope": "rubin",
    "arm": "direct",
    "estimated_usd": 0.02997
  },
  {
    "sample": 1,
    "scope": "capex",
    "arm": "basis",
    "estimated_usd": 0.084762
  },
  {
    "sample": 1,
    "scope": "capex",
    "arm": "direct",
    "estimated_usd": 0.035324
  },
  {
    "sample": 2,
    "scope": "rubin",
    "arm": "basis",
    "estimated_usd": 0.08080999999999999
  },
  {
    "sample": 2,
    "scope": "rubin",
    "arm": "direct",
    "estimated_usd": 0.0313
  },
  {
    "sample": 2,
    "scope": "capex",
    "arm": "basis",
    "estimated_usd": 0.080175
  },
  {
    "sample": 2,
    "scope": "capex",
    "arm": "direct",
    "estimated_usd": 0.033742
  },
  {
    "sample": 3,
    "scope": "rubin",
    "arm": "basis",
    "estimated_usd": 0.084116
  },
  {
    "sample": 3,
    "scope": "rubin",
    "arm": "direct",
    "estimated_usd": 0.029116
  },
  {
    "sample": 3,
    "scope": "capex",
    "arm": "basis",
    "estimated_usd": 0.079916
  },
  {
    "sample": 3,
    "scope": "capex",
    "arm": "direct",
    "estimated_usd": 0.035383
  }
]
```
