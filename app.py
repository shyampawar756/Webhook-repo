from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from flask import Flask


app = Flask(__name__)
client = MongoClient("mongodb+srv://shyampawar756:xuvsGBy4Jk8SxLBq@cluster0.wpcti6y.mongodb.net/")
db = client["webhook_db"]
collection = db["events"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Parse the event type and payload
    event_type = request.headers.get('X-GitHub-Event')
    payload = {}

    if event_type == "push":
        payload = {
            "author": data["pusher"]["name"],
            "action": "push",
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.utcnow()
        }

    elif event_type == "pull_request":
        action = data["action"]
        if action in ["opened"]:
            payload = {
                "author": data["pull_request"]["user"]["login"],
                "action": "pull_request",
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow()
            }

    elif event_type == "pull_request" and data["action"] == "closed" and data["pull_request"]["merged"]:
        payload = {
            "author": data["pull_request"]["user"]["login"],
            "action": "merge",
            "from_branch": data["pull_request"]["head"]["ref"],
            "to_branch": data["pull_request"]["base"]["ref"],
            "timestamp": datetime.utcnow()
        }

    if payload:
        collection.insert_one(payload)

    return jsonify({"status": "success"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    data = list(collection.find().sort("timestamp", -1).limit(10))
    for item in data:
        item["_id"] = str(item["_id"])
        item["timestamp"] = item["timestamp"].strftime("%d %b %Y - %I:%M %p UTC")
    return jsonify(data)

@app.route("/test")
def test():
    return "Test route is working!"

if __name__ == "__main__":
    app.run(debug=True)
