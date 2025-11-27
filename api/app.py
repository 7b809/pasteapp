# api/app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import uuid, os
from flask_cors import CORS
from cryptography.fernet import Fernet, InvalidToken

app = Flask(__name__)
CORS(app)

# ------------------ Encryption Setup ------------------
FERNET_KEY = os.getenv("ENCRYPT_KEY")

if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()
    print("⚠ WARNING: No ENCRYPT_KEY provided. Using EPHEMERAL key.")
else:
    FERNET_KEY = FERNET_KEY.encode()

fernet = Fernet(FERNET_KEY)

def encrypt_text(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    try:
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        raise InvalidToken("Invalid encryption key or corrupted data.")


# ------------------ MongoDB Connection ------------------
mongo_url = os.getenv("MONGO_URL")
client = MongoClient(mongo_url)
db = client["paste_db"]
pastes = db["pastes"]


# ------------------ Routes ------------------

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form.get("content")
        if content and content.strip():
            key = str(uuid.uuid4())[:8]
            enc = encrypt_text(content)
            pastes.insert_one({"key": key, "message_list": [enc]})
            return redirect(url_for("view_paste", key=key))
    return render_template("index.html")


@app.route("/api/get/<key>", methods=["GET"])
def api_get_paste(key):
    paste = pastes.find_one({"key": key})
    if not paste:
        return jsonify({"error": "Paste not found"}), 404

    try:
        encrypted = paste["message_list"][-1]
        decrypted = decrypt_text(encrypted)
        return jsonify({"content": decrypted})
    except InvalidToken:
        return jsonify({"error": "Decryption failed - invalid key or corrupted data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------ Updated View + Custom ID Logic ------------------
@app.route("/<key>", methods=["GET", "POST"])
def view_paste(key):
    paste = pastes.find_one({"key": key})

    # ---------- POST: Save or Update ----------
    if request.method == "POST":
        new_content = request.form.get("content")
        if new_content and new_content.strip():
            enc = encrypt_text(new_content)

            if paste:
                # Append version
                pastes.update_one({"key": key}, {"$push": {"message_list": enc}})
            else:
                # Create new paste with custom ID
                pastes.insert_one({"key": key, "message_list": [enc]})

            return redirect(url_for("view_paste", key=key))

    # ---------- GET: View existing or blank ----------
    latest_message = ""

    if paste:
        try:
            encrypted = paste["message_list"][-1]
            latest_message = decrypt_text(encrypted)
        except InvalidToken:
            latest_message = "[DECRYPTION FAILED: Wrong server encryption key]"
        except:
            latest_message = ""

    # If paste does not exist → user sees blank textarea and can create content
    return render_template("paste.html", key=key, content=latest_message)


# ----------- JSON Upload API -----------
@app.route("/api/upload", methods=["POST"])
def api_upload():
    data = request.get_json()
    content = data.get("content") if data else None

    if content and content.strip():
        key = str(uuid.uuid4())[:8]
        enc = encrypt_text(content)
        pastes.insert_one({"key": key, "message_list": [enc]})
        return jsonify({"status": "success", "key": key})

    return jsonify({"status": "error", "message": "No content provided"}), 400


# ----------- Raw Text Upload -----------
@app.route("/api/upload/raw", methods=["POST"])
def api_upload_raw():
    content = request.get_data(as_text=True)

    if content and content.strip():
        key = str(uuid.uuid4())[:8]
        enc = encrypt_text(content)
        pastes.insert_one({"key": key, "message_list": [enc]})
        return jsonify({"status": "success", "key": key})

    return jsonify({"status": "error", "message": "No content provided"}), 400


@app.route("/upload_batches")
def upload_batches_page():
    return render_template("upload_batches.html")


# ------------------ IMPORTANT ------------------
# ❌ DO NOT USE app.run() on Vercel
# ------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
