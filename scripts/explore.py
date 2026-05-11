import json

with open("C:\\ClutchCricket\\data\\1512754.json","r") as f:
    match=json.load(f)




for innings_index, innings in enumerate(match["innings"], start=1):
    print(f"\nINNINGS {innings_index}")
    total_score = 0
    wickets = 0
    
    for over in innings["overs"]:
        over_num=over["over"]
            
        for ball_index, delivery in enumerate(over["deliveries"], start=1):
            batter=delivery["batter"]
            bowler=delivery["bowler"]
            runs=delivery["runs"]["total"]
                
            total_score+=runs
            if "wickets" in delivery:
                wickets += len(delivery["wickets"])
                    
            print(
                f"{over_num}.{ball_index}: {bowler} to {batter} - "
                f"{runs} runs | Score: {total_score}/{wickets}"
            )