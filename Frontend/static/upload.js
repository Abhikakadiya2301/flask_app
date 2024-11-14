const form = document.getElementById('uploadForm');
        const progressBar = document.getElementById('progressBar');

        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(form);
            const xhr = new XMLHttpRequest();

            // Update the progress bar during upload
            xhr.upload.addEventListener('progress', function(event) {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    progressBar.style.width = percentComplete + '%';
                }
            });

            // Handle request completion
            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    alert('File uploaded successfully!');
                } else {
                    alert('File upload failed. Please try again.');
                }
            });

            // Set up the request
            xhr.open('POST', '/', true);

            // Send the form data
            xhr.send(formData);
        });