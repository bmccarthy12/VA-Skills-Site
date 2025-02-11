import requests
import json
import time

# Replace with your actual API key
API_KEY = "APIKey"  # ***REPLACE WITH YOUR ACTUAL API KEY***

# Season ID - Replace with the correct season ID
SEASON_ID = 190  # ***REPLACE WITH THE CORRECT SEASON ID***

team_list = [121849, 46465, 46468, 46471, 98485, 154568, 169590, 169669, 110896, 169750, 169751, 133474, 169776, 78132, 78134, 79175, 107040, 138841, 109693, 102975, 154029, 170054, 170204, 170205, 141212, 157577, 111660, 131366, 74175, 101992, 161029, 74174, 74173, 74172, 170287, 26932, 28438, 28441, 40945, 64868, 140967, 4086, 4096, 4101, 4106, 4116, 26686, 26689, 139683, 172076, 172727, 172967, 172968, 173024, 136488, 17032, 17035, 83827, 3441, 25570, 27013, 35863, 14704, 157067, 81691, 49878, 157068, 130499, 56191, 39544, 173800, 50999, 36862, 155640, 158054, 158055, 15001, 14998, 51000, 158051, 175524, 53190, 53222, 43639, 176155, 46474, 98329, 135883, 131943, 131952, 138962, 176437, 176442, 107622, 176492, 4091, 4111, 26668, 26683, 54326, 54327, 160910, 160911, 67311, 140834, 63681, 168065, 177857, 146827, 178023, 178024, 146829, 178463, 76817, 76818, 117062, 43747, 66423, 119695, 119696, 119697, 119698, 4166, 88963, 179542, 5666, 179867, 180039, 161426, 115412, 164326, 181238, 156054, 181972, 182377, 48711, 78014, 76876, 161908]

def get_skills_data(team_list, output_filename="skills_data.json"):
    """Retrieves skills data for a list of teams using the /teams/{id}/skills endpoint."""

    all_teams_data = []
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        for team_number in team_list:
            skills_url = f"https://www.robotevents.com/api/v2/teams/{team_number}/skills?program[]=1&season[]={SEASON_ID}"  # Correct URL
            skills_response = requests.get(skills_url, headers=headers)

            if skills_response.status_code == 404:  # Check for 404 (no skills data)
                print(f"Team '{team_number}' has no skills data for season {SEASON_ID}.")
                # all_teams_data.append({
                #     "team_number": team_number,
                #     "team_name": team_name,
                #     "team_id": team_id,
                #     "skills_data": []
                # })
                continue

            skills_response.raise_for_status()
            skills_data = skills_response.json().get("data", [])

            event_scores = {}  # Dictionary to track the best scores for each event

            for entry in skills_data:
                event_id = entry["event"]["id"]
                event_name = entry["event"]["name"]
                score = entry["score"]
                team_name = entry["team"]["name"]

                if event_id not in event_scores:
                    event_scores[event_id] = {
                        "event_name": event_name,
                        "programming_score": 0,
                        "driver_score": 0,
                        "total_score": 0,
                        "team_number": team_number,
                        "team_name": team_name
                    }

                if entry["type"] == "programming":
                    event_scores[event_id]["programming_score"] = max(event_scores[event_id]["programming_score"], score)
                elif entry["type"] == "driver":
                    event_scores[event_id]["driver_score"] = max(event_scores[event_id]["driver_score"], score)

                event_scores[event_id]["total_score"] = (
                    event_scores[event_id]["programming_score"] +
                    event_scores[event_id]["driver_score"]
                )

            # Find the event with the highest total score
            best_event = max(event_scores.values(), key=lambda x: x["total_score"], default=None)

            if best_event:
                all_teams_data.append({
                    "team_number": best_event["team_number"],
                    "team_name": best_event["team_name"],
                    "event_name": best_event["event_name"],
                    "programming_score": best_event["programming_score"],
                    "driver_score": best_event["driver_score"],
                    "total_score": best_event["total_score"]
                })

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(all_teams_data, f, indent=2, ensure_ascii=False)

        print(f"Skills data saved to {output_filename}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
    output_file = "skills_list.json"
    success = get_skills_data(team_list, output_file)
    if success:
        print("Skills data retrieval and saving complete.")
    else:
        print("Skills data retrieval and saving failed.")