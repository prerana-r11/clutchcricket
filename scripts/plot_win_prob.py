import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

df = df[df["innings"] == 2]
df = df.dropna(subset=["runs_needed"])

df["runs_needed_bucket"] = (df["runs_needed"] / 5).round() * 5
df["balls_remaining_bucket"] = (df["balls_remaining"] / 6).round() * 6

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

match_id = "1512754"

match_df = df[df["match_id"].astype(str) == match_id].copy()

match_df = match_df.merge(
    win_prob_table,
    on=[
        "runs_needed_bucket",
        "balls_remaining_bucket",
        "wickets"
    ],
    how="left"
)

plt.figure(figsize=(12, 6))

plt.plot(
    match_df["balls_bowled"],
    match_df["win_probability"] * 100
)

plt.title(f"Win Probability Curve - Match {match_id}")
plt.xlabel("Balls Bowled")
plt.ylabel("Win Probability (%)")
plt.grid(True)

OUTPUT_DIR = Path(r"C:\ClutchCricket\visuals")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.savefig(
    OUTPUT_DIR / f"win_probability_{match_id}.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()