document.getElementById('paraphrase-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const sentence = document.getElementById('sentence').value;
    const resultDiv = document.getElementById('result');

    // Send sentence to the Flask backend
    try {
        const response = await fetch('/paraphrase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sentence }),
        });

        const data = await response.json();

        if (response.ok) {