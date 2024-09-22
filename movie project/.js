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
                    alert('Movie not found. Please try another title.');
          }
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          alert('An error occurred. Please try again later.');
        });
    }
  };
  request.onerror = (event) => {
    console.error('Error fetching data from database:', event.target.error);
  };
};

// Function to store movie data in IndexedDB
const storeMovieData = (data) => {
    const transaction = db.transaction('movies', 'readwrite');
    const movieStore = transaction.objectStore('movies');

    // Ensure the data has a 'title' property with fallback values for undefined fields
    const movieData = {
        title: data.Title || "Unknown Title",  // Fallback to "Unknown Title" if not available
        imdbID: data.imdbID || "N/A",          // Fallback to "N/A" if imdbID is missing
        year: data.Year || "Unknown Year",     // Fallback to "Unknown Year" if year is missing
        genre: data.Genre || "Unknown Genre",  // Fallback to "Unknown Genre" if genre is missing
        director: data.Director || "Unknown Director"  // Fallback to "Unknown Director" if director is missing
      };
      // Log the movie data being added for easier debugging
    console.log('Storing movie data:', movieData);
  
    const addRequest = movieStore.add(movieData);
  
    addRequest.onsuccess = () => {
      console.log('Movie data stored successfully');
    };
    
  };

  // Function to send movie data to Python (Flask)  
const saveMovieToCSV = (data) => {
    fetch('http://127.0.0.1:5000/save_movie', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        Title: data.Title,
        Year: data.Year,
        Genre: data.Genre,
        Director: data.Director
      })
    })
    