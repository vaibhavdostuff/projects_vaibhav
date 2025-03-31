import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

def collect_data():
    """Fetches data from a sample API and saves it as a CSV file."""
    print("🔄 Collecting data...")
    
    # Sample API (replace with real API)
    url = "https://api.example.com/data"
    
    try:
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data)
        df.to_csv("data/raw_data.csv", index=False)
        print("✅ Data collected and saved to data/raw_data.csv")
    except Exception as e:
        print(f"❌ Error in data collection: {e}")

