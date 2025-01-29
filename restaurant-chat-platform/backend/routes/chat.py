from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal, redis_client
from ..models import ChatRoom
from ..websocket import ConnectionManager