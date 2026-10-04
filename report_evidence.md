# Report Evidence Pack — CMP4294 Assessment 2

This is NOT the final report. It is a verified evidence pack for writing the report.
Every numeric statement cites the notebook section or output it came from. No value is invented.

Notebook: `Angish_Sapkota_26152255.ipynb` (37 cells, executed clean, 0 errors).
Dataset: `data/ecommerce_2000.csv`. Generator: `data/make_ecommerce_2000.py`.

---

## A. Domain
E-commerce / online retail (customer analytics).

## B. Problem definition
Raw transaction data does not directly reveal meaningful groups of customers based on purchasing
behaviour. The knowledge-discovery question is: can K-Means clustering identify meaningful customer
groups from e-commerce purchasing behaviour so that the retailer can better understand high-value,
regular, occasional and low-engagement customers? (Source: project problem definition, README.)

## C. Why the problem matters
Retailers hold transaction records but often cannot tell which customers behave alike. Grouping
customers by measured behaviour supports targeting and retention decisions. This is a descriptive
task: it describes structure in the data and does not test interventions.

## D. Dataset source
Kaggle "Online Retail Business" (`umerkk12/online-retail-business`), file `OnlineRetail.csv`. This file
is a copy of the UCI Online Retail dataset (ID 352). (Source: README; references/sources.md.)

## E. Source dataset dimensions
- 541,909 rows x 8 columns.
- Rows with a CustomerID: 406,829 (the remainder have no customer key).
- Unique customers: 4,372; 4,293 with 2+ transactions.
Provenance: results_summary.md (Dataset); generator output line SOURCE_ROWS 406829; dataset-validation run.

## F. Project dataset dimensions
- `data/ecommerce_2000.csv`: exactly 2,000 rows x 8 columns.
- Unique customers: 141; 139 with two or more rows.
- SHA-256 verified identical before and after regeneration
  (`a310977b2f64afadbaafd2f2e6d93be1acca052eafc6ea16fc244ce89e644c53`).
Provenance: notebook section 2 and section 4 outputs; results_summary.md.

## G. Dataset attributes
InvoiceNo (order id; C-prefix = cancellation), StockCode, Description, Quantity, InvoiceDate,
UnitPrice, CustomerID, Country. (Source: notebook section 3 output.)

## H. Sampling method
Customer-aware, deterministic subset built by `data/make_ecommerce_2000.py`:
- customers grouped into order-frequency bands (1-2, 3-4, 5-9, 10-30 orders);
- sampled round-robin across bands with seed 42;
- LINE_CAP = 3 line items kept per order; INV_CAP = 10 orders kept per customer;
- customers with more than 30 source orders excluded.
Chosen to preserve repeated customer histories within a 2,000-row scope. 2,000 rows is our chosen
project scope (the brief requires at least 200 rows and 4 attributes).

## I. Sampling limitations
- Naive random sampling would leave most customers with a single row, making RFM impossible.
- LINE_CAP = 3 truncates large orders, so Monetary understates true customer spend.
- INV_CAP = 10 and excluding 30+ order customers compress the Frequency upper tail.
- Monetary upper tail is compressed because fewer line items per order are counted.
- The sample is representative in structure but small (141 customers), so clusters cannot be
  generalised automatically to the full retailer population.

## J. Cleaning decisions and counts
Starting from 2,000 rows (notebook section 5 output):
- cancelled invoices removed: 185 (2,000 to 1,815);
- invalid non-positive quantity or price removed: 1 (1,815 to 1,814);
- duplicate rows removed: 0;
- missing CustomerID in the subset: 0 (such rows were excluded during sampling);
- final cleaned rows: 1,814; unique customers: 141.

## K. RFM definitions
Per CustomerID, with snapshot date 2011-12-09 (one day after the last transaction):
- Recency = days from the customer most recent purchase to the snapshot date;
- Frequency = number of distinct invoices (orders);
- Monetary = sum of TotalPrice, where TotalPrice = Quantity x UnitPrice.
(Source: notebook section 8; snapshot printed as 2011-12-09.)

## L. Descriptive statistics (141 customers; notebook section 8 output)
- Recency (days): mean 73.08, median 33, min 1, max 366.
- Frequency (orders): mean 4.51, median 4, min 1, max 10.
- Monetary (GBP): mean 366.06, median 215.55, min 15.20, max 3089.42.

## M. Why scaling was required
Recency (days), Frequency (orders) and Monetary (GBP) differ in magnitude. In Euclidean distance,
Monetary would dominate and the segments would mainly reflect spend. StandardScaler standardises each
feature to mean 0 and standard deviation 1. (Source: notebook section 9.)

---

## N. K values tested
K = 2, 3, 4, 5, 6, 7, 8 (notebook section 10).

## O. Complete inertia table (notebook section 10 output)
| K | Inertia |
|---|---------|
| 2 | 247.11 |
| 3 | 157.79 |
| 4 | 91.01 |
| 5 | 73.21 |
| 6 | 56.88 |
| 7 | 43.30 |
| 8 | 38.53 |

## P. Complete silhouette table (notebook section 10 output)
| K | Silhouette |
|---|------------|
| 2 | 0.4103 |
| 3 | 0.4329 |
| 4 | 0.4714 |
| 5 | 0.4625 |
| 6 | 0.4693 |
| 7 | 0.4270 |
| 8 | 0.3896 |

## Q. Robustness-test result (notebook robustness cell, computed)
K = 4 re-fitted for random_state 0 to 19 at n_init = 10:
- Silhouette min = 0.4714, mean = 0.4714, max = 0.4714;
- mean Adjusted Rand Index against the random_state = 42 solution = 1.0;
- number of distinct cluster-size signatures = 1 (always 11, 30, 40, 60).
Interpretation: for this dataset the K = 4 solution is stable across initialisations.

## R. Why K = 4 was selected (notebook section 11)
- Highest silhouette score (0.4714) among K = 2 to 8;
- inertia elbow flattens after K = 4;
- four segments remain interpretable in business terms;
- the robustness check shows the solution does not depend on initialisation.
Caveat: silhouette for K = 4, 5 and 6 is close, so K is a modelling choice.

## S. Cluster profile table (notebook section 12 output, K = 4)

| Cluster | Customers | Recency mean | Recency median | Frequency mean | Frequency median | Monetary mean | Monetary median |
|---------|-----------|--------------|----------------|----------------|------------------|---------------|-----------------|
| 0 | 11 | 26.55 | 21.0 | 8.45 | 9.0 | 1811.52 | 1577.24 |
| 1 | 60 | 38.98 | 31.0 | 2.87 | 3.0 | 187.98 | 159.37 |
| 2 | 40 | 24.02 | 17.0 | 7.92 | 8.0 | 415.52 | 371.08 |
| 3 | 30 | 223.73 | 193.0 | 1.80 | 1.0 | 126.28 | 86.43 |

## T. Cluster interpretations (from the computed profile; notebook section 14)
Cluster numeric IDs are arbitrary. Labels are interpretations of the statistics, not ground truth:
- Cluster 0 (11 customers): high-value loyal. Recent, most frequent, highest spend.
- Cluster 2 (40 customers): frequent regular. Recent and frequent, moderate spend.
- Cluster 1 (60 customers): occasional. Reasonably recent, low frequency, low spend.
- Cluster 3 (30 customers): lapsed / low-engagement. Least recent, fewest orders, lowest spend.
No statement implies causation; the analysis measures association only.

## U. Business implications (evidence-linked, cautious)
- Cluster 0 contributes disproportionate spend from few customers: retention attention is
  justifiable on the observed monetary mean (1811.52) and frequency mean (8.45).
- Cluster 2 combines high frequency with moderate spend: there may be a basket-value opportunity,
  but the data does not test that any offer would succeed.
- Cluster 1 is numerous but low frequency and low spend: a frequency-building opportunity may exist.
- Cluster 3 is the least recent and lowest spend: reactivation could be investigated.
The data does not measure campaign effectiveness, so no action is claimed to work.

---

## V. Limitations
- Sampling: 2,000-row scope with LINE_CAP = 3 and INV_CAP = 10; 30+ order customers excluded;
  Frequency and Monetary upper tails compressed; 141 customers only.
- Monetary ignores product margin and cost.
- RFM ignores product mix, time between purchases and returns detail.
- K-Means assumes roughly spherical, comparable clusters; sensitive to K and scaling.
- Silhouette for K = 4, 5 and 6 is close; K choice is a modelling decision.
- Cluster names are interpretations; clustering shows similarity, not causation.
- Stability across initialisation was tested; stability across different samples was not.

## W. Recommendations (cautious, evidence-linked)
1. Retain the high-value loyal segment (Cluster 0): protect its recent, frequent, high-spend
   behaviour through retention attention. Evidence: Monetary mean 1811.52, Frequency mean 8.45.
2. Investigate basket value for the frequent regular segment (Cluster 2): it buys often but at
   lower spend per order. Evidence: Frequency mean 7.92, Monetary mean 415.52.
3. Investigate frequency for the occasional segment (Cluster 1): numerous customers with low order
   frequency. Evidence: 60 customers, Frequency mean 2.87, Monetary mean 187.98.
4. Investigate reactivation for the lapsed segment (Cluster 3): least recent and lowest spend.
   Evidence: Recency mean 223.73, Frequency mean 1.80, Monetary mean 126.28.
These are hypotheses grounded in observed segments; none is a tested intervention.

## X. Figure list (all regenerated by the notebook; verified present)
- `figures/01_missing_values.png` - missing values per column and data-quality issue counts.
- `figures/02_transaction_distribution.png` - TotalPrice distribution (log y-axis) with units GBP.
- `figures/03_rfm_distributions.png` - Recency, Frequency, Monetary histograms.
- `figures/04_elbow_method.png` - inertia against K.
- `figures/05_silhouette_scores.png` - silhouette against K.
- `figures/06_customer_clusters.png` - Frequency vs Monetary scatter by cluster (legend, GBP).
- `figures/07_cluster_profiles.png` - mean Recency, Frequency, Monetary by cluster.
Dimensions range from ~948x587 to ~1788x468; titles and axis labels present; 06 has a legend.

## Y. References to use (see references/sources.md)
- Kaggle dataset (umerkk12/online-retail-business).
- UCI Online Retail dataset (ID 352), Dua and Graff (2019).
- K-Means: MacQueen (1967); Lloyd (1982); scikit-learn KMeans documentation.
- Silhouette: Rousseeuw (1987); scikit-learn silhouette_score documentation.
- Scaling: scikit-learn StandardScaler documentation.
- RFM/segmentation: Hughes (1994); Fader, Hardie and Lee (2005); Wedel and Kamakura (2000).
- Library: Pedregosa et al. (2011).
Only references actually used in the report will be retained.

---

Note: all figures and values above are reproduced by executing the notebook; they were not
hard-coded. The notebook computes every statistic from `data/ecommerce_2000.csv`.
