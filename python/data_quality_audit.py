"""Run lightweight quality checks across the Olist source extracts."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "datasets"
OUTPUT_DIR = ROOT / "sql" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
}


def audit_table(name: str, frame: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for column in frame.columns:
        rows.append(
            {
                "table": name,
                "column": column,
                "rows": len(frame),
                "missing_count": int(frame[column].isna().sum()),
                "missing_percent": round(frame[column].isna().mean() * 100, 2),
                "unique_count": int(frame[column].nunique(dropna=True)),
                "unique_percent": round(frame[column].nunique(dropna=True) / max(len(frame), 1) * 100, 2),
            }
        )
    return rows


def main() -> None:
    frames = {name: pd.read_csv(DATA_DIR / filename) for name, filename in FILES.items()}
    audit = pd.DataFrame(
        row for name, frame in frames.items() for row in audit_table(name, frame)
    )

    orders = frames["orders"]
    items = frames["items"]
    products = frames["products"]
    orphan_checks = pd.DataFrame(
        [
            {
                "check": "items_without_orders",
                "count": int((~items["order_id"].isin(orders["order_id"])).sum()),
            },
            {
                "check": "items_without_products",
                "count": int((~items["product_id"].isin(products["product_id"])).sum()),
            },
        ]
    )

    numeric = items["price"].astype(float)
    q1, q3 = numeric.quantile([0.25, 0.75])
    iqr = q3 - q1
    outliers = pd.DataFrame(
        [{"column": "price", "lower_bound": q1 - 1.5 * iqr, "upper_bound": q3 + 1.5 * iqr,
          "outlier_count": int(((numeric < q1 - 1.5 * iqr) | (numeric > q3 + 1.5 * iqr)).sum())}]
    )

    audit.to_csv(OUTPUT_DIR / "data_quality_audit.csv", index=False)
    orphan_checks.to_csv(OUTPUT_DIR / "orphan_id_checks.csv", index=False)
    outliers.to_csv(OUTPUT_DIR / "iqr_outlier_summary.csv", index=False)
    print(f"Wrote {len(audit)} column checks and {len(orphan_checks)} relationship checks")


if __name__ == "__main__":
    main()