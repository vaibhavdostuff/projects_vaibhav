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

    try:
        decoded_token = firebase_auth.verify_id_token(token)
        email = decoded_token.get("email")
        name = decoded_token.get("name")

        # Check if the user already exists
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Add new user to the database
            user = User(name=name, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)

        return {"message": "User logged in", "user": {"name": name, "email": email}}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

        