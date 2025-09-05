# 💬 Real-Time Chat Application

This is a full-stack real-time chat application built with:

- ⚙️ **Backend**: FastAPI, MongoDB, Redis, WebSocket
- 💻 **Frontend**: React, Redux, TypeScript, Tailwind CSS

---

## 📁 Project Structure

```
message-app/
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── websocket.py
│   ├── redispool.py
│   └── 
└── frontend/
    ├── src/
    │   ├── apiInterface/
    │   ├── components/
    │   ├── pages/
    │   ├── store/
    │   └── App.tsx
    └── 
```
## 🚀 Features

- ✅ User Authentication (Signup / Login)
- 🔐 Session handling with `sessionStorage` & `Redux`
- 💬 Real-time messaging using WebSockets
- 📁 MongoDB for persistent chat storage
- ⚡ Redis for fast context and temporary storage
- 🌍 Secure HTTPS with NGINX + Let's Encrypt
- 🧩 Scalable and modular architecture
- 🖥️ UI powered by React + Vite
---

## 🚀 Backend Flow (FastAPI)

### ✅ 1. **Authentication**
- `/api/register`: Register a user (returns JWT token and user info).
- `/api/login`: Login with email and password.
- `/api/me`: Authenticated route to fetch current user based on token.

### ✅ 2. **Chat Management**
- `/api/chats`: Fetch or create chat rooms between users.
- `/api/messages/{room_id}`: Fetch messages for a specific chat room.

### ✅ 3. **WebSocket (Real-Time Messaging)**
- `/ws/{user_id}`: WebSocket connection per logged-in user.
- Client sends:
  ```json
  {
    "room_id": "abc123",
    "sender_id": "user1",
    "message": "Hello!"
  }
  ```
- Server:
  - Saves message to MongoDB.
  - Broadcasts to all active connections using `ConnectionManager`.

---

## 🖥️ Frontend Flow (React + Redux)

### ✅ 1. **Authentication**
- `SignUp` / `Login` components send user data to backend.
- On success:
  - JWT and user data are stored in `sessionStorage`.
  - Redux state is updated with `authtoken`, `userData`.

### ✅ 2. **Homepage (`/`)**
- Shows sidebar (`ChatSidebar`) with all users.
- Click on user creates a chat room.
- Existing chat rooms are listed on right.
- Click on room → opens `ChatRoom` component.

### ✅ 3. **ChatRoom**
- Fetches past messages via REST API (`/api/messages/{room_id}`).
- Establishes WebSocket connection to `/ws/{user_id}`.
- Messages sent through WebSocket.
- Incoming messages are added to state and displayed in real-time.

---

## 🧪 Development

### 📦 Backend (FastAPI)

```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 9010 --reload
```

- MongoDB must be running at `mongodb://admin:admin@localhost:27017`
- Redis must be running and accessible from `redispool.py`

### 📦 Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

> Make sure `.env` or config points `VITE_API_BASE_URL` to the backend (`http://localhost:9010` or domain).

---

## 🔐 Production Setup (Optional)

### 🧰 Systemd Service (Backend)

```ini
# /etc/systemd/system/message-app.service

[Unit]
Description=Message App Backend
After=network.target

[Service]
User=root
WorkingDirectory=/opt/message-app/backend/
ExecStart=/opt/message-app/backend/env/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 🔒 SSL with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d messaging.vsystech.net
```

---

## 🔄 Future Improvements

- ✅ Pagination or infinite scroll for messages.
- ✅ User status (online/offline).
- ✅ File/image sharing.
- ✅ Read receipts.

---

## 🧠 Author

Made with ❤️ by [Vishnuvardhan Venkannagari](https://github.com/Vishnuvardhan-Venkannagari)

---
