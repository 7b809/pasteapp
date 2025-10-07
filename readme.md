# Flask Paste App

This is a simple pastebin-style Flask app deployed on Vercel. You can create and view pastes using a web interface or directly via API endpoints.

**Deployed URL:** [https://pasteapp-sable.vercel.app](https://pasteapp-sable.vercel.app)

---

## Table of Contents

1. [Web Interface](#web-interface)
2. [API Endpoints](#api-endpoints)
   - [Upload JSON Content](#api-upload-json-content)
   - [Upload Raw Text](#api-upload-raw-text)
3. [Viewing a Paste](#viewing-a-paste)
4. [Paste Structure in Database](#paste-structure-in-database)
5. [Notes](#notes)
6. [Examples](#examples)

---

## Web Interface

### Create a Paste

- **URL:** `/`
- **Method:** `POST`
- **Form Parameter:**
  - `content` – The text you want to save.
- **Response:** Redirects to `/paste_key` page to view the paste.

### View a Paste

- **URL:** `/<paste_key>`
- **Method:** `GET`
- **Response:** HTML page showing the latest message of the paste.
- **Optional Form Parameter to Append Message:**
  - `content` – Additional text to append to the paste.

---

## API Endpoints

### 1. API: Upload JSON Content

- **URL:** `/api/upload`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body Parameters:**
```json
{
  "content": "Your text here"
}
