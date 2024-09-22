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
