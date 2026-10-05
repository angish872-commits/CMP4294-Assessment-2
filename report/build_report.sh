#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT/report"
FINAL_BASENAME="Angish_Sapkota_26152255"

cd "$REPORT_DIR"

# Fetch the two institutional logos used on the sample-style cover.
mkdir -p assets
curl -L --fail --silent --show-error   "https://api.myunicampus.com/6da490c2-415b-4732-9b44-b41fc1a2565b_1744952092980.png"   -o assets/sunway_logo.png
curl -L --fail --silent --show-error   "https://seeklogo.com/images/B/birmingham-city-university-logo-5A4A5571BE-seeklogo.com.png"   -o assets/bcu_logo.png

rm -f "${FINAL_BASENAME}.aux" "${FINAL_BASENAME}.log" "${FINAL_BASENAME}.out" \
      "${FINAL_BASENAME}.toc" "${FINAL_BASENAME}.lof" "${FINAL_BASENAME}.lot" \
      "${FINAL_BASENAME}.pdf"

xelatex -interaction=nonstopmode -halt-on-error "${FINAL_BASENAME}.tex"
xelatex -interaction=nonstopmode -halt-on-error "${FINAL_BASENAME}.tex"

cp "${FINAL_BASENAME}.pdf" "$ROOT/${FINAL_BASENAME}.pdf"

rm -rf "$REPORT_DIR/qa"
mkdir -p "$REPORT_DIR/qa"
pdftoppm -png -r 144 "$ROOT/${FINAL_BASENAME}.pdf" "$REPORT_DIR/qa/page" >/dev/null 2>&1

python3 - <<'PY'
from pathlib import Path
qa = Path("qa")
for p in sorted(qa.glob("page-*.png")):
    n = int(p.stem.split("-")[-1])
    p.rename(qa / f"page-{n:02d}.png")
PY

cd "$ROOT"
# Single-slot Moodle submission: bundle report, notebook, and dataset together.
rm -f "${FINAL_BASENAME}.zip"
zip -j "${FINAL_BASENAME}.zip" \
    "${FINAL_BASENAME}.pdf" \
    "${FINAL_BASENAME}.ipynb" \
    "data/ecommerce_2000.csv" >/dev/null

echo "Built:"
echo "  $ROOT/${FINAL_BASENAME}.pdf"
echo "  $ROOT/${FINAL_BASENAME}.zip"
echo "  $REPORT_DIR/qa/page-*.png"
