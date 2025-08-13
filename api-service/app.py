# ./api-service/app.py
import os
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# Connect to Redis
# We use the hostname 'redis' because that will be the service name in Docker Compose.
try:
    redis_client = redis.Redis(
        host=os.environ.get('REDIS_HOST', 'redis'),
        port=6379,
        db=0,
        socket_connect_timeout=2,
        socket_timeout=2,
        decode_responses=True # Decode responses to strings
    )
    redis_client.ping()
    print("Connected to Redis successfully!")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    redis_client = None

@app.route('/vote', methods=['POST'])
def vote():
    if not redis_client:
        return jsonify({"error": "Database connection failed"}), 500

    data = request.get_json()
    if not data or 'vote' not in data:
        return jsonify({"error": "Vote not provided"}), 400

    vote_option = data['vote']
    if vote_option not in ['cats', 'dogs']:
        return jsonify({"error": "Invalid vote option"}), 400

    # Use a Redis Hash to store vote counts. 'hincrby' increments a field in a hash.
    count = redis_client.hincrby('votes', vote_option, 1)
    return jsonify({"option": vote_option, "count": count})

# A simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    # Host on 0.0.0.0 to make it accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)