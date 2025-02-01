from fastapi import APIRouter, Depends, HTTPException
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


@router.post("/place-order")
def place_order(user_email: str, order_details: dict, db: Session = Depends(get_db)):
    """
    Places a food order for a user.
    """
    # Ensure user exists
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "Order placed successfully", "order_details": order_details}
