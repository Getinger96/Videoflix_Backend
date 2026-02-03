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

## 🎥 Video & Streaming

Method	Endpoint	Description
GET	/api/video/	List all available videos
GET	/api/video/<int:movie_id>/<str:resolution>/index.m3u8	HLS playlist for selected resolution
GET	/api/video/<int:movie_id>/<str:resolution>/<str:segment>/	Video segment

📌 Supported resolutions (example):
360p, 480p, 720p, 1080p

## ▶️ Video Streaming

Video playback is handled using HTTP Live Streaming (HLS):

The client requests the .m3u8 playlist

The playlist references multiple video segments

Segments are streamed sequentially

Adaptive bitrate streaming enables smooth playback

### Installation

1. Clone the repository:

```bash
git clone <repository_url>
```
1.5 Open the folder on your ide

2. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate   # Linux / macOS
env\Scripts\activate      # Windows
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```
### Running the Project
S
1. Apply migrations:

```bash
python manage.py migrate
```

2. Start the development server:

```bash
python manage.py runserver
```

🧪 Testing (Optional)
python manage.py test