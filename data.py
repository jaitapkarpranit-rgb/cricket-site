import requests

CRICAPI_KEY = "35f9a069-2dfa-4ce4-8ec6-ca09a515e072"

BASE_URL = "https://api.cricapi.com/v1"


def get_matches():
    url = f"{BASE_URL}/currentMatches"

    params = {
        "apikey": CRICAPI_KEY,
        "offset": 0
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    matches = []

    for m in data.get("data", []):
        teams = m.get("teams", [])

        if len(teams) < 2:
            continue

        score = m.get("score", [])

        matches.append({
            "id": m.get("id"),
            "team1": teams[0],
            "team2": teams[1],
            "score1": format_score(score, 0),
            "score2": format_score(score, 1),
            "status": m.get("status", "")
        })

    return matches


def format_score(score_list, idx):
    try:
        s = score_list[idx]
        return f"{s['r']}/{s['w']} ({s['o']} ov)"
    except Exception:
        return ""
