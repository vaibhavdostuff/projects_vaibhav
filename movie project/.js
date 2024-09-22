// Replace with your API key
const apiKey = 'b67c9c19';

// Open the database connection
let db;
const request = indexedDB.open('myDatabase', 1);
request.onupgradeneeded = (event) => {
    db = event.target.result;
    const objectStore = db.createObjectStore('movies', { keyPath: 'title' });
    objectStore.createIndex('title', 'title', { unique: true });
  };

  request.onsuccess = (event) => {
    db = event.target.result;
    console.log('Database connection established');
  
    // Add event listener after the database connection is established
    document.getElementById('searchButton').addEventListener('click', function(event) {
      event.preventDefault();
      const movieTitle = document.getElementById('movieInput').value.trim();

    if (movieTitle) {
      getMovieDataFromDB(movieTitle); // Call the function to retrieve movie data from the database
    } else {
      alert('Please enter a movie title.');
    }
  });
};

request.onerror = (event) => {
    console.error('Error opening database:', event.target.errorCode);
  };

// Function to get movie data from IndexedDB
const getMovieDataFromDB = (movieTitle) => {
    const transaction = db.transaction('movies', 'readonly');
    const movieStore = transaction.objectStore('movies');
    const index = movieStore.index('title');
    const request = index.get(movieTitle);

    request.onsuccess = (event) => {
        const movieData = event.target.result;
        if (movieData) {
          const imdbId = movieData.imdbID;
          const triviaUrl = `https://www.imdb.com/title/${imdbId}/trivia/`;
          window.location.href = triviaUrl;
        } else {
            // Movie not found in the database, make an API call to OMDB API
            fetch(`http://www.omdbapi.com/?t=${encodeURIComponent(movieTitle)}&apikey=${apiKey}`)
              .then(response => response.json())
              .then(data => {
                if (data.Response === "True") {
                  storeMovieData(data); // Store the movie data in the database
                  const imdbId = data.imdbID;
                  const triviaUrl = `https://www.imdb.com/title/${imdbId}/trivia/`;
                  window.location.href = triviaUrl;
                } else {
                    