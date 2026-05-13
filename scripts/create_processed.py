import json
import pandas as pd
from pathlib import Path

MATCH_ID = "1512754"

RAW_FILE = Path(r"C:\ClutchCricket\data") / f"{MATCH_ID}.json"
OUTPUT_FILE = Path(r"C:\ClutchCricket\processed_data") / f"{MATCH_ID}_processed.csv"

OUTPUT_FILE.parent.mkdir(exist_ok=True)

with open(RAW_FILE, "r", encoding="utf-8") as f:
    match = json.load(f)

ball_data = []
target = None

for innings_index, innings in enumerate(match["innings"], start=1):
    total_score = 0
    wickets = 0
    balls_bowled = 0

    team_batting = innings["team"]
    teams = match["info"]["teams"]
    team_bowling = teams[1] if teams[0] == team_batting else teams[0]

    for over in innings["overs"]:
        over_num = over["over"]

        for delivery in over["deliveries"]:
            batter = delivery["batter"]
            bowler = delivery["bowler"]

            runs_batter = delivery["runs"]["batter"]
            runs_total = delivery["runs"]["total"]
            extras = delivery["runs"]["extras"]

            total_score += runs_total

            extra_details = delivery.get("extras", {})
            is_legal_delivery = not ("wides" in extra_details or "noballs" in extra_details)

            if is_legal_delivery:
                balls_bowled += 1

            wicket_fell = 0
            if "wickets" in delivery:
                wicket_fell = len(delivery["wickets"])
                wickets += wicket_fell

            balls_remaining = max(0, 120 - balls_bowled)

            runs_needed = None
            required_run_rate = None
            pressure = None

            if innings_index == 2 and target is not None:
                runs_needed = max(0, target - total_score)

                if balls_remaining > 0:
                    required_run_rate = (runs_needed * 6) / balls_remaining
                else:
                    required_run_rate = 0

                pressure = required_run_rate + (wickets * 1.5)

            ball_data.append({
                "match_id": MATCH_ID,
                "team_batting": team_batting,
                "team_bowling": team_bowling,
                "innings": innings_index,
                "over": over_num,
                "batter": batter,
                "bowler": bowler,
                "runs_batter": runs_batter,
                "runs_total": runs_total,
                "extras": extras,
                "legal_delivery": is_legal_delivery,
                "wicket_fell": wicket_fell,
                "score": total_score,
                "wickets": wickets,
                "balls_bowled": balls_bowled,
                "balls_remaining": balls_remaining,
                "target": target,
                "runs_needed": runs_needed,
                "required_run_rate": required_run_rate,
                "pressure": pressure
            })

    if innings_index == 1:
        target = total_score + 1

df = pd.DataFrame(ball_data)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved processed CSV to: {OUTPUT_FILE}")
print(df.head())
print(df.tail())