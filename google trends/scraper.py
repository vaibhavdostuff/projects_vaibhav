from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta
import os


def scrape_google_trends(keywords, timeframe='today 3-m'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
    
    data = pytrends.interest_over_time()
    return data


def save_data(data, filename):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    filepath = os.path.join('data', filename)
    data.to_csv(filepath)
    print(f"Data saved to {filepath}")


if __name__ == "__main__":
    keywords = ['python', 'javascript', 'java']
    data = scrape_google_trends(keywords)

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"google_trends_{timestamp}.csv"
    
    save_data(data, filename)

