from flask import Flask, render_template, request
import data   # IMPORTANT: do NOT change this

app = Flask(__name__)


# ---------- STATIC PAGES ----------

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


# ---------- HOME ----------

@app.route("/")
@app.route("/<status>")
def home(status=None):
    matches = data.get_matches()

    # SEARCH
    search = request.args.get("q", "").lower()
    if search:
        matches = [
            m for m in matches
            if search in m["team1"].lower() or search in m["team2"].lower()
        ]

    # STATUS FILTER
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
    match = data.get_match_detail(match_id)

    if not match:
        return "Match not found", 404

    return render_template("match.html", match=match)


# ---------- RUN ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=False)
