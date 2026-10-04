# CMP4294 Assessment 2: Customer Segmentation in E-Commerce Using K-Means Clustering
Module: CMP4294 Introduction to Artificial Intelligence (Assessment 2). Student: Angish Sapkota (26152255).
Descriptive machine-learning task. One main technique: K-Means clustering.
Research question: Can K-Means clustering identify meaningful customer groups from e-commerce purchasing behaviour so that the retailer can better understand high-value, regular, occasional, and low-engagement customers?
Dataset source (exact): Kaggle Online Retail Business (umerkk12/online-retail-business), file OnlineRetail.csv, about 6000 rows and 8 columns (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country).
Project dataset: data/ecommerce_2000.csv, a reproducible customer-aware subset capped at exactly 2000 transaction rows (random_state=42). Method recorded in results_summary.md.
Note: the Notion project plan drafts mention about 2500 rows; the final project dataset uses 2000 rows to satisfy the assignment maximum of 2000 transaction rows.
Repo layout: data/source (original file if licence permits), data/ecommerce_2000.csv, figures, references/sources.md, Angish_Sapkota_26152255.ipynb, results_summary.md, README.md.
Run in Google Colab: upload the ipynb, keep data/ecommerce_2000.csv alongside it, Runtime Run-all. Standard Colab already provides pandas, numpy, matplotlib and scikit-learn. No absolute paths; random_state=42 everywhere.
Status: CODE plus DATA portion only; no PDF report yet.
