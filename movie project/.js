const apiKey = ' 9c8791f0'; // Replace with your API keyp

document.getElementById('searchButton').addEventListener('click', function(event) {
    event.preventDefault();
    const movieTitle = document.getElementById('movieInput').value.trim();
    
    if (movieTitle) {
        fetch('http://www.omdbapi.com/?t=${encodeURIComponent(movieTitle)}&apikey=${apiKey}')
            .then(response => response.json())
            .then(data => { 
                if (data.Response === "True") {
                    const imdbId = data.imdbID;
                    const triviaUrl = 'https://www.imdb.com/title/${imdbId}/trivia/';
                    window.location.href = triviaUrl;
                } else {
                    alert('Movie not found. Please try another title.');
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                alert('An error occurred. Please try again later.');
            });
    } else {
        alert('Please enter a movie title.');
    }
});
