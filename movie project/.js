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
  