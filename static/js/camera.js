let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let startButton = document.getElementById('startButton');
let captureButton = document.getElementById('captureButton');
let result = document.getElementById('result');
let stream = null;

startButton.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.play();
        startButton.disabled = true;
        captureButton.disabled = false;
    } catch (err) {
        showResult('Error accessing camera: ' + err.message, false);
    }
});

captureButton.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    const imageData = canvas.toDataURL('image/jpeg');
    
    fetch('/api/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image: imageData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showResult(`Attendance marked for: ${data.name}`, true);
        } else {
            showResult(data.message, false);
        }
    })
    .catch(error => {
        showResult('Error: ' + error.message, false);
    });
});

function showResult(message, success) {
    result.textContent = message;
    result.className = `alert ${success ? 'alert-success' : 'alert-danger'} mt-3`;
    result.style.display = 'block';
}

window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
