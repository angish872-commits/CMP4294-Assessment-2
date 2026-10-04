# Report Evidence Check — CMP4294 Assessment 2

Every number in report/report_final.md was checked against the executed notebook Angish_Sapkota_26152255.ipynb and results_summary.md.
(`Angish_Sakupkota_26152255.ipynb` -> corrected to `Angish_Sapkota_26152255.ipynb`) and `results_summary.md`.
Executed notebook is the preferred source of truth. No number was invented.

| # | Report statement | Value in report | Source of truth | Status |
|---|------------------|-----------------|-----------------|--------|
| 1 | Source dataset size | 541,909 rows x 8 columns | results_summary.md (Dataset); dataset validation | PASS |
| 2 | Project dataset size | 2,000 rows x 8 columns | notebook section 2 and 4 outputs | PASS |
| 3 | Unique customers | 141 | notebook section 2 and 4 outputs | PASS |
| 4 | Customers with 2+ rows | 139 | notebook section 4 output; results_summary.md | PASS |
| 5 | Cleaned rows | 1,814 | notebook section 5 output | PASS |
| 6 | Cancelled invoices removed | 185 | notebook section 5 output | PASS |
| 7 | Invalid price rows removed | 1 | notebook section 5 output | PASS |
| 8 | Duplicate rows | 0 | notebook section 5 output | PASS |
| 9 | Reference (snapshot) date | 9 December 2011 | notebook section 8 output (2011-12-09) | PASS |
| 10 | Inertia and silhouette by K | table 2 values | notebook section 10 output | PASS |
| 11 | K = 4 silhouette | 0.4714 | notebook section 10 and 11 output | PASS |
| 12 | Robustness silhouette min/mean/max | 0.4714 | notebook robustness cell output | PASS |
| 13 | Robustness mean ARI | 1.0 | notebook robustness cell output | PASS |
| 14 | Cluster 0 profile | 11 / 26.55 / 8.45 / 1811.52 | notebook section 12 output | PASS |
| 15 | Cluster 2 profile | 40 / 24.02 / 7.92 / 415.52 | notebook section 12 output | PASS |
| 16 | Cluster 1 profile | 60 / 38.98 / 2.87 / 187.98 | notebook section 12 output | PASS |
| 17 | Cluster 3 profile | 30 / 223.73 / 1.80 / 126.28 | notebook section 12 output | PASS |
| 18 | Sampling caps (3 lines/order, 10 orders/customer, >30 excluded) | as stated | data/make_ecommerce_2000.py | PASS |

Result: 18 of 18 checks PASS. No FAIL items to fix.
