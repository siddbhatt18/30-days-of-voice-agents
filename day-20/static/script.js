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

    // Track processed transcriptions to prevent UI duplicates
    let processedTranscripts = new Set();
    let lastTranscriptTime = 0;

    const recordBtn = document.getElementById("recordBtn");
    const statusDisplay = document.getElementById("statusDisplay");
    const transcriptionDisplay = document.getElementById("transcriptionDisplay");
    const currentTranscript = document.getElementById("currentTranscript");
    const transcriptionHistory = document.getElementById("transcriptionHistory");

    const startRecording = async () => {
        if (!navigator.mediaDevices?.getUserMedia) {
            alert("Audio recording not supported in this browser.");
            return;
        }

        isRecording = true;
        recordBtn.classList.add("recording");
        statusDisplay.textContent = "Listening... Speak now.";
        
        // Show transcription area and clear current transcript
        currentTranscript.textContent = "Listening for speech...";
        transcriptionDisplay.classList.remove("d-none");

        // Reset duplicate tracking for new recording session
        processedTranscripts.clear();
        lastTranscriptTime = 0;

        try {
            // Establish WebSocket connection
            const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
            socket = new WebSocket(`${wsProtocol}//${window.location.host}/ws`);

            socket.onopen = async () => {
                console.log("WebSocket connection established for streaming transcription with turn detection.");
                statusDisplay.textContent = "Connected. Speak now - I'll detect when you stop talking.";

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

            // Handle messages from the WebSocket (transcription updates and turn detection)
            socket.onmessage = (event) => {
                console.log("Received WebSocket message:", event.data);
                try {
                    const data = JSON.parse(event.data);
                    console.log("Parsed message data:", data);
                    
                    if (data.type === "transcription" && data.end_of_turn) {
                        // Display transcription only at end of turn
                        console.log(`End of turn transcription: ${data.text}`);
                        
                        // Normalize transcript for duplicate detection (same as backend)
                        const normalizedText = data.text.toLowerCase().replace(/\s+/g, ' ').trim();
                        const currentTime = Date.now();
                        
                        // Check for duplicates (same logic as backend)
                        if (data.text.length > 3 && 
                            !processedTranscripts.has(normalizedText) && 
                            currentTime - lastTranscriptTime > 2000) { // 2 second gap
                            
                            // Mark as processed
                            processedTranscripts.add(normalizedText);
                            lastTranscriptTime = currentTime;
                            
                            // Update the current transcript display
                            currentTranscript.textContent = data.text;
                            currentTranscript.classList.add("final-transcript");
                            
                            // Add to transcription history
                            addToTranscriptionHistory(data.text);
                            
                            // Update status
                            statusDisplay.textContent = "Turn completed. Continue speaking or stop recording.";
                        }
                        
                    } else if (data.type === "turn_end") {
                        console.log("Turn end detected:", data.message);
                        statusDisplay.textContent = "Turn detected. Waiting for next speech...";
                        
                        // Reset current transcript display for next turn
                        setTimeout(() => {
                            currentTranscript.textContent = "Listening for next speech...";
                            currentTranscript.classList.remove("final-transcript");
                        }, 2000);
                        
                    } else if (data.type === "error") {
                        console.error("Transcription error:", data.message);
                        statusDisplay.textContent = `Error: ${data.message}`;
                        statusDisplay.classList.add("text-danger");
                    } else if (data.type === "status") {
                        console.log("Status message:", data.message);
                        statusDisplay.textContent = data.message;
                    }
                } catch (err) {
                    console.error("Error parsing WebSocket message:", err, "Raw data:", event.data);
                }
            };

            socket.onclose = () => {
                console.log("WebSocket connection closed.");
                statusDisplay.textContent = "Transcription session ended.";
                statusDisplay.classList.remove("text-danger");
            };

            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
                statusDisplay.textContent = "Connection error occurred.";
                statusDisplay.classList.add("text-danger");
            };

        } catch (err) {
            console.error("Error starting recording:", err);
            alert("Failed to start recording session.");
            stopRecording();
        }
    };

    const addToTranscriptionHistory = (text) => {
        if (!transcriptionHistory) return;
        
        const historyItem = document.createElement("div");
        historyItem.className = "transcription-history-item";
        historyItem.innerHTML = `
            <div class="history-timestamp">${new Date().toLocaleTimeString()}</div>
            <div class="history-text">${text}</div>
        `;
        transcriptionHistory.appendChild(historyItem);
        
        // Scroll to bottom of history
        transcriptionHistory.scrollTop = transcriptionHistory.scrollHeight;
    };

    const stopRecording = () => {
        if (!isRecording) return;

        isRecording = false;
        recordBtn.classList.remove("recording");
        statusDisplay.textContent = "Stopping recording...";
        statusDisplay.classList.remove("text-danger");

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