from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import uuid, os

app = Flask(__name__)

# MongoDB connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["paste_db"]
pastes = db["pastes"]

# Simple reversible "encryption" using key
def encrypt(content, key):
    # Add key as simple salt and reverse
    return (content + key)[::-1]

def decrypt(content, key):
    # Reverse and remove key suffix
    return content[::-1][:-len(key)]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            key = str(uuid.uuid4())[:8]  # generate unique key
            encrypted_content = encrypt(content, key)
            # Save encrypted content
            pastes.insert_one({"key": key, "message_list": [encrypted_content]})
            return redirect(url_for("view_paste", key=key))
    return render_template("index.html")

@app.route("/<key>", methods=["GET", "POST"])
def view_paste(key):
    paste = pastes.find_one({"key": key})
    
    if request.method == "POST":
        new_content = request.form.get("content", "").strip()
        if new_content:
            encrypted_content = encrypt(new_content, key)
            pastes.update_one({"key": key}, {"$push": {"message_list": encrypted_content}})
            return redirect(url_for("view_paste", key=key))
    
    if paste:
        latest_encrypted = paste["message_list"][-1]
        latest_message = decrypt(latest_encrypted, key)
    else:
        latest_message = ""

    return render_template("paste.html", key=key, content=latest_message)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
