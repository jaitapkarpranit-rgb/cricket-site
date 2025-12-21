import os
import requests

CRICAPI_KEY = os.environ.get("CRICAPI_KEY")

API_URL = "https://api.cricapi.com/v1/currentMatches"


def get_matches():
    if not CRICAPI_KEY:
        print("❌ CRICAPI_KEY missing")
        return []

    try:
        response = requests.get(
            API_URL,
            params={"apikey": CRICAPI_KEY},
            timeout=10
        )

        data = response.json()
        print("API STATUS:", data.get("status"))

        if data.get("status") != "success":
            print("API ERROR:", data)
            return []

        matches = []

        for m in data.get("data", []):
            teams = m.get("teams", [])
            scores = m.get("score", [])

            score1 = ""
            score2 = ""

            if len(scores) > 0:
                score1 = f'{scores[0].get("r","")}/{scores[0].get("w","")}'
            if len(scores) > 1:
                score2 = f'{scores[1].get("r","")}/{scores[1].get("w","")}'

            matches.append({
                "id": m.get("id"),
                "team1": teams[0] if len(teams) > 0 else "Team A",
                "team2": teams[1] if len(teams) > 1 else "Team B",
                "status": m.get("status", ""),
                "venue": m.get("venue", ""),
                "date": m.get("date", ""),
                "score1": score1,
                "score2": score2
            })

        print("MATCHES FETCHED:", len(matches))
        return matches

    except Exception as e:
        print("EXCEPTION:", e)
        return []
