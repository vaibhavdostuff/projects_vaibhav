document.addEventListener('DOMContentLoaded', function() {
    var result = JSON.parse(sessionStorage.getItem('queryResult'));
    var resultTextElement = document.getElementById('resultText');
    var resultPlotElement = document.getElementById('resultPlot');

    if (result.error) {
        resultTextElement.textContent = 'Error: ' + result.error;
    } else if (result.plot) {
        resultTextElement.textContent = result.message;
        resultPlotElement.src = '/plot/' + result.plot;
        resultPlotElement.style.display = 'block';
    } else {
        resultTextElement.textContent = JSON.stringify(result, null, 2);
    }

    document.getElementById('newQuestion').addEventListener('click', function() {
        window.location.href = '/questions';
    });

    document.getElementById('newFile').addEventListener('click', function() {
        window.location.href = '/';
    });
});

