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
    let audioContext = null;
    let processor = null;

    const recordBtn = document.getElementById("recordBtn");
    const statusDisplay = document.getElementById("statusDisplay");
    const transcriptionDisplay = document.getElementById("transcriptionDisplay");

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
                    audio: {
                        sampleRate: 16000,
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true
                    }
                });

                // Create AudioContext for processing audio to PCM format
                audioContext = new AudioContext({ sampleRate: 16000 });
                const source = audioContext.createMediaStreamSource(stream);
                
                // Create ScriptProcessorNode for audio processing
                processor = audioContext.createScriptProcessor(4096, 1, 1);
                
                processor.onaudioprocess = (event) => {
                    if (socket && socket.readyState === WebSocket.OPEN) {
                        const inputData = event.inputBuffer.getChannelData(0);
                        
                        // Convert float32 audio data to 16-bit PCM
                        const pcmData = new Int16Array(inputData.length);
                        for (let i = 0; i < inputData.length; i++) {
                            // Clamp the value to prevent distortion
                            const sample = Math.max(-1, Math.min(1, inputData[i]));
                            pcmData[i] = sample * 32767;
                        }
                        
                        // Send PCM data as bytes
                        socket.send(pcmData.buffer);
                    }
                };
                
                // Connect the audio processing chain
                source.connect(processor);
                processor.connect(audioContext.destination);

            } catch (err) {
                console.error("Error accessing mic:", err);
                alert("Could not access microphone. Please check permissions.");
                isRecording = false;
                recordBtn.classList.remove("recording");
                statusDisplay.textContent = "Ready to chat!";
            }
        };

        socket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                
                if (message.type === "transcription") {
                    // Display transcription in console and UI
                    console.log("Transcription:", message.text);
                    
                    if (transcriptionDisplay) {
                        transcriptionDisplay.textContent = message.text;
                        transcriptionDisplay.style.display = "block";
                    }
                } else if (message.type === "error") {
                    console.error("Transcription error:", message.message);
                    statusDisplay.textContent = `Error: ${message.message}`;
                }
            } catch (err) {
                console.error("Error parsing WebSocket message:", err);
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
        if (processor) {
            processor.disconnect();
            processor = null;
        }
        
        if (audioContext) {
            audioContext.close();
            audioContext = null;
        }
        
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.close();
        }
        
        isRecording = false;
        recordBtn.classList.remove("recording");
        statusDisplay.textContent = "Recording stopped. Check console for transcriptions.";
    };

    recordBtn.addEventListener("click", () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });
});