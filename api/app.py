from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import uuid,os

app = Flask(__name__)

# MongoDB connection
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["paste_db"]
pastes = db["pastes"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content.strip():
            key = str(uuid.uuid4())[:8]  # generate unique key
            # create new document with message_list containing the first message
            pastes.insert_one({"key": key, "message_list": [content]})
            return redirect(url_for("view_paste", key=key))
    return render_template("index.html")

@app.route("/<key>", methods=["GET", "POST"])
def view_paste(key):
    paste = pastes.find_one({"key": key})
    
    if request.method == "POST":
        new_content = request.form.get("content")
        if new_content.strip():
            # append new message to message_list
            pastes.update_one({"key": key}, {"$push": {"message_list": new_content}})
            return redirect(url_for("view_paste", key=key))
    
    latest_message = paste["message_list"][-1] if paste else ""
    return render_template("paste.html", key=key, content=latest_message)
    
if __name__ == "__main__":
    app.run(debug=True)
