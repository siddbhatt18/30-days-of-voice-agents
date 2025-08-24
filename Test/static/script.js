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
    let audioContext;
    let source = null;
    let processor = null;
    let isRecording = false;
    let ws = null;
    let stream;

    // Audio streaming variables
    let audioQueue = [];
    let isPlaying = false;

    const recordBtn = document.getElementById("recordBtn");
    const statusDisplay = document.getElementById("statusDisplay");
    const transcriptionDisplay = document.getElementById("transcriptionDisplay");
    const currentTranscript = document.getElementById("currentTranscript");
    const transcriptionHistory = document.getElementById("transcriptionHistory");
    const chatLog = document.getElementById('chat-log');


    function addTextMessage(text, type) {
        const messageDiv = document.createElement('div');

        if (type === "llm") {
            // Agent → left side
            messageDiv.className = 'self-start max-w-[80%] px-4 py-2 bg-gray-800 rounded-xl text-sm text-gray-200';
        } else if (type === "transcript") {
            // User → right side
            messageDiv.className = 'self-end max-w-[80%] px-4 py-2 bg-indigo-600 rounded-xl text-sm text-white';
        }

        messageDiv.textContent = text;
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    /* Convert Float32 → PCM16 */
    function floatTo16BitPCM(float32Array) {
        const buffer = new ArrayBuffer(float32Array.length * 2);
        const view = new DataView(buffer);
        let offset = 0;
        for (let i = 0; i < float32Array.length; i++, offset += 2) {
            let s = Math.max(-1, Math.min(1, float32Array[i]));
            view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
        }
        return buffer;
    }

    const startRecording = async () => {
        ws = new WebSocket("ws://127.0.0.1:8000/ws/audio");

        ws.onopen = () => console.log("WebSocket connected");
        ws.onclose = () => console.log("WebSocket closed");
        ws.onerror = (err) => console.error("WebSocket error", err);

        ws.onmessage = (event) => {
            try {
                const msg = JSON.parse(event.data);

                if (msg.type === "llm") {
                    addTextMessage(msg.text, "llm");
                } else if (msg.type === "final") {
                    addTextMessage(msg.text, "transcript");
                } else if (msg.type === "audio") {
                    playAudioChunk(msg.b64); // 🔊 Play streaming audio
                } else if (msg.type === "error") {
                    console.error("Server error:", msg.message);
                }
            } catch {
                console.log("Raw message:", event.data);
            }
        };

        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioContext = new AudioContext({ sampleRate: 16000 });
        source = audioContext.createMediaStreamSource(stream);
        processor = audioContext.createScriptProcessor(4096, 1, 1);

        source.connect(processor);
        processor.connect(audioContext.destination);

        processor.onaudioprocess = (e) => {
            const inputData = e.inputBuffer.getChannelData(0);
            const pcm16 = floatTo16BitPCM(inputData);
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(pcm16);
            }
        };
    }

    function playAudioChunk(b64) {
        const audioData = Uint8Array.from(atob(b64), c => c.charCodeAt(0)).buffer;
        audioContext.decodeAudioData(audioData)
            .then(buffer => {
                audioQueue.push(buffer);
                if (!isPlaying) playNextChunk();
            })
            .catch(err => console.error("Decode error:", err));
    }

    function playNextChunk() {
        if (audioQueue.length === 0) {
            isPlaying = false;
            return;
        }
        isPlaying = true;
        const buffer = audioQueue.shift();
        const sourceNode = audioContext.createBufferSource();
        sourceNode.buffer = buffer;
        sourceNode.connect(audioContext.destination);
        sourceNode.onended = () => playNextChunk();
        sourceNode.start();
    }

    const stopRecording = () => {
        if (!isRecording) return;

        isRecording = false;
        recordBtn.classList.remove("recording");
        statusDisplay.textContent = "Stopping recording...";
        statusDisplay.classList.remove("text-danger");

        // Clean up audio processing
        if (processor) {
            processor.disconnect();
            processor.onaudioprocess = null;
        }

        if (source) {
            source.disconnect();
        }

        if (audioContext && audioContext.state !== 'closed') {
            audioContext.close();
        }


        // Stop media stream tracks
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }

        // Send EOF and close WebSocket
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.close();
        }
        ws = null;

        // Log final audio session summary if exists
        if (audioQueue.length > 0) {
            console.log(`[Day 21] Session ended with ${audioQueue.length} total audio chunks accumulated`);
        }

        statusDisplay.textContent = "Ready to chat!";
    };

    recordBtn.addEventListener("click", () => {
        if (isRecording) {
            stopRecording();
            recordBtn.textContent = "Start Recording";

        } else {
            isRecording = true;
            recordBtn.classList.add("recording");
            statusDisplay.textContent = "Listening... Speak now.";
            recordBtn.textContent = "Stop Recording";
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