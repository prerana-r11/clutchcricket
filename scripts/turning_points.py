import pandas as pd

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

match_id = "1512754"

match_df = df[
    (df["match_id"].astype(str) == match_id)
    & (df["innings"] == 2)
]

match_df = match_df.dropna(subset=["pressure"])

# Calculate pressure change
match_df["pressure_delta"] = (
    match_df["pressure"].diff()
)

# Biggest pressure increases
turning_points = match_df.sort_values(
    by="pressure_delta",
    ascending=False
).head(10)

print(
    turning_points[[
        "over",
        "balls_bowled",
        "batter",
        "bowler",
        "score",
        "wickets",
        "required_run_rate",
        "pressure",
        "pressure_delta"
    ]]
)