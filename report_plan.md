# Report Plan (Blueprint) — CMP4294 Assessment 2

This is a plan only. The full report is NOT written yet. Target: about 1,500 words of main prose,
within the official word-count rules. Evidence is drawn from `report_evidence.md` (verified outputs).

Word budget for main prose: 1,500 (plus cover page, tables of contents/figures, abstract and
references, which are normally excluded from the main word count).

---

## Front matter (not counted in main prose)

### Cover page
- Module, assessment, title, student name and ID, date, repository link.
- Evidence: README metadata.

### Table of Contents
- Auto-generated from headings.

### Table of Figures
- 7 figures (see report_evidence.md section X).

### Abstract (optional; ~120 words, usually excluded from word count)
- Evidence: project question, 2,000-row dataset, 141 customers, K = 4, silhouette 0.4714.
- Critical point: state that this is descriptive clustering, not prediction or causation.

---

## 1. Domain Description (~110 words)
- Evidence required: e-commerce/online retail; transaction-level data.
- Figure/table: none.
- References: none required (or a retail-analytics source if used).
- Critical point: distinguish descriptive analytics from prediction.

## 2. Problem Definition (~140 words)
- Evidence required: the research question and why raw transactions hide customer structure.
- Figure/table: none.
- References: customer segmentation framing (Wedel and Kamakura 2000).
- Critical point: define the task as descriptive machine learning with one technique.

## 3. Brief Literature Review (~220 words)
- Evidence required: K-Means origin and use; silhouette evaluation; RFM segmentation.
- Figure/table: none.
- References: MacQueen (1967), Lloyd (1982), Rousseeuw (1987), Hughes (1994), Fader et al. (2005).
- Critical point: note K-Means assumptions and the limits of RFM.

## 4. Dataset Description (~180 words)
- Evidence required: source (Kaggle mirror of UCI Online Retail), 541,909 x 8, 4,372 customers;
  project dataset 2,000 x 8, 141 customers, 139 repeat.
- Figure/table: Table 1 dataset attributes; figure 01.
- References: Kaggle; UCI (Dua and Graff 2019).
- Critical point: state clearly that 2,000 rows is a chosen scope, not a brief maximum.

## 5. Dataset Pre-processing (~230 words)
- Evidence required: sampling method (seed 42, bands, LINE_CAP=3, INV_CAP=10); cleaning counts
  (185 cancellations, 1 invalid, 0 duplicates; 1,814 rows; 141 customers); TotalPrice; scaling.
- Figure/table: Table 2 cleaning counts; figure 01; figure 02.
- References: scikit-learn StandardScaler.
- Critical point: explain the sampling bias and why naive random sampling fails for RFM.

## 6. Experiments — K-Means (~280 words)
- Evidence required: K = 2 to 8; inertia and silhouette tables; elbow and silhouette figures;
  robustness across 20 seeds; final K = 4 with random_state = 42 and n_init = 10.
- Figure/table: Table 3 inertia; Table 4 silhouette; figures 04, 05; Table 5 robustness.
- References: scikit-learn KMeans and silhouette_score.
- Critical point: K is selected from evidence; K = 4/5/6 are close, stated honestly.
  No accuracy metric is reported because this is clustering.

## 7. Analysis of Results and Conclusion (~340 words)
- Evidence required: cluster profile table; segment interpretations; robustness; limitations;
  cautious recommendations.
- Figure/table: Table 6 cluster profiles; Table 7 recommendations; figures 06, 07.
- References: as used above.
- Critical point: cluster IDs are arbitrary, names are interpretations, and clustering shows
  similarity not causation; segments do not automatically generalise beyond the sample.

## References — BCU Harvard (not counted)
- Final list drawn only from sources actually used; see references/sources.md.
- Verify every item; fabricate nothing.

---

## Totals
- Main prose: about 1,500 words across sections 1 to 7.
- Figures: 7. Tables: about 7. Verify final word count against the official brief before submission.
