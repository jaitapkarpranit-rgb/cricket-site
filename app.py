from flask import Flask, render_template, request
from data import get_matches

app = Flask(__name__)


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

    # STATUS FILTER (TABS)
    if status:
        matches = [
            m for m in matches
            if m["status"].lower() == status.lower()
        ]

    return render_template(
        "home.html",
        matches=matches,
        current=status
    )


@app.route("/match/<int:match_id>")
def match_detail(match_id):
    matches = get_matches()
    match = next((m for m in matches if m["id"] == match_id), None)

    if not match:
        return "Match not found", 404

    return render_template("match.html", match=match)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=False)

