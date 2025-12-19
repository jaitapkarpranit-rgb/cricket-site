# data.py

def get_matches():
    """
    SINGLE ENTRY POINT FOR MATCH DATA

    Later:
    - Replace this function’s body with real API calls
    - UI / routes will NOT change
    """

    return _dummy_matches()


def _dummy_matches():
    return [
        {
            "id": 1,
            "team1": "India",
            "team2": "Australia",
            "score1": "245/6",
            "score2": "230/10",
            "status": "Finished"
        },
        {
            "id": 2,
            "team1": "CSK",
            "team2": "MI",
            "score1": "180/5",
            "score2": "175/8",
            "status": "Live"
        },
        {
            "id": 3,
            "team1": "RCB",
            "team2": "KKR",
            "score1": "",
            "score2": "",
            "status": "Upcoming"
        }
    ]
