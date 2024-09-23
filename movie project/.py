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
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scrape the first search result from IMDb
    result = soup.find('td', class_='result_text')
    if result:
        # Extract movie title link and navigate to the movie page
        movie_link = "https://www.imdb.com" + result.a['href']
        movie_page = requests.get(movie_link)
        movie_soup = BeautifulSoup(movie_page.text, 'html.parser')

        # Extract relevant details (Title, Year, Genre, Director)
        title = movie_soup.find('h1').text.strip()
        year = movie_soup.find('span', id='titleYear').text.strip('()') if movie_soup.find('span', id='titleYear') else "N/A"
        genres = [g.text for g in movie_soup.findAll('span', class_='genre')] or ["N/A"]
        director = movie_soup.find('a', href=lambda x: x and x.startswith('/name/')).text if movie_soup.find('a', href=lambda x: x and x.startswith('/name/')) else "N/A"

        return {
            'Title': title,
            'Year': year,
            'Genre': ', '.join(genres),
            'Director': director
        }
    else:
        return None

