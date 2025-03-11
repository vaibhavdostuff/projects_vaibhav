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

# Create table for sample sales data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        product_name TEXT,
        sales_amount FLOAT,
        date TIMESTAMP
    );
''')
conn.commit()

# Pydantic model for Sales Data
class Sale(BaseModel):
    product_name: str
    sales_amount: float
    date: str  # ISO format

# Route to insert sample data
@app.post("/sales/")
def add_sale(sale: Sale):
    cursor.execute("INSERT INTO sales (product_name, sales_amount, date) VALUES (%s, %s, %s)", 
                   (sale.product_name, sale.sales_amount, sale.date))
    conn.commit()
    return {"message": "Sale record added"}