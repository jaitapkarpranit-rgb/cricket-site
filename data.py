import os
import requests

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

BASE_URL = f"https://{RAPIDAPI_HOST}"


def get_matches():
    try:
        if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
            raise Exception("API keys missing")
        return _get_live_matches()
    except Exception as e:
        print("API error:", e)
        return _dummy_matches()


def _get_live_matches():
    url = f"{BASE_URL}/matches/v1/live"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, timeout=5)
    data = response.json()

    matches = []

    for type_block in data.get("typeMatches", []):
        for series in type_block.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper")
            if not wrapper:
                continue

            for m in wrapper.get("matches", []):
                info = m.get("matchInfo", {})
                score = m.get("matchScore", {})

                team1 = info.get("team1", {}).get("teamName", "")
                team2 = info.get("team2", {}).get("teamName", "")

                matches.append({
                    "id": info.get("matchId"),
                    "team1": team1,
                    "team2": team2,
                    "score1": _score(score, 0),
                    "score2": _score(score, 1),
                    "status": info.get("status", "Live")
                })

    return matches[:10]


def _score(score, idx):
    try:
        return score["teamScore"][idx]["inngs1"]["runs"]
    except Exception:
        return ""


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
