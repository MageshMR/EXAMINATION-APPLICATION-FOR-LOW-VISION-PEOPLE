let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        document.getElementById("status").innerText = "Recording...";
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const reader = new FileReader();
            reader.onload = function() {
                const base64data = reader.result;
                document.getElementById("voice_sample").value = base64data;
            };
            reader.readAsDataURL(audioBlob);
        };
    });
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById("status").innerText = "Recording stopped.";
}
