from __future__ import annotations

import json
import re
import statistics
import zipfile
from pathlib import Path

import fitz
import pandas as pd
from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report"
BASENAME = "Angish_Sapkota_26152255"
PDF = ROOT / f"{BASENAME}.pdf"
ZIP = ROOT / f"{BASENAME}.zip"
TEX = REPORT_DIR / f"{BASENAME}.tex"
QA_DIR = REPORT_DIR / "qa"
QA_MD = REPORT_DIR / "FINAL_SUBMISSION_QA.md"
NOTEBOOK = ROOT / f"{BASENAME}.ipynb"
DATASET = ROOT / "data" / "ecommerce_2000.csv"

checks: list[tuple[str, bool, str]] = []

def add(name: str, ok: bool, detail: str) -> None:
    checks.append((name, ok, detail))
    if not ok:
        raise AssertionError(f"{name}: {detail}")

add("Final PDF exists", PDF.exists(), str(PDF))
add("Final ZIP exists", ZIP.exists(), str(ZIP))
add("LaTeX source exists", TEX.exists(), str(TEX))

doc = fitz.open(PDF)
page_count = doc.page_count
add("PDF page count", 18 <= page_count <= 28, f"{page_count} pages")

page_text = [page.get_text("text") for page in doc]
all_text = "\n".join(page_text)
upper_text = all_text.upper()

add("Anonymous report content", "ANGISH SAPKOTA" not in upper_text, "Student name absent from PDF content")
add("Student number present", "26152255" in page_text[0], "Cover contains student number")
add("Module code present", ("CMP4294" in page_text[0] or "CMP 4294" in page_text[0]), "Cover contains CMP4294")
add("Cover has sample-style fields",
    all(x in page_text[0] for x in ["Student Name", "Student ID", "Module Leader"]),
    "Cover includes the same field structure as the supplied sample while preserving anonymity")

required = [
    "Domain Description",
    "Problem Definition",
    "Literature Review",
    "Dataset Description",
    "Data Pre-Processing",
    "Descriptive Analysis Techniques",
    "Experiments",
    "Analysis of Results and Conclusion",
    "References",
]
add("Required sections present", all(h in all_text for h in required), "All required/sample-aligned sections found")
add("Contents page present", "Contents" in page_text[1], "Page 2")
add("Table of Figures present", "Table of Figures" in page_text[2], "Page 3")
add("Acknowledgement present", "Acknowledgement" in all_text, "Front matter includes acknowledgement")
add("Colab access present", "colab.research.google.com" in all_text, "Clickable Colab notebook URL is present")
add("CSV evidence present", "VINTAGE DOILY TRAVEL SEWING KIT" in all_text, "Report includes actual CSV preview rows")

for caption in [
    "Data-quality issues in the 2,000-row project dataset",
    "Distribution of cleaned transaction value",
    "RFM distributions for the 141 customers",
    "Elbow method: inertia against the number of clusters",
    "Silhouette score against the number of clusters",
    "Customer clusters: Frequency versus Monetary value",
    "Mean Recency, Frequency and Monetary value by cluster",
]:
    add(f"Figure caption: {caption[:30]}", caption in all_text, caption)

for caption in [
    "Dataset characteristics",
    "Feature descriptions",
    "RFM descriptive statistics",
    "Evaluation of candidate values of K",
    "Cluster profiles for the final K-Means model",
]:
    add(f"Table caption: {caption[:30]}", caption in all_text, caption)

for snippet in [
    'pd.read_csv',
    'StandardScaler',
    'KMeans',
    'final_k',
    'groupby',
]:
    add(f"Code evidence: {snippet[:25]}", snippet in all_text, snippet)

add("No replacement glyphs", "\ufffd" not in all_text, "No Unicode replacement characters found")

qa_pages = sorted(QA_DIR.glob("page-*.png"))
add("Rendered QA page count", len(qa_pages) == page_count, f"{len(qa_pages)} rendered PNGs")

means = []
black_ratios = []
for p in qa_pages:
    im = Image.open(p).convert("L")
    stat = ImageStat.Stat(im)
    mean = stat.mean[0]
    hist = im.histogram()
    blackish = sum(hist[:40]) / (im.width * im.height)
    means.append(mean)
    black_ratios.append(blackish)
    add(
        f"Visual sanity {p.name}",
        im.width >= 900 and im.height >= 1200 and mean > 150 and blackish < 0.30,
        f"{im.width}x{im.height}, mean={mean:.1f}, black_ratio={blackish:.4f}",
    )

with zipfile.ZipFile(ZIP) as zf:
    names = sorted(zf.namelist())
expected_zip = sorted([f"{BASENAME}.ipynb", "ecommerce_2000.csv"])
add("ZIP contents exact", names == expected_zip, f"{names}")

df = pd.read_csv(DATASET)
add("Dataset dimensions", df.shape == (2000, 8), f"{df.shape[0]} rows x {df.shape[1]} columns")

nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
cells = nb.get("cells", [])
code_cells = [c for c in cells if c.get("cell_type") == "code"]
add("Notebook structure", len(cells) >= 35 and len(code_cells) >= 17, f"{len(cells)} cells; {len(code_cells)} code")

tex = TEX.read_text(encoding="utf-8")
body_start = tex.index(r"\section{Domain Description}")
body_end = tex.index(r"\section*{References}")
body = tex[body_start:body_end]
body = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", " ", body, flags=re.S)
body = re.sub(r"\\begin\{lstlisting\}.*?\\end\{lstlisting\}", " ", body, flags=re.S)
body_clean = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", body)
body_clean = re.sub(r"[{}$~^&#_\\]", " ", body_clean)
main_words = re.findall(r"\b[\w£–-]+(?:['’][\w]+)?\b", body_clean)
add("Main-body word-count range", 1450 <= len(main_words) <= 2100, f"approx. {len(main_words)} words excluding code listings/figures")

abstract_match = re.search(
    r"\\section\*\{Abstract\}.*?\\addcontentsline\{toc\}\{section\}\{Abstract\}(.*?)\\clearpage",
    tex,
    flags=re.S,
)
abstract_text = abstract_match.group(1) if abstract_match else ""
abstract_clean = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", abstract_text)
abstract_clean = re.sub(r"[{}$~^&#_\\]", " ", abstract_clean)
abstract_words = re.findall(r"\b[\w–-]+(?:['’][\w]+)?\b", abstract_clean)
add("Abstract word-count range", 90 <= len(abstract_words) <= 150, f"{len(abstract_words)} words")

reference_order = [
    "Chen, D. (2015)",
    "Chen, D., Sain, S.L. and Guo, K. (2012)",
    "Fader, P.S.",
    "Hughes, A.M.",
    "Kaggle (2021)",
    "Lloyd, S.P.",
    "MacQueen, J.",
    "Pedregosa, F.",
    "Rousseeuw, P.J.",
    "Wedel, M.",
]
positions = [all_text.find(x) for x in reference_order]
add("References alphabetical", all(p >= 0 for p in positions) and positions == sorted(positions),
    "Reference entries found in expected alphabetical order")

passed = sum(ok for _, ok, _ in checks)
lines = [
    "# Final Submission QA",
    "",
    f"**Overall:** PASS ({passed}/{len(checks)} checks)",
    "",
    f"- Final PDF: {PDF.name}",
    f"- PDF pages: {page_count}",
    f"- Final ZIP: {ZIP.name}",
    f"- ZIP contents: {', '.join(expected_zip)}",
    f"- Dataset: {df.shape[0]} rows x {df.shape[1]} columns",
    f"- Notebook: {len(cells)} cells ({len(code_cells)} code)",
    f"- Approximate main-body word count: {len(main_words)} (code listings and figures excluded)",
    f"- Abstract word count: {len(abstract_words)}",
    f"- Rendered page brightness mean: {statistics.mean(means):.1f}",
    f"- Maximum black-pixel ratio: {max(black_ratios):.4f}",
    "",
    "## Checks",
    "",
]
for name, ok, detail in checks:
    lines.append(f"- {'PASS' if ok else 'FAIL'} - **{name}**: {detail}")

lines += [
    "",
    "## Manual visual review checklist",
    "",
    "- Cover page follows the supplied sample's information structure without copying its project content.",
    "- Contents and Table of Figures are complete.",
    "- Code evidence is readable and comes from the submitted notebook.",
    "- CSV preview uses actual rows from ecommerce_2000.csv.",
    "- Tables and figures are complete with no footer overlap.",
    "- No black boxes, clipped text, overlapping elements, or broken glyphs.",
    "- References are alphabetical and consistent.",
    "",
    "The final PDF source is report/Angish_Sapkota_26152255.tex.",
]
QA_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:14]))
