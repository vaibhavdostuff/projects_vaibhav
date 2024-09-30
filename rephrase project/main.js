document.getElementById('paraphrase-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const sentence = document.getElementById('sentence').value;
    const resultDiv = document.getElementById('result');

    