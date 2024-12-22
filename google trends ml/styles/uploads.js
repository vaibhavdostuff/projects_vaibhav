document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput');
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('message').textContent = data.error;
        } else {
            document.getElementById('message').textContent = data.message;
            setTimeout(() => {
                window.location.href = '/questions';
            }, 1000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'An error occurred while uploading the file.';
    });
});
