from flask import Flask, jsonify

app = Flask(__name__)

# Dummy API endpoints
@app.route('/get_points_balance')
def get_points_balance():
    # Mock response data
    points_data = {"balance": 100}
    return jsonify(points_data)

@app.route('/get_referee_stats')
def get_referee_stats():
    # Mock response data
    referee_stats_data = {"referees": 10}
    return jsonify(referee_stats_data)

@app.route('/get_vault_balance')
def get_vault_balance():
    # Mock response data
    vault_balance_data = {"balance": 1000}
    return jsonify(vault_balance_data)

if __name__ == '__main__':
    app.run(debug=True)
