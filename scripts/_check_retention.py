"""Check retention data and suggest better visualization."""
import pandas as pd

df = pd.read_csv("data/metrics/retention.csv", parse_dates=["cohort_month"])
print(f"Shape: {df.shape}")
print(f"Date range: {df['cohort_month'].min().date()} to {df['cohort_month'].max().date()}")
print(f"Cohorts with n_new > 0: {(df['n_new'] > 0).sum()}")

# Show last 20 cohorts
print("\n=== Last 20 cohorts ===")
print(df.tail(20).to_string(index=False))

# Show first 10 cohorts
print("\n=== First 10 cohorts ===")
print(df.head(10).to_string(index=False))

# Summary stats
for col in [c for c in df.columns if c.startswith("retention_")]:
    col_data = df[df[col].notna()][col]
    if len(col_data):
        print(f"\n{col}: mean={col_data.mean():.1%}, median={col_data.median():.1%}")
        # Show last 5 values
        recent = df[df[col].notna()].tail(5)
        print(f"  Recent: {[f'{v:.0%}' for v in recent[col].values]}")

# Cross-tab: cohort year x retention_6mo
df["year"] = df["cohort_month"].dt.year
pivot = df.groupby("year").agg(
    cohorts=("cohort_month", "count"),
    avg_retention_1mo=("retention_1mo", "mean"),
    avg_retention_3mo=("retention_3mo", "mean"),
    avg_retention_6mo=("retention_6mo", "mean"),
)
print("\n=== Yearly averages ===")
print(pivot.to_string())
