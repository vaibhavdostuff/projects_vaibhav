const form = document.getElementById('paraphraseForm');
const loader = document.getElementById('loader');
const resultList = document.getElementById('resultList');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    resultList.innerHTML = '';
    loader.style.display = 'block';

    const text = document.getElementById('textInput').value;

    try {
        const response = await fetch('/api/paraphrase', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        loader.style.display = 'none';

        if (data.paraphrased_texts) {

            const labels = [
                "💼 Professional",
                "✨ Expressive",
                "💬 Casual"
            ];

            data.paraphrased_texts.forEach((item, index) => {
                const li = document.createElement('li');

                li.innerHTML = `<strong>${labels[index]}:</strong><br>${item}`;

                resultList.appendChild(li);
            });

        } else {
            alert(data.error);
        }

    } catch (error) {
        loader.style.display = 'none';
        alert("Something went wrong!");
    }
});