#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT/report"
FINAL_BASENAME="Angish_Sapkota_26152255"

cd "$REPORT_DIR"

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
rm -f "${FINAL_BASENAME}.zip"
zip -j "${FINAL_BASENAME}.zip" \
    "${FINAL_BASENAME}.ipynb" \
    "data/ecommerce_2000.csv" >/dev/null

echo "Built:"
echo "  $ROOT/${FINAL_BASENAME}.pdf"
echo "  $ROOT/${FINAL_BASENAME}.zip"
echo "  $REPORT_DIR/qa/page-*.png"
