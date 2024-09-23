from flask import Flask, request, jsonify
import csv
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Define the absolute path for the CSV file
file_path = 'C:\Users\Vaibhav Negi\OneDrive\Desktop\web scrapingmovie'  # Update this path

# Function to scrape movie data from IMDb
def scrape_movie_data(movie_title):
    search_url = f"https://www.imdb.com/find?q={movie_title.replace(' ', '+')}&s=tt&ttype=ft"
    