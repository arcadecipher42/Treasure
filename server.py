from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access this backend

# Store teams and scores (resets on server restart)
leaderboard = []

@app.route('/register', methods=['POST'])
def register_team():
    """Register a team before starting"""
    data = request.json
    team_name = data.get("team_name")

    if not team_name:
        return jsonify({"error": "Team name is required"}), 400

    for team in leaderboard:
        if team["team_name"] == team_name:
            return jsonify({"error": "Team already registered!"}), 400

    leaderboard.append({"team_name": team_name, "time": None})
    return jsonify({"message": f"Team '{team_name}' registered!"})

@app.route('/submit', methods=['POST'])
def submit_score():
    """Submit time taken after solving"""
    data = request.json
    team_name = data.get("team_name")
    time_taken = data.get("time")

    if not team_name or time_taken is None:
        return jsonify({"error": "Team name and time are required"}), 400

    for team in leaderboard:
        if team["team_name"] == team_name:
            team["time"] = time_taken
            break
    else:
        return jsonify({"error": "Team not found"}), 404

    return jsonify({"message": f"Score submitted for '{team_name}'!"})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get current leaderboard sorted by time"""
    sorted_leaderboard = sorted(
        [team for team in leaderboard if team["time"] is not None], 
        key=lambda x: x["time"]
    )
    return jsonify(sorted_leaderboard)

if __name__ == '__main__':
    app.run(debug=True)
