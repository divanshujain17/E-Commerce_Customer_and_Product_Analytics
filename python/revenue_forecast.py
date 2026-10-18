"""Forecast the next three months of delivered-item revenue."""

from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "datasets"
OUTPUT_DIR = ROOT / "sql" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_monthly_revenue() -> pd.Series:
    orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
    items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv", usecols=["order_id", "price"])
    delivered = orders.loc[orders["order_status"].eq("delivered"), ["order_id", "order_purchase_timestamp"]]
    monthly = delivered.merge(items, on="order_id")
    return monthly.set_index("order_purchase_timestamp")["price"].resample("MS").sum()


def mape(actual: pd.Series, predicted: pd.Series) -> float:
    non_zero = actual.ne(0)
    return float((np.abs((actual[non_zero] - predicted[non_zero]) / actual[non_zero])).mean() * 100)


def main() -> None:
    revenue = load_monthly_revenue()
    holdout_size = min(3, max(1, len(revenue) // 5))
    train, test = revenue.iloc[:-holdout_size], revenue.iloc[-holdout_size:]
    validation_model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal="add" if len(train) >= 24 else None,
        seasonal_periods=12 if len(train) >= 24 else None,
    ).fit()
    validation = validation_model.forecast(holdout_size)
    metrics = pd.DataFrame([{"rmse": float(np.sqrt(((test - validation) ** 2).mean())), "mape_percent": mape(test, validation)}])

    final_model = ExponentialSmoothing(revenue, trend="add", seasonal="add", seasonal_periods=12).fit()
    forecast = final_model.forecast(3).rename("forecast_revenue").reset_index()
    forecast.columns = ["month", "forecast_revenue"]
    forecast.to_csv(OUTPUT_DIR / "revenue_forecast.csv", index=False)
    metrics.to_csv(OUTPUT_DIR / "revenue_forecast_metrics.csv", index=False)
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()