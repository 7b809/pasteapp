from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import uuid, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
 
# MongoDB connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["paste_db"]
pastes = db["pastes"]
 
# ------------------ Existing Routes ------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content and content.strip():
            key = str(uuid.uuid4())[:8]  # generate unique key
            pastes.insert_one({"key": key, "message_list": [content]})
            return redirect(url_for("view_paste", key=key))
    return render_template("index.html")

@app.route("/api/get/<key>", methods=["GET"])
def api_get_paste(key):
    paste = pastes.find_one({"key": key})
    if not paste:
        return jsonify({"error": "Paste not found"}), 404
    
    latest_message = paste["message_list"][-1]
    return jsonify({"content": latest_message})


@app.route("/<key>", methods=["GET", "POST"])
def view_paste(key):
    paste = pastes.find_one({"key": key})
    
    if request.method == "POST":
        new_content = request.form.get("content")
        if new_content and new_content.strip():
            pastes.update_one({"key": key}, {"$push": {"message_list": new_content}})
            return redirect(url_for("view_paste", key=key))
    
    latest_message = paste["message_list"][-1] if paste else ""
    return render_template("paste.html", key=key, content=latest_message)

# ------------------ Existing API Route ------------------

@app.route("/api/upload", methods=["POST"])
def api_upload():
    """
    Accepts JSON payload:
    { "content": "<file content here>" }
    Stores it in MongoDB with a unique key.
    Returns the key as JSON.
    """
    data = request.get_json()
    content = data.get("content") if data else None
    
    if content and content.strip():
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [content]})
        return jsonify({"status": "success", "key": key})
    
    return jsonify({"status": "error", "message": "No content provided"}), 400

# ------------------ New API Route for Raw Body ------------------

@app.route("/api/upload/raw", methods=["POST"])
def api_upload_raw():
    """
    Accepts raw text in the request body.
    Stores it in MongoDB with a unique key.
    Returns the key as JSON.
    """
    content = request.get_data(as_text=True)
    
    if content and content.strip():
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [content]})
        return jsonify({"status": "success", "key": key})
    
    return jsonify({"status": "error", "message": "No content provided"}), 400

@app.route("/upload_batches")
def upload_batches_page():
    return render_template("upload_batches.html")

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)