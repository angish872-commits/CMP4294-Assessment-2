# CMP4294 Assessment 2: Customer Segmentation in E-Commerce Using K-Means Clustering

**Module:** CMP4294 Introduction to Artificial Intelligence  
**Assessment:** Assessment 2  
**Student:** Angish Sapkota (26152255)  
**Project title:** Customer Segmentation in E-Commerce Using Purchasing Behaviour and K-Means Clustering

## FINAL SUBMISSION FILES

1. `Angish_Sapkota_26152255.pdf`
2. `Angish_Sapkota_26152255.zip`

The ZIP contains exactly these two files:

- `Angish_Sapkota_26152255.ipynb`
- `ecommerce_2000.csv`

The PDF itself follows the brief's anonymous-marking instruction and contains the **student number only**. The full-name filename follows the working submission naming convention.

Final automated QA: **61/61 checks PASS**. See `report/FINAL_SUBMISSION_QA.md`.

## Research question

Can K-Means clustering identify meaningful customer groups from e-commerce purchasing behaviour so
that the retailer can better understand high-value, regular, occasional and low-engagement customers?

## Technique

One main technique: **K-Means clustering** (a descriptive machine-learning task).

## Dataset

- Source: Kaggle "Online Retail Business" (`umerkk12/online-retail-business`), file `OnlineRetail.csv`.
- The actual file is the full UCI Online Retail dataset: **541,909 rows x 8 columns**.
- Final project dataset `data/ecommerce_2000.csv`: **exactly 2,000 transaction rows x 8 columns**,
  141 unique customers.
- The brief requires at least 200 rows and 4 attributes; 2,000 rows is the chosen project scope,
  not an imposed maximum.
- Generated reproducibly by `data/make_ecommerce_2000.py` (seed 42, customer-aware) and verified
  by identical SHA-256 before and after regeneration.

## Results at a glance

- Cleaned rows: 1,814; unique customers: 141.
- Selected K = 4: highest silhouette score (0.4714), supported by the inertia elbow and interpretability.
- Robustness across 20 initialisations: identical segmentation (mean ARI = 1.0).
- Cluster sizes: 11, 60, 40, 30.
- Full verified results: `results_summary.md`.

## Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/angish872-commits/CMP4294-Assessment-2/blob/main/Angish_Sapkota_26152255.ipynb)

`Angish_Sapkota_26152255.ipynb` executes from first cell to last with no errors. The same notebook runs from the submitted ZIP, a GitHub checkout, or Google Colab (the dataset is located automatically).

### Run in Google Colab

Open the notebook directly in Google Colab:

https://colab.research.google.com/github/angish872-commits/CMP4294-Assessment-2/blob/main/Angish_Sapkota_26152255.ipynb

1. Choose **Runtime -> Run all**.
2. The notebook locates `ecommerce_2000.csv` automatically: it uses the CSV beside the notebook, or `data/ecommerce_2000.csv` in a GitHub/Colab checkout, or downloads the exact verified CSV from this repository.
3. Standard libraries only; no Kaggle credentials, Google Drive mount, or absolute paths are required.

## Final report QA

The final report is built from `report/Angish_Sapkota_26152255.tex`. The reproducible build:

- compiles the report with XeLaTeX;
- renders every final PDF page to PNG for visual inspection;
- checks required sections, captions, tables and references;
- checks anonymous PDF content;
- verifies the 2,000 x 8 dataset;
- verifies the exact ZIP contents.

The final PDF contains:
- 22 pages;
- approximately 1,995 main-body words, excluding Python code listings and figures;
- 105-word abstract;
- 7 figures;
- 6 tables;
- 10 verified references;
- 7 code excerpts taken from the submitted notebook;
- direct Google Colab and GitHub reproducibility links.

## Repository structure

```text
CMP4294-Assessment-2/
├── Angish_Sapkota_26152255.pdf      # final report
├── Angish_Sapkota_26152255.zip      # final submission ZIP
├── Angish_Sapkota_26152255.ipynb    # executed analysis notebook
├── data/
│   ├── source/OnlineRetail.csv
│   ├── make_ecommerce_2000.py
│   └── ecommerce_2000.csv
├── figures/                          # notebook-generated figures
├── references/sources.md             # verified source record
├── report/
│   ├── Angish_Sapkota_26152255.tex   # canonical final report source
│   ├── FINAL_SUBMISSION_QA.md
│   ├── qa/                            # rendered final PDF pages
│   ├── build_report.sh
│   └── verify_submission.py
├── report_evidence.md
├── report_plan.md
├── results_summary.md
└── README.md
```

## Status

**Submission package built and verified.** Before Moodle submission, the student should read the final PDF once and confirm the current Moodle filename/cover-sheet instructions. The polished anonymous report variant is maintained on the `final-report-polish` branch so the verified main-branch version remains untouched.

