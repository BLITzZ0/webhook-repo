from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get environment variables
mongo_uri = os.getenv("MONGO_URI")
db_client = os.getenv("DB_CLIENT")       
db_collection = os.getenv("DB_COLLECTION")

if not mongo_uri or not db_client or not db_collection:
    raise Exception("Missing environment variables for DB connection")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_client]
collection = db[db_collection]

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# GitHub Webhook receiver route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        event_type = request.headers.get("X-GitHub-Event")
        data = request.json
        print("Webhook Received:", event_type)

        record = {}

        if event_type == "push":
            record = {
                "request_id": data.get("after"),
                "author": data.get("pusher", {}).get("name", "unknown"),
                "action": "PUSH",
                "from_branch": None,
                "to_branch": data.get("ref", "").split("/")[-1],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        elif event_type == "pull_request":
            pr = data.get("pull_request", {})
            pr_action = data.get("action")
            is_merge = pr.get("merged", False)

            if pr_action == "opened":
                record = {
                    "request_id": str(pr.get("id")),
                    "author": pr.get("user", {}).get("login", "unknown"),
                    "action": "PULL_REQUEST",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref"),
                    "timestamp": pr.get("created_at")
                }

            elif pr_action == "closed" and is_merge:
                record = {
                    "request_id": str(pr.get("id")),
                    "author": pr.get("user", {}).get("login", "unknown"),
                    "action": "MERGE",
                    "from_branch": pr.get("head", {}).get("ref"),
                    "to_branch": pr.get("base", {}).get("ref"),
                    "timestamp": pr.get("merged_at")
                }

        if record:
            collection.insert_one(record)
            # print("Stored in MongoDB:", record)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print("Webhook handling failed:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# API endpoint to fetch all events
@app.route("/api/events")
def get_events():
    try:
        raw_events = list(collection.find())
        print(f"RAW EVENTS COUNT: {len(raw_events)}")  # 👈 ADD THIS
        events = [{k: v for k, v in doc.items() if k != "_id"} for doc in raw_events]
        return jsonify(events)
    except Exception as e:
        print("Error in /api/events:", e)
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500 


# Start the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
