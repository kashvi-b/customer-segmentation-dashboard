import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def generate_sample_data(n=200):
    np.random.seed(42)
    return pd.DataFrame({
        "customer_id": range(1, n + 1),
        "total_spend": np.random.exponential(500, n),
        "purchase_frequency": np.random.poisson(5, n),
        "avg_order_value": np.random.normal(100, 30, n).clip(10),
        "days_since_last_purchase": np.random.randint(1, 365, n),
    })


def run_segmentation(df: pd.DataFrame, n_clusters=5) -> pd.DataFrame:
    features = df[[
        "total_spend", "purchase_frequency",
        "avg_order_value", "days_since_last_purchase"
    ]]
    scaler = StandardScaler()
    X = scaler.fit_transform(features.fillna(0))

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df = df.copy()
    df["segment"] = model.fit_predict(X)

    # Label segments by average spend rank
    spend_rank = df.groupby("segment")["total_spend"].mean().rank(ascending=False)
    label_map = {1: "Champions", 2: "Loyal", 3: "Potential", 4: "At Risk", 5: "Lost"}

    def get_label(seg):
        rank = int(spend_rank[seg])
        return label_map.get(rank, f"Segment {rank}")

    df["segment_label"] = df["segment"].map(get_label)
    return df


def get_segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("segment_label").agg(
        count=("customer_id", "count"),
        avg_spend=("total_spend", "mean"),
        avg_frequency=("purchase_frequency", "mean"),
        avg_order_value=("avg_order_value", "mean"),
        avg_recency=("days_since_last_purchase", "mean"),
    ).reset_index()
