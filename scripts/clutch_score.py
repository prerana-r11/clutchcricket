import pandas as pd

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

# Only innings 2 because pressure is meaningful there
df = df[df["innings"] == 2]

# Remove rows without pressure
df = df.dropna(subset=["pressure"])

# Calculate weighted pressure contribution
df["clutch_contribution"] = (
    df["runs_batter"] * df["pressure"]
)

# Group by batter
clutch_scores = (
    df.groupby("batter")["clutch_contribution"]
    .sum()
    .sort_values(ascending=False)
)

print(clutch_scores.head(20))