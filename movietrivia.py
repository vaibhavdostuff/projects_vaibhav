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
   file_exists = os.path.isfile('search_results.csv')
    with open('search_results.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Title', 'IMDb ID', 'Trivia URL']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
           writer.writeheader()  # Write header only once
        for item in data:
            writer.writerow({
                'Title': item['title'],
                'IMDb ID': item['imdbID'],
                'Trivia URL': item['trivia_url']
            })

# Search route
@app.route('/search', methods=['GET'])
def search():
   query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required.'}), 400

    try:
      results = search_imdb(query)
        if results:
            save_to_csv(results)  # Save results to CSV
            return jsonify({'results': results})
        else:
         return jsonify({'error': 'No results found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve HTML page
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
