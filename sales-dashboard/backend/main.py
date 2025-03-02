from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
import openai
from dotenv import load_dotenv
from crewai import Agent, Crew

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Database Connection (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
