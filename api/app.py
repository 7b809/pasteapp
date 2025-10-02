from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import uuid, os

app = Flask(__name__)

# ------------------ MongoDB Connection ------------------
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["paste_db"]
pastes = db["pastes"]

# ------------------ Web Routes ------------------

@app.route("/", methods=["GET", "POST"], endpoint="index_endpoint")
def index_func():
    if request.method == "POST":
        content = request.form.get("content")
        if content and content.strip():
            key = str(uuid.uuid4())[:8]  # generate unique key
            pastes.insert_one({"key": key, "message_list": [content]})
            return redirect(url_for("view_paste_endpoint", key=key))
    return render_template("index.html")

@app.route("/<key>", methods=["GET", "POST"], endpoint="view_paste_endpoint")
def view_paste_func(key):
    paste = pastes.find_one({"key": key})
    
    if request.method == "POST":
        new_content = request.form.get("content")
        if new_content and new_content.strip():
            pastes.update_one({"key": key}, {"$push": {"message_list": new_content}})
            return redirect(url_for("view_paste_endpoint", key=key))
    
    latest_message = paste["message_list"][-1] if paste else ""
    return render_template("paste.html", key=key, content=latest_message)

# ------------------ API Routes ------------------

@app.route("/api/upload", methods=["POST"], endpoint="api_upload_json_endpoint")
def api_upload_func():
    """
    Accepts JSON payload:
    { "content": "<file content here>" }
    Stores it in MongoDB with a unique key.
    """
    data = request.get_json()
    content = data.get("content") if data else None
    
    if content and content.strip():
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [content]})
        return jsonify({"status": "success", "key": key})
    
    return jsonify({"status": "error", "message": "No content provided"}), 400

@app.route("/api/upload_raw", methods=["POST"], endpoint="api_upload_raw_endpoint")
def api_upload_raw_func():
    """
    Accepts raw text in body (Content-Type: text/plain).
    Stores it in MongoDB with a unique key.
    """
    raw_content = request.data.decode("utf-8").strip() if request.data else None

    if raw_content:
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [raw_content]})
        return jsonify({"status": "success", "key": key})

    return jsonify({"status": "error", "message": "No raw content provided"}), 400

@app.route("/api/get/<key>", methods=["GET"], endpoint="api_get_endpoint")
def api_get_func(key):
    """
    Returns the paste data as JSON.
    """
    paste = pastes.find_one({"key": key})
    if paste:
        return jsonify({"status": "success", "key": key, "messages": paste["message_list"]})
    return jsonify({"status": "error", "message": "Paste not found"}), 404

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)

# ------------------ API Routes ------------------

@app.route("/api/upload", methods=["POST"], endpoint="api_upload_json")
def api_upload():
    """
    Accepts JSON payload:
    { "content": "<file content here>" }
    """
    data = request.get_json()
    content = data.get("content") if data else None
    
    if content and content.strip():
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [content]})
        return jsonify({"status": "success", "key": key})
    
    return jsonify({"status": "error", "message": "No content provided"}), 400


@app.route("/api/upload_raw", methods=["POST"], endpoint="api_upload_raw")
def api_upload_raw():
    """
    Accepts raw text in body (Content-Type: text/plain).
    """
    raw_content = request.data.decode("utf-8").strip() if request.data else None

    if raw_content:
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [raw_content]})
        return jsonify({"status": "success", "key": key})

    return jsonify({"status": "error", "message": "No raw content provided"}), 400


@app.route("/api/get/<key>", methods=["GET"], endpoint="api_get")
def api_get(key):
    """
    Returns the paste data as JSON.
    """
    paste = pastes.find_one({"key": key})
    if paste:
        return jsonify({"status": "success", "key": key, "messages": paste["message_list"]})
    return jsonify({"status": "error", "message": "Paste not found"}), 404

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)

# ------------------ API Routes ------------------

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


@app.route("/api/upload_raw", methods=["POST"])
def api_upload_raw():
    """
    Accepts raw text in body (Content-Type: text/plain).
    Stores it in MongoDB with a unique key.
    Returns the key as JSON.
    """
    raw_content = request.data.decode("utf-8").strip() if request.data else None

    if raw_content:
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [raw_content]})
        return jsonify({"status": "success", "key": key})

    return jsonify({"status": "error", "message": "No raw content provided"}), 400


@app.route("/api/get/<key>", methods=["GET"])
def api_get(key):
    """
    Returns the paste data as JSON.
    Example response:
    { "key": "abcd1234", "messages": ["first msg", "second msg"] }
    """
    paste = pastes.find_one({"key": key})
    if paste:
        return jsonify({"status": "success", "key": key, "messages": paste["message_list"]})
    return jsonify({"status": "error", "message": "Paste not found"}), 404

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)

# ------------------ API Routes ------------------

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


@app.route("/api/upload_raw", methods=["POST"])
def api_upload_raw():
    """
    Accepts raw text in body (Content-Type: text/plain).
    Stores it in MongoDB with a unique key.
    Returns the key as JSON.
    """
    raw_content = request.data.decode("utf-8").strip() if request.data else None

    if raw_content:
        key = str(uuid.uuid4())[:8]
        pastes.insert_one({"key": key, "message_list": [raw_content]})
        return jsonify({"status": "success", "key": key})

    return jsonify({"status": "error", "message": "No raw content provided"}), 400

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)

# ------------------ New API Route ------------------

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

# ------------------ Run App ------------------

if __name__ == "__main__":
    app.run(debug=True)
