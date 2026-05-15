import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
df = pd.read_csv(
    r"C:\ClutchCricket\processed_data\t20i_ball_by_ball.csv"
)

# Pick one match
match_id = "1512754"

# Only second innings
match_df = df[
    (df["match_id"].astype(str) == match_id)
    & (df["innings"] == 2)
]

# Remove rows without pressure
match_df = match_df.dropna(subset=["pressure"])

# Create x-axis using legal balls bowled
x = match_df["balls_bowled"]

# Pressure values
y = match_df["pressure"]

# Plot
plt.figure(figsize=(12, 6))

plt.plot(x, y)

plt.title(f"Pressure Curve - Match {match_id}")
plt.xlabel("Balls Bowled")
plt.ylabel("Pressure")

plt.grid(True)

OUTPUT_DIR = Path(r"C:\ClutchCricket\visuals")
OUTPUT_DIR.mkdir(exist_ok=True)

plt.savefig(
    OUTPUT_DIR / f"pressure_curve_{match_id}.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()