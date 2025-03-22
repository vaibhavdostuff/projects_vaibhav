from crewai import Agent, Crew
from database import cursor
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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

def get_sales_insights():
    sales_data = sales_fetcher.fetch_sales_data()
    return sales_analyzer.analyze_sales(sales_data)

