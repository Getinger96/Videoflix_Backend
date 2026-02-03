# 🎬 Videoflix

Videoflix is a modern **video streaming platform** that allows users to register, authenticate, and stream videos in multiple resolutions.  
Authentication is handled securely using **JWT (JSON Web Tokens)**.  
Video delivery is based on **HLS (HTTP Live Streaming)** using `.m3u8` playlists and segmented media files.

---

## 🚀 Features

- User registration and email-based account activation
- Secure JWT authentication (login, logout, token refresh)
- Password reset functionality
- Protected API endpoints
- Video streaming with multiple resolutions
- HLS streaming with segmented video delivery

---

## 🛠️ Tech Stack (Example)

- Backend: Django & Django REST Framework
- Authentication: JWT
- Streaming Protocol: HLS
- Database: PostgreSQL / SQLite (depending on environment)

---

## 🔐 Authentication

Videoflix uses **JWT-based authentication**.

- Access Token for authorized API requests
- Refresh Token to renew expired access tokens
- Protected endpoints require the following HTTP header:

```http
Authorization: Bearer <access_token>
```

## 🎥 Video & Streaming

Videoflix provides video playback using **HTTP Live Streaming (HLS)**.  
Videos are delivered via `.m3u8` playlists and segmented media files, allowing efficient and adaptive streaming.

### Available Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/video/` | Retrieve a list of all available videos |
| GET | `/api/video/<int:movie_id>/<str:resolution>/index.m3u8` | HLS playlist for the selected video and resolution |
| GET | `/api/video/<int:movie_id>/<str:resolution>/<str:segment>/` | Stream a specific video segment |

**Supported resolutions (example):**  
`360p`, `480p`, `720p`, `1080p`

---

## ▶️ Video Streaming Workflow

Video playback is handled using **HTTP Live Streaming (HLS)**:

1. The client requests the `.m3u8` playlist for a selected video and resolution  
2. The playlist contains references to multiple video segments  
3. Video segments are streamed sequentially  
4. Adaptive bitrate streaming ensures smooth playback based on network conditions  

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository_url>
```

### 2. Open the project in your IDE

Navigate into the project directory and open it using your preferred IDE  
(e.g. VS Code, PyCharm, IntelliJ).

---

### 3. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate    # Linux / macOS
env\Scripts\activate       # Windows
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

### 1. Apply database migrations

```bash
python manage.py migrate
```

### 2. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## 🧪 Testing (Optional)

Run the test suite using:

```bash
python manage.py test
```