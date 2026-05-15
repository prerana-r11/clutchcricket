import pandas as pd

# Load full dataset
df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

# Only second innings
df = df[df["innings"] == 2]
df = df.dropna(subset=["runs_needed"])

# Buckets
df["runs_needed_bucket"] = (
    (df["runs_needed"] / 5).round() * 5
)

df["balls_remaining_bucket"] = (
    (df["balls_remaining"] / 6).round() * 6
)

# Final result
final_states = (
    df.sort_values("balls_bowled")
    .groupby("match_id")
    .tail(1)
)

final_states["chase_won"] = (
    final_states["runs_needed"] <= 0
).astype(int)

results = final_states[["match_id", "chase_won"]]

df = df.merge(results, on="match_id")

# Historical win probability table
win_prob_table = (
    df.groupby([
        "runs_needed_bucket",
        "balls_remaining_bucket",
        "wickets"
    ])["chase_won"]
    .mean()
    .reset_index()
)

win_prob_table.rename(
    columns={"chase_won": "win_probability"},
    inplace=True
)

# Pick one match
match_id = "1512754"

match_df = df[df["match_id"].astype(str) == match_id].copy()

# Merge probabilities
match_df = match_df.merge(
    win_prob_table,
    on=[
        "runs_needed_bucket",
        "balls_remaining_bucket",
        "wickets"
    ],
    how="left"
)

print(
    match_df[[
        "over",
        "score",
        "wickets",
        "runs_needed",
        "balls_remaining",
        "win_probability"
    ]].tail(20)
)