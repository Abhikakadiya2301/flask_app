document.getElementById('upload-form').addEventListener('submit', function (e) {
    e.preventDefault();

    var fileInput = document.getElementById('file-input');
    var messageBox = document.getElementById('message-box');

    if (fileInput.files.length === 0) {
        showMessage('Please select a file to upload.', 'error');
        return;
    }

    showMessage('Uploading file...', 'info');

    var formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'error');
        } else {
            showMessage(data.message, 'success');
        }
    })
    .catch(error => {
        showMessage('Error uploading file: ' + error.message, 'error');
    });
});

function showMessage(message, type) {
    var messageBox = document.getElementById('message-box');
    messageBox.textContent = message;
    messageBox.className = type;
    messageBox.style.display = 'block';
}
