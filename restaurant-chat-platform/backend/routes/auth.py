from fastapi import APIRouter, HTTPException, Depends
from firebase_admin import auth as firebase_auth
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login_user(token: str, db: Session = Depends(get_db)):
    """
    Logs in the user using Firebase ID token.
    """