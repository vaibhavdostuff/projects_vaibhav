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

# Route to get all sales data
@app.get("/sales/")
def get_sales():
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    return {"sales": sales}

# OpenAI API Key (for LLM insights)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route for AI Sales Insights
@app.post("/sales-insights/")
def sales_insights(query: dict):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query["question"]}]
    )
    return {"insight": response["choices"][0]["message"]["content"]}

# CrewAI Agent Setup
class SalesFetcher(Agent):
    def fetch_sales_data(self):
        cursor.execute("SELECT * FROM sales")
        return cursor.fetchall()

class SalesAnalyzer(Agent):
    def analyze_sales(self, sales_data):
        prompt = f"Analyze the following sales data and provide insights: {sales_data}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

sales_fetcher = SalesFetcher()
sales_analyzer = SalesAnalyzer()

crew = Crew(agents=[sales_fetcher, sales_analyzer])

@app.get("/crewai-sales-insights/")
def crewai_sales_insights():
    sales_data = sales_fetcher.fetch_sales_data()
    insights = sales_analyzer.analyze_sales(sales_data)
    return {"crewai_insight": insights}

# Run FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)