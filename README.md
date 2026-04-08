# RoomieMatch Pro 🏠
**RoomieMatch Pro** is an intelligent, modern roommate matching platform designed to help people find their perfect living partners based on lifestyle, personality, and AI-driven compatibility analysis.

This project was built for **Project Exhibition - II 2026**.

## 🚀 Key Features
- **AI-Driven Matching**: Leverages Gemini 1.5/Gwen models (via OpenRouter) to go beyond keyword matching and understand true lifestyle compatibility.
- **One-Click Google Sign-In**: Secure and seamless authentication powered by Firebase.
- **Tinder-Style Discovery**: A beautiful, gesture-oriented interface for swiping through potential roommate matches.
- **Real-Time Compatibility Scores**: Instant feedback on how well you would live with another person.
- **Integrated Chat**: Community forums and private messaging to coordinate with matches.
- **Automated Agreements**: Generate and download roommate agreements instantly.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite (In-Memory for Vercel, Physical for Local) with SQLAlchemy ORM
- **AI**: OpenRouter API (Gemini / Gwen models)
- **Auth**: Firebase Google Sign-In
- **Frontend**: Modern Vanilla JS, HTML5, CSS3 (Rich aesthetics with glassmorphism and animations)

## 💻 Local Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python -m uvicorn server_app.app:app --reload
   ```

3. **Access the Site**:
   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🌐 Vercel Deployment

This project is optimized for Vercel Serverless deployment. 

1. **Environment Variables**:
   Add the following variables to your Vercel Dashboard:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key for AI matching.

2. **Consolidated Architecture**:
   The application uses a unified Python deployment model. The frontend is served directly through the FastAPI instance for maximum stability.

---
*Developed for Project Exhibition - II 2026*
