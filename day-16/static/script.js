// static/script.js

document.addEventListener("DOMContentLoaded", async () => {
    // --- SESSION MANAGEMENT ---
    const urlParams = new URLSearchParams(window.location.search);
    let sessionId = urlParams.get('session_id');
    if (!sessionId) {
        sessionId = crypto.randomUUID();
        window.history.replaceState({}, '', `?session_id=${sessionId}`);
    }

    // --- WebSocket and Recording Logic ---
    let mediaRecorder = null;
    let isRecording = false;
    let socket = null;

    const recordBtn = document.getElementById("recordBtn");
    const statusDisplay = document.getElementById("statusDisplay");

    const startRecording = async () => {
        if (!navigator.mediaDevices?.getUserMedia) {
            alert("Audio recording not supported in this browser.");
            return;
        }

        isRecording = true;
        recordBtn.classList.add("recording");
        statusDisplay.textContent = "Recording... Press the button to stop.";

        // Establish WebSocket connection
        const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        socket = new WebSocket(`${wsProtocol}//${window.location.host}/ws`);

        socket.onopen = async () => {
            console.log("WebSocket connection established.");
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    audio: true
                });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
                        socket.send(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    if (socket.readyState === WebSocket.OPEN) {
                        socket.close();
                    }
                     // Stop the media stream tracks
                    stream.getTracks().forEach(track => track.stop());
                };
                
                // Start recording and send data every 200ms
                mediaRecorder.start(200);

            } catch (err) {
                console.error("Error accessing mic:", err);
                alert("Could not access microphone. Please check permissions.");
                isRecording = false;
                recordBtn.classList.remove("recording");
                statusDisplay.textContent = "Ready to chat!";
            }
        };
        
        socket.onclose = () => {
            console.log("WebSocket connection closed.");
        };
        
        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };
    };

    const stopRecording = () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            isRecording = false;
            recordBtn.classList.remove("recording");
            statusDisplay.textContent = "Recording stopped. Audio saved on server.";
        }
    };

    recordBtn.addEventListener("click", () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });
});