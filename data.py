import os
import requests
from datetime import datetime, timedelta


SPORTMONKS_TOKEN = os.environ.get("SPORTMONKS_TOKEN")
BASE_URL = "https://cricket.sportmonks.com/api/v2.0"


def _get(endpoint, params=None):
    if not SPORTMONKS_TOKEN:
        print("❌ SPORTMONKS_TOKEN missing")
        return None

    if params is None:
        params = {}

    params["api_token"] = SPORTMONKS_TOKEN

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=10
        )
        data = response.json()
        return data.get("data")
    except Exception as e:
        print("❌ SportMonks API error:", e)
        return None


# ---------- MATCH LIST ----------

def get_matches():
    from datetime import datetime, timedelta

    today = datetime.utcnow().date()
    start = today - timedelta(days=2)
    end = today + timedelta(days=7)

    fixtures = _get(
        "fixtures",
        {
            "include": "localteam,visitorteam,venue,runs",
            "filter[starts_between]": f"{start},{end}",
            "sort": "starting_at"
        }
    )


    if not fixtures:
        return []

    matches = []

    for f in fixtures:
        local = f.get("localteam", {})
        visitor = f.get("visitorteam", {})
        runs = f.get("runs", [])

        score1 = ""
        score2 = ""

        if len(runs) > 0:
            score1 = f'{runs[0].get("score","")}/{runs[0].get("wickets","")}'
        if len(runs) > 1:
            score2 = f'{runs[1].get("score","")}/{runs[1].get("wickets","")}'

        matches.append({
            "id": f.get("id"),
            "team1": local.get("name", "Team A"),
            "team2": visitor.get("name", "Team B"),
            "status": f.get("status", ""),
            "venue": (f.get("venue") or {}).get("name", ""),
            "date": f.get("starting_at", ""),
            "score1": score1,
            "score2": score2
        })

    return matches


# ---------- MATCH DETAIL ----------

def get_match_detail(match_id):
    fixture = _get(
        f"fixtures/{match_id}",
        {
            "include": "localteam,visitorteam,venue"
        }
    )

    if not fixture:
        return None

    return {
        "id": fixture.get("id"),
        "name": f'{fixture.get("localteam", {}).get("name","")} vs {fixture.get("visitorteam", {}).get("name","")}',
        "status": fixture.get("status", ""),
        "venue": (fixture.get("venue") or {}).get("name", ""),
        "date": fixture.get("starting_at", "")
    }


# ---------- SCORECARD ----------

def get_match_scorecard(match_id):
    fixture = _get(
        f"fixtures/{match_id}",
        {
            "include": "runs.team,runs.batting.batsman,runs.bowling.bowler"
        }
    )

    print("==== RAW SPORTMONKS FIXTURE ====")
    print(fixture)
    print("==== END FIXTURE ====")

    fixture = _get(
        f"fixtures/{match_id}",
        {
            "include": "runs.team,runs.batting.batsman,runs.bowling.bowler"
        }
    )

    if not fixture:
        return None

    runs = fixture.get("runs", [])
    if not runs:
        return None

    innings_data = []

    for r in runs:
        innings_data.append({
            "inning": f"{(r.get('team') or {}).get('name','')} Innings",
            "batting": [
                {
                    "batsman": (b.get("batsman") or {}).get("fullname", ""),
                    "r": b.get("score", ""),
                    "b": b.get("balls", ""),
                    "fours": b.get("four_x", ""),
                    "sixes": b.get("six_x", ""),
                    "sr": b.get("rate", "")
                }
                for b in r.get("batting", [])
            ],
            "bowling": [
                {
                    "bowler": (bo.get("bowler") or {}).get("fullname", ""),
                    "o": bo.get("overs", ""),
                    "r": bo.get("runs", ""),
                    "w": bo.get("wickets", ""),
                    "econ": bo.get("rate", "")
                }
                for bo in r.get("bowling", [])
            ]
        })

    return {
        "innings": innings_data
    }

