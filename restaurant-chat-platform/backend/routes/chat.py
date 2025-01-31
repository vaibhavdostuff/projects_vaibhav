from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, redis_client
from ..models import ChatRoom
from ..websocket import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-room")
def create_chat_room(table_number: int, db: Session = Depends(get_db)):
    """
    Creates a chat room for the specified table.
    """
    chat_room = ChatRoom(table_number=table_number, qr_code=f"/join/{table_number}")
    db.add(chat_room)
    db.commit()
    db.refresh(chat_room)
    return {"message": "Chat room created", "chat_room": chat_room.qr_code}

@router.websocket("/ws/{room_id}")
async def chat_room_ws(websocket: WebSocket, room_id: int):
    """
    WebSocket endpoint for real-time chat communication.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the message to all clients
            await manager.broadcast(f"Room {room_id}: {data}")
    except Exception:
        await manager.disconnect(websocket)
        raise HTTPException(status_code=400, detail="Disconnected")

        