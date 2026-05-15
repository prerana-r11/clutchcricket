import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

# Only chase innings
df = df[df["innings"] == 2]

# Remove missing pressure
df = df.dropna(subset=["pressure"])

# Clutch contribution
df["clutch_contribution"] = (
    df["runs_batter"] * df["pressure"]
)

# Aggregate by batter
clutch_scores = (
    df.groupby("batter")["clutch_contribution"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

# Plot
plt.figure(figsize=(12, 8))

clutch_scores.sort_values().plot(kind="barh")

plt.title("Top Clutch Batters in T20 Chases")
plt.xlabel("Clutch Score")
plt.ylabel("Batter")

plt.tight_layout()

plt.show()