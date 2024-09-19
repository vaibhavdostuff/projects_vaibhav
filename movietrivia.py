from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import csv
import os

app = Flask(__name__)

# Helper function to scrape IMDb and return results
def search_imdb(query):
    search_url = f"https://www.imdb.com/find?q={query}&s=tt"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

     results = []
    # IMDb search results are usually in 'td' tags with 'result_text' class
    for result in soup.find_all('td', class_='result_text'):
        link = result.find('a')
        if link:
            title = link.text.strip()
            imdb_id = link['href'].split('/')[2]  # Extract IMDb ID from the URL
            results.append({
                'title': title,
                'imdbID': imdb_id,
                'trivia_url': f"https://www.imdb.com/title/{imdb_id}/trivia/"
            })

    return results

# Helper function to save results to CSV
def save_to_csv(data):
   