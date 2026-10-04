"""
Reproducible creation of data/ecommerce_2000.csv for CMP4294 Assessment 2.

Source : data/source/OnlineRetail.csv  (Kaggle umerkk12/online-retail-business,
         a copy of the UCI Online Retail dataset; 541,909 line-item rows).
Output : data/ecommerce_2000.csv        (exactly 2,000 line-item rows).

Why this method (customer-aware, NOT a naive random sample):
- A naive 2,000-row sample leaves almost every customer with a single row,
  which destroys the repeated history needed for Recency/Frequency/Monetary.
- The source has huge orders (median 12 line items) and a few very frequent
  customers, so the 2,000-row budget is shared across many customers by
  (a) capping line items per order and (b) capping orders per customer.
- Customers are sampled deterministically (random_state=42) and stratified
  by order-frequency band so low-, medium- and high-engagement buyers are
  all represented. This is not cherry-picked for attractive clusters.

Reproduce with:  python data/make_ecommerce_2000.py
"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
SOURCE = DATA_DIR / "source" / "OnlineRetail.csv"
OUTPUT = DATA_DIR / "ecommerce_2000.csv"

SEED = 42                 # fixed seed for every random choice
TARGET_ROWS = 2000        # assignment maximum for the project dataset
LINE_CAP = 3              # max line items kept per order (in 2,000-row budget)
INV_CAP = 10              # max orders kept per customer
DATE_FMT = "%d-%m-%Y %H:%M"


def load_source():
    """Load the source transactions and parse the customer key and dates."""
    df = pd.read_csv(SOURCE, encoding="ISO-8859-1", dtype={"CustomerID": "string"})
    # Customer segmentation needs a customer key, so rows without CustomerID
    # are excluded here and this decision is documented in the notebook.
    df = df.dropna(subset=["CustomerID"]).copy()
    df["CustomerID"] = df["CustomerID"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format=DATE_FMT)
    return df


def band_for(order_count):
    """Map a customer to an engagement band by number of distinct orders."""
    if order_count <= 2:
        return 1
    if order_count <= 4:
        return 2
    if order_count <= 9:
        return 3
    if order_count <= 30:
        return 4
    return 5  # customers with >30 orders are excluded from the sample


def straddle(n, k):
    """Return up to k positions spread across range(n), including first/last."""
    positions = np.linspace(0, n - 1, min(n, k))
    return np.unique(np.round(positions).astype(int))


def customer_transactions(group):
    """Keep a bounded, time-spread subset of one customer orders and lines."""
    group = group.sort_values(["InvoiceDate", "InvoiceNo"])
    invoices = group["InvoiceNo"].unique()
    keep = set(invoices[straddle(len(invoices), INV_CAP)])
    group = group[group["InvoiceNo"].isin(keep)]
    chunks = []
    for _, invoice_rows in group.groupby("InvoiceNo"):
        invoice_rows = invoice_rows.sort_values("StockCode")
        chunks.append(invoice_rows.iloc[straddle(len(invoice_rows), LINE_CAP)])
    return pd.concat(chunks)


def build_dataset():
    """Sample customers round-robin across engagement bands until 2,000 rows."""
    df = load_source()
    order_counts = df.groupby("CustomerID")["InvoiceNo"].nunique()
    bands = order_counts.map(band_for)
    rng = np.random.default_rng(SEED)
    pools = {}
    for band_id in (1, 2, 3, 4):
        ids = bands[bands == band_id].index.to_numpy().copy()
        rng.shuffle(ids)
        pools[band_id] = list(ids)
    groups = {cid: g for cid, g in df.groupby("CustomerID")}
    pointers = {band_id: 0 for band_id in pools}
    frames = []
    total = 0
    while total < TARGET_ROWS:
        progressed = False
        for band_id in (1, 2, 3, 4):
            if pointers[band_id] >= len(pools[band_id]) or total >= TARGET_ROWS:
                continue
            customer_id = pools[band_id][pointers[band_id]]
            pointers[band_id] += 1
            progressed = True
            rows = customer_transactions(groups[customer_id])
            remaining = TARGET_ROWS - total
            if len(rows) <= remaining:
                frames.append(rows)
                total += len(rows)
            else:
                frames.append(rows.head(remaining))
                total += remaining
        if not progressed:
            break
    subset = pd.concat(frames).sample(frac=1.0, random_state=SEED)
    subset = subset.reset_index(drop=True)
    subset["InvoiceDate"] = subset["InvoiceDate"].dt.strftime(DATE_FMT)
    subset.to_csv(OUTPUT, index=False)
    print("SOURCE_ROWS", len(df))
    print("FINAL_SHAPE", subset.shape)
    print("UNIQUE_CUSTOMERS", subset["CustomerID"].nunique())
    print("CANCELLED_ROWS", int(subset["InvoiceNo"].astype(str).str.startswith("C").sum()))


if __name__ == "__main__":
    build_dataset()
