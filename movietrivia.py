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

    