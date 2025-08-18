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
    let audioContext = null;
    let source = null;
    let processor = null;
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
        statusDisplay.textContent = "Streaming audio... Press the button to stop.";

        try {
            // Establish WebSocket connection
            const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
            socket = new WebSocket(`${wsProtocol}//${window.location.host}/ws`);

            socket.onopen = async () => {
                console.log("WebSocket connection established for streaming transcription.");
                statusDisplay.textContent = "Connected. Speaking...";

                try {
                    // Get microphone access
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    
                    // Create AudioContext with 16kHz sample rate (required by AssemblyAI)
                    audioContext = new (window.AudioContext || window.webkitAudioContext)({ 
                        sampleRate: 16000 
                    });
                    
                    source = audioContext.createMediaStreamSource(stream);
                    
                    // Create ScriptProcessorNode for processing audio chunks
                    processor = audioContext.createScriptProcessor(4096, 1, 1); // Mono, 4096 buffer size

                    processor.onaudioprocess = (event) => {
                        const inputData = event.inputBuffer.getChannelData(0);
                        
                        // Convert float32 (-1.0 to 1.0) to 16-bit PCM
                        const pcmData = new Int16Array(inputData.length);
                        for (let i = 0; i < inputData.length; i++) {
                            const sample = Math.max(-1, Math.min(1, inputData[i]));
                            pcmData[i] = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
                        }
                        
                        // Send PCM data to server if WebSocket is open
                        if (socket && socket.readyState === WebSocket.OPEN) {
                            console.log(`Sending PCM chunk of size: ${pcmData.buffer.byteLength} bytes`);
                            socket.send(pcmData.buffer);
                        }
                    };

                    // Connect the audio nodes
                    source.connect(processor);
                    processor.connect(audioContext.destination);

                    // Store the stream for cleanup
                    recordBtn.mediaStream = stream;

                } catch (micError) {
                    console.error("Error accessing microphone:", micError);
                    alert("Could not access microphone. Please check permissions.");
                    stopRecording();
                }
            };

            socket.onclose = () => {
                console.log("WebSocket connection closed.");
                statusDisplay.textContent = "Transcription session ended.";
            };

            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
                statusDisplay.textContent = "Connection error occurred.";
            };

        } catch (err) {
            console.error("Error starting recording:", err);
            alert("Failed to start recording session.");
            stopRecording();
        }
    };

    const stopRecording = () => {
        if (!isRecording) return;

        isRecording = false;
        recordBtn.classList.remove("recording");
        statusDisplay.textContent = "Stopping recording...";

        // Clean up audio processing
        if (processor) {
            processor.disconnect();
            processor = null;
        }
        
        if (source) {
            source.disconnect();
            source = null;
        }
        
        if (audioContext) {
            audioContext.close();
            audioContext = null;
        }

        // Stop media stream tracks
        if (recordBtn.mediaStream) {
            recordBtn.mediaStream.getTracks().forEach(track => track.stop());
            recordBtn.mediaStream = null;
        }

        // Send EOF and close WebSocket
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send("EOF");
            socket.close();
        }
        socket = null;

        statusDisplay.textContent = "Ready to chat!";
    };

    recordBtn.addEventListener("click", () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });

    // Clean up on page unload
    window.addEventListener('beforeunload', () => {
        if (isRecording) {
            stopRecording();
        }
    });
});