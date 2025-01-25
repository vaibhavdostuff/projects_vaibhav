from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

DATABASE_URL = "postgresql://user:password@localhost/restaurant_chat"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Redis for real-time chat storage
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)
