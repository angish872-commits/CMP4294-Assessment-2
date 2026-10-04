# CMP4294 Assessment 2: Customer Segmentation in E-Commerce Using K-Means Clustering

**Module:** CMP4294 Introduction to Artificial Intelligence
**Assessment:** Assessment 2
**Student:** Angish Sapkota (26152255)
**Project title:** Customer Segmentation in E-Commerce Using Purchasing Behaviour and K-Means Clustering

## Research question

Can K-Means clustering identify meaningful customer groups from e-commerce purchasing behaviour so
that the retailer can better understand high-value, regular, occasional and low-engagement customers?

## Technique

One main technique: **K-Means clustering** (a descriptive machine-learning task).

## Dataset

- Source: Kaggle "Online Retail Business" (`umerkk12/online-retail-business`), file `OnlineRetail.csv`.
- The Kaggle page states 6,000 rows, but the actual file is the full UCI Online Retail dataset:
  **541,909 rows x 8 columns**.
- Final project dataset `data/ecommerce_2000.csv`: **exactly 2,000 transaction rows x 8 columns**,
  141 unique customers. The brief requires at least 200 rows and 4 attributes; 2,000 rows is our
  chosen project scope, not an imposed maximum.
- Generated reproducibly by `data/make_ecommerce_2000.py` (seed 42, customer-aware). Verified by an
  identical SHA-256 before and after regeneration.

## Results at a glance

- Cleaned rows: 1,814. Unique customers: 141.
- Selected K = 4 (highest silhouette 0.4714, inertia elbow flattens, four interpretable segments).
- Cluster sizes: 11, 60, 40, 30.
- Full verified results: see `results_summary.md`.

## Notebook

`Angish_Sapkota_26152255.ipynb` runs from first cell to last with no errors.

### How to run in Google Colab

1. Open Google Colab and upload `Angish_Sapkota_26152255.ipynb`.
2. Upload `data/ecommerce_2000.csv` to the Colab session, keeping the relative path `data/ecommerce_2000.csv`.
3. Choose Runtime, then Run all. Standard Colab already provides pandas, numpy, matplotlib and scikit-learn.

No absolute local paths and no Kaggle credentials are required to run the analysis.

## Repository structure

```text
CMP4294-Assessment-2/
├── data/
│   ├── source/OnlineRetail.csv    # original source dataset
│   ├── make_ecommerce_2000.py     # reproducible subset generator (seed 42)
│   └── ecommerce_2000.csv         # final project dataset (exactly 2,000 rows)
├── figures/                       # 7 figures exported by the notebook
├── references/sources.md          # sources for later BCU Harvard referencing
├── Angish_Sapkota_26152255.ipynb  # analysis notebook
├── results_summary.md             # verified results
└── README.md
```

## Status

CODE + DATA phase complete. The PDF report is not written yet.
