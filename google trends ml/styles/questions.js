document.getElementById('questionForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const question = document.getElementById('queryInput').value.trim();
    const column = document.getElementById('columnSelect').value;

    if (!question || !column) {
        alert('Please select a column and enter a question.');
        return;
    }

    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question, column: column })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else if (data.plot) {
                sessionStorage.setItem('queryResult', JSON.stringify(data));
                window.location.href = `/results/${data.plot}`;
            } else {
                document.getElementById('response').textContent = data.message || 'No results available.';
            }
        })
        .catch(err => {
            console.error('Error:', err);
            document.getElementById('response').textContent = 'An error occurred while processing your question.';
        });
});
