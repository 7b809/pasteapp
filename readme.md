# Flask Paste App - API & Usage Guide

This is a simple pastebin-style Flask app deployed on Vercel. You can create, view, and append text pastes using a web interface or API endpoints.

**Base URL:**  
https://pasteapp-sable.vercel.app

---

## 1. Web Interface

### 1.1 Create a Paste

- **URL:** `/`
- **Method:** `POST`
- **Form Parameter:**
  - `content` (string) – The text you want to save.
- **Response:** Redirects to `/<paste_key>` page to view the paste.

**Steps:**

1. Open your browser at `https://pasteapp-sable.vercel.app`.
2. Enter your text in the form.
3. Submit → You will be redirected to a unique URL like `https://pasteapp-sable.vercel.app/abc12345`.

---

### 1.2 View & Append Paste

- **URL:** `/<paste_key>`
- **Method:** `GET` (to view), `POST` (to append)
- **Form Parameter (optional to append):**
  - `content` – Additional text to append to the paste.
- **Response:** Shows the latest message and allows adding more text.

**Example URL:**  
https://pasteapp-sable.vercel.app/abc12345

---

## 2. API Endpoints

### 2.1 Upload JSON Content

- **URL:** `/api/upload`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "content": "Your text here"
}
```

- **Response (success):**
```json
{
  "status": "success",
  "key": "8-char-unique-key"
}
```
- **Response (error, missing content):**
```json
{
  "status": "error",
  "message": "No content provided"
}
```

**ThunderClient / Postman Steps:**

1. Set Method: POST
2. URL: `https://pasteapp-sable.vercel.app/api/upload`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "content": "Hello world from API!"
}
```
5. Send → Response will include `key`.

**Example curl command:**
```bash
curl -X POST https://pasteapp-sable.vercel.app/api/upload \
-H "Content-Type: application/json" \
-d '{"content":"Hello world!"}'
```

---

### 2.2 Upload Raw Text

- **URL:** `/api/upload/raw`
- **Method:** `POST`
- **Headers:** Optional: `Content-Type: text/plain`
- **Body:** Raw text only (no JSON)

- **Response (success):**
```json
{
  "status": "success",
  "key": "8-char-unique-key"
}
```
- **Response (error, empty body):**
```json
{
  "status": "error",
  "message": "No content provided"
}
```

**ThunderClient / Postman Steps:**

1. Set Method: POST
2. URL: `https://pasteapp-sable.vercel.app/api/upload/raw`
3. Headers: Optional: `Content-Type: text/plain`
4. Body (raw):
```
This is a raw text paste
```
5. Send → Response will include `key`.

**Example curl command:**
```bash
curl -X POST https://pasteapp-sable.vercel.app/api/upload/raw \
--data "This is a raw text paste"
```

---

## 3. Paste Data Structure

Each paste is stored in MongoDB like:

```json
{
  "key": "abc12345",
  "message_list": [
    "first message",
    "additional message 1",
    "additional message 2"
  ]
}
```

- `key` – Unique identifier for the paste.
- `message_list` – Array of all messages submitted for this paste.

---

## 4. Notes & Tips

1. Each paste key is **8 characters long**.
2. Web interface and API endpoints are interchangeable.
3. You can append messages multiple times using the same paste key.
4. Vercel’s filesystem is **read-only**, but MongoDB stores all pastes.
5. Use Postman or ThunderClient to easily test the endpoints with JSON or raw text.

---

## 5. Quick Reference Table

| Endpoint                 | Method | Body / Params        | Response                       | Notes                             |
|---------------------------|--------|-------------------|--------------------------------|----------------------------------|
| `/`                       | POST   | `content` (form)  | Redirect to `/<key>`           | Web form interface               |
| `/<key>`                  | GET    | -                 | Latest message HTML            | View paste                        |
| `/<key>`                  | POST   | `content` (form)  | Redirect to same `/<key>`      | Append message via web           |
| `/api/upload`             | POST   | JSON `{"content":"..."}` | JSON with `key`               | JSON API                         |
| `/api/upload/raw`         | POST   | Raw text          | JSON with `key`               | Raw text API                      |

---

Now you can quickly use the app through the web or API for storing and retrieving