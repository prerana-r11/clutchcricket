import json
import pandas as pd

with open(r"C:\ClutchCricket\data\1512754.json", "r", encoding="utf-8") as f:
    match = json.load(f)

ball_data = []
target = None

for innings_index, innings in enumerate(match["innings"], start=1):
    total_score = 0
    wickets = 0
    balls_bowled = 0

    for over in innings["overs"]:
        over_num = over["over"]

        for ball_index, delivery in enumerate(over["deliveries"], start=1):
            batter = delivery["batter"]
            bowler = delivery["bowler"]
            runs = delivery["runs"]["total"]

            total_score += runs
            extras = delivery.get("extras", {})
            
            is_legal_delivery = not ("wides" in extras or "noballs" in extras)
            if is_legal_delivery:
                balls_bowled += 1

            wicket_fell = 0
            if "wickets" in delivery:
                wicket_fell = len(delivery["wickets"])
                wickets += wicket_fell

            balls_remaining = 120 - balls_bowled

            runs_needed = None
            required_run_rate = None
            pressure = None

            if innings_index == 2 and target is not None:
                runs_needed = target - total_score

                if balls_remaining > 0:
                    required_run_rate = (runs_needed * 6) / balls_remaining
                else:
                    required_run_rate = 0

                pressure = required_run_rate + (wickets * 1.5)

            ball_data.append({
                "innings": innings_index,
                "over": over_num,
                "ball": ball_index,
                "batter": batter,
                "bowler": bowler,
                "runs": runs,
                "wicket_fell": wicket_fell,
                "score": total_score,
                "wickets": wickets,
                "balls_remaining": balls_remaining,
                "runs_needed": runs_needed,
                "required_run_rate": required_run_rate,
                "pressure": pressure
            })

    if innings_index == 1:
        target = total_score + 1

df = pd.DataFrame(ball_data)

print(df.head())
print(df.tail(20))