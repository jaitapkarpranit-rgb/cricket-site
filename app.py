from flask import Flask, render_template, request
from data import get_matches

app = Flask(__name__)


# ---------- STATIC PAGES (MUST COME FIRST) ----------

@app.route("/series")
def series():
    series_list = [
        "Indian Premier League (IPL)",
        "Big Bash League (BBL)",
        "The Ashes",
        "ICC World Cup",
        "ICC T20 World Cup"
    ]
    return render_template("series.html", series=series_list)


@app.route("/teams")
def teams():
    teams_list = [
        "India",
        "Australia",
        "England",
        "South Africa",
        "New Zealand",
        "Pakistan",
        "Sri Lanka",
        "West Indies",
        "CSK",
        "MI",
        "RCB"
    ]
    return render_template("teams.html", teams=teams_list)


# ---------- HOME & STATUS FILTER ----------

@app.route("/")
@app.route("/<status>")
def home(status=None):
    matches = get_matches()

    # SEARCH
    search = request.args.get("q", "").lower()
    if search:
        matches = [
            m for m in matches
            if search in m["team1"].lower() or search in m["team2"].lower()
        ]

    # STATUS FILTER (tabs: live / finished / upcoming)
    if status:
        matches = [
            m for m in matches
            if status.lower() in m["status"].lower()
        ]

    return render_template(
        "home.html",
        matches=matches,
        current=status
    )


# ---------- MATCH DETAIL ----------

@app.route("/match/<match_id>")
def match_detail(match_id):
    matches = get_matches()
    match = next((m for m in matches if m["id"] == match_id), None)

    if not match:
        return "Match not found", 404

    return render_template("match.html", match=match)


# ---------- RUN ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=False)
