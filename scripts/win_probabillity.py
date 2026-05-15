import pandas as pd

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

# Only second innings
df = df[df["innings"] == 2]

# Remove rows without chase info
df = df.dropna(subset=["runs_needed"])

# Bucket states
df["runs_needed_bucket"] = (
    (df["runs_needed"] / 5).round() * 5
)

df["balls_remaining_bucket"] = (
    (df["balls_remaining"] / 6).round() * 6
)

# Determine if chase succeeded
# Final row of each match
final_states = (
    df.sort_values("balls_bowled")
    .groupby("match_id")
    .tail(1)
)

# Match result
final_states["chase_won"] = (
    final_states["runs_needed"] <= 0
).astype(int)

# Keep only result column
results = final_states[["match_id", "chase_won"]]

# Merge result back into every ball
df = df.merge(results, on="match_id")

# Group similar situations
win_prob = (
    df.groupby([
        "runs_needed_bucket",
        "balls_remaining_bucket",
        "wickets"
    ])["chase_won"]
    .mean()
    .reset_index()
)

win_prob.rename(
    columns={"chase_won": "win_probability"},
    inplace=True
)

print(win_prob.head(20))