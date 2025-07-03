# GitHub Webhook Listener Project

This is a Flask-based backend application that listens for GitHub webhook events. It captures `push`, `pull_request`, and `merge` events and stores them in a MongoDB database. It also has a basic frontend UI to view the received events in real-time.

---

## Project Structure

```
webhook-repo/
├── app.py                  # Main Flask backend
├── requirements.txt        # Python dependencies
├── static/
│   └── app.js              # Frontend JavaScript (fetches events)
├── templates/
│   └── index.html          # Frontend HTML UI
```

---

## Features

- Receives GitHub webhook events (`push`, `pull_request`, `merge`)
- Stores them in MongoDB
- Shows formatted events in browser
- Auto-refreshes every 15 seconds
- Timestamp formatted as readable UTC time

---

## How to Set Up and Run

### 1. Clone this repository

You can either download it as a ZIP or clone from GitHub (if it's uploaded there):

```
git clone https://github.com/BLITzZ0/webhook-repo.git
cd webhook-repo
```

### 2. Create a virtual environment (recommended)

This keeps your dependencies isolated.

```
python -m venv venv
```

Activate it:

- On Windows:
```
venv\Scripts\activate
```

### 3. Install required packages

```
pip install -r requirements.txt
```

### 4. Connect to MongoDB

This app uses MongoDB Atlas (cloud) by default.

In `app.py`, make sure this line has your correct connection string:

```python
client = MongoClient("your_mongodb_connection_string")
```

If you’re using MongoDB Compass locally, adjust it to:

```python
client = MongoClient("mongodb://localhost:27017/")
```

Make sure the database name is `github_events` and collection is `events` .

### 5. Run the Flask app

```
python app.py
```

It will start at:

```
http://localhost:5000
```

You can now visit the frontend at that address.

---

## GitHub Webhook Configuration

### 1. Create a GitHub Repository

You can use any dummy repo (`action-repo`) for testing.

### 2. Expose your Flask server using Ngrok

Since Flask runs locally, use Ngrok to expose it to the internet:

```
ngrok http 5000
```

Copy the HTTPS URL from Ngrok (example: `https://1234abcd.ngrok.io`)

### 3. Set up the Webhook on GitHub

1. Go to your `action-repo` on GitHub
2. Click on **Settings > Webhooks > Add webhook**
3. Payload URL: `https://your-ngrok-url/webhook`
4. Content type: `application/json`
5. Select events:
   - Just `push`
   - `pull_request`
   - Or all events (optional)
6. Click **Add webhook**

### 4. Trigger Events

- Make a push to `main` or `feature-branch`
- Create and merge pull requests

These actions should trigger the webhook and insert event data into MongoDB.

---

## Viewing Events

Open:

```
http://localhost:5000
```

You will see a list of recent events with messages like:

- "BLITzZ0" pushed to "feature-branch" on 3rd July 2025 - 8:06 AM UTC
- "BLITzZ0" merged branch "feature-branch" to "main" on 3rd July 2025 - 8:07 AM UTC
- "BLITzZ0" submitted a pull request from "feature-branch" to "main" on 3rd July 2025 - 8:06 AM UTC

It auto-refreshes every 15 seconds.

---

## API Endpoint

You can fetch all events (in JSON) using:

```
GET /api/events
```

---

## Optional Testing

To quickly test DB connection, open:

```
http://localhost:5000/test-db
```

It will insert a test event into MongoDB.

---

## Notes

- Merge events are optional, but included in this version.
- Make sure Ngrok is running whenever you test webhook triggers.
- Don’t forget to activate your virtual environment every time you work on this.

---

## Troubleshooting

- If events don’t show up:
  - Check the `Flask` console for `Webhook Received`
  - Check MongoDB Compass if documents are added
  - Verify Ngrok URL and webhook endpoint match
  - Make sure GitHub push or PR is actually happening

---

## Author

This project is built for the GitHub Webhook Developer Assessment (TechStaX / similar).
