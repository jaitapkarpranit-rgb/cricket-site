import os
import requests

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

BASE_URL = f"https://{RAPIDAPI_HOST}"


def get_matches():
    try:
        return _get_live_matches()
    except Exception as e:
        print("API error:", e)
        return _dummy_matches()


def _get_live_matches():
    url = f"{BASE_URL}/cricket-match-info"
    params = {"matchid": "102040"}  # sample match id (API limitation)

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=params, timeout=5)
    data = response.json()

    match = data.get("data", {})

    return [{
        "id": 1,
        "team1": match.get("team1", "Team A"),
        "team2": match.get("team2", "Team B"),
        "score1": match.get("team1_score", ""),
        "score2": match.get("team2_score", ""),
        "status": match.get("status", "Live")
    }]


def _dummy_matches():
    return [
        {
            "id": 1,
            "team1": "India",
            "team2": "Australia",
            "score1": "245/6",
            "score2": "230/10",
            "status": "Finished"
        }
    ]
