document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');
    const progressContainer = document.querySelector('.progress-container');
    const progressBar = document.querySelector('.progress-bar');
    const progressText = document.querySelector('.progress-text');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        resultDiv.innerHTML = '';
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        progressText.textContent = '0%';
        
        // Simulate progress during compression
        let progress = 0;
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += Math.random() * 10;
                progressBar.style.width = `${Math.min(progress, 90)}%`;
                progressText.textContent = `${Math.round(Math.min(progress, 90))}%`;
            }
        }, 200);
        
        fetch('/compress', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            clearInterval(progressInterval);
            progressBar.style.width = '100%';
            progressText.textContent = '100%';
            
            setTimeout(() => {
                progressContainer.style.display = 'none';
                if (data.success) {
                    resultDiv.innerHTML = `
                        <p>Compressed Image Size: ${data.size} MB</p>
                        <p><a href="${data.output_path}" download class="download-link">Download Compressed Image</a></p>
                    `;
                } else {
                    resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
                }
            }, 500);
        })
        .catch(error => {
            clearInterval(progressInterval);
            progressContainer.style.display = 'none';
            resultDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
            console.error('Error:', error);
        });
    });

    // Hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});