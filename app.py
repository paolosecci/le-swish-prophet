from flask import Flask, render_template, jsonify, request
import datetime
import json
import pandas as pd
from pytz import timezone
import analyze_nba_data as nba_analyzer

app = Flask(__name__)
last_nba_data_update = None

@app.route("/")
def le_swish_prophet():
    global last_nba_data_update
    return render_template("LeSwishProphet.html", last_data_update=last_nba_data_update)

@app.route("/ingest", methods=["POST"])
def ingest_nba_json_data():
    data = request.get_json()
    global last_nba_data_update
    if not data or "player_data" not in data or "team_data" not in data:
        return jsonify({"error": "missing data"}), 400
    try:
        with open("data/nba_player_boxscores.json", "w") as f:
            json.dump(data["player_data"], f)
        with open("data/nba_team_boxscores.json", "w") as f:
            json.dump(data["team_data"], f)
        last_nba_data_update = datetime.datetime.now()
        return jsonify({
            "status": "successfully pushed nba data",
            "last_update": last_nba_data_update.astimezone(timezone('US/Pacific')).strftime("%Y-%m-%d %H:%M:%S PST")
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/last-update")
def get_last_update():
    global last_nba_data_update
    if last_nba_data_update:
        return jsonify({
            "last_update": last_nba_data_update.astimezone(timezone('US/Pacific')).strftime("%Y-%m-%d %H:%M:%S PST")
        })
    return jsonify({"last_update": "Never"})

@app.route("/predict/<team>")
def predict(team):
    with open('data/nba_player_boxscores.json') as file_in:
        nba_json = json.load(file_in)
    df = nba_analyzer.clean_df(nba_analyzer.make_json_df(nba_json))
    df = nba_analyzer.make_days_since_col(df)
    team_df = nba_analyzer.get_team_df(team, df)
    team_lineup = nba_analyzer.predict_lineup(team_df)
    p_json_out = []
    sum_pts = 0
    for player in team_lineup:
        p_pts = nba_analyzer.predict_stat(player, 'PTS', team_df)
        p_json_out.append({
            'NAME': player,
            'PTS': p_pts,
            'AST': nba_analyzer.predict_stat(player, 'AST', team_df),
            'REB': nba_analyzer.predict_stat(player, 'REB', team_df)
        })
        sum_pts += p_pts
    json_out = [sum_pts, p_json_out]
    return jsonify(json_out)

@app.route('/simgame/<team1>/<team2>')
def simgame(team1, team2):
    p_t1 = nba_analyzer.predict_team(team1)
    p_t2 = nba_analyzer.predict_team(team2)
    t1s = (p_t1['predicted_pts'] + p_t2['predicted_opp_pts']) / 2
    t2s = (p_t2['predicted_pts'] + p_t1['predicted_opp_pts']) / 2
    return jsonify([t1s, t2s])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
