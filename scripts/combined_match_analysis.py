import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

# Second innings only
df = df[df["innings"] == 2]
df = df.dropna(subset=["runs_needed"])

# Buckets
df["runs_needed_bucket"] = (
    (df["runs_needed"] / 5).round() * 5
)

df["balls_remaining_bucket"] = (
    (df["balls_remaining"] / 6).round() * 6
)

# Match result
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

# Historical win probability
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

# Select match
match_id = "1512754"

match_df = df[
    df["match_id"].astype(str) == match_id
].copy()

# Merge win probability
match_df = match_df.merge(
    win_prob_table,
    on=[
        "runs_needed_bucket",
        "balls_remaining_bucket",
        "wickets"
    ],
    how="left"
)

# Turning points
match_df["pressure_delta"] = (
    match_df["pressure"].diff()
)

turning_points = match_df.sort_values(
    by="pressure_delta",
    ascending=False
).head(5)

# Wickets
wickets_df = match_df[
    match_df["wicket_fell"] > 0
]

# Plot
fig, ax1 = plt.subplots(figsize=(14, 7))

# Pressure
ax1.plot(
    match_df["balls_bowled"],
    match_df["pressure"],
    label="Pressure"
)

# Wicket markers
ax1.scatter(
    wickets_df["balls_bowled"],
    wickets_df["pressure"],
    marker="x",
    s=100,
    label="Wicket"
)

# Turning points
ax1.scatter(
    turning_points["balls_bowled"],
    turning_points["pressure"],
    marker="o",
    s=120,
    label="Turning Point"
)

ax1.set_xlabel("Balls Bowled")
ax1.set_ylabel("Pressure")

# Win probability axis
ax2 = ax1.twinx()

ax2.plot(
    match_df["balls_bowled"],
    match_df["win_probability"] * 100,
    linestyle="--",
    label="Win Probability (%)"
)

ax2.set_ylabel("Win Probability (%)")

plt.title(f"Combined Match Analysis - {match_id}")

fig.legend(loc="upper left")

OUTPUT_DIR = Path(r"C:\ClutchCricket\visuals")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.savefig(
    OUTPUT_DIR / f"combined_analysis_{match_id}.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()