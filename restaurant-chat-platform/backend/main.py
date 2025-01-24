from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import auth, chat
import firebase_admin
from firebase_admin import auth as firebase_auth

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def health_check():
    return {"message": "Restaurant Chat API is running"}

