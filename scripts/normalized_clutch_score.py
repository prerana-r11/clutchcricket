import pandas as pd

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

df = df[df["innings"] == 2]
df = df.dropna(subset=["pressure"])

df["clutch_contribution"] = df["runs_batter"] * df["pressure"]

player_stats = df.groupby("batter").agg(
    total_runs=("runs_batter", "sum"),
    balls_faced=("legal_delivery", "sum"),
    avg_pressure=("pressure", "mean"),
    total_clutch=("clutch_contribution", "sum")
)

player_stats["clutch_per_ball"] = (
    player_stats["total_clutch"] / player_stats["balls_faced"]
)

player_stats["strike_rate"] = (
    player_stats["total_runs"] / player_stats["balls_faced"] * 100
)

# filter tiny samples
player_stats = player_stats[player_stats["balls_faced"] >= 30]

print(
    player_stats.sort_values(
        by="clutch_per_ball",
        ascending=False
    ).head(20)
)