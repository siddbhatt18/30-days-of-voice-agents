const startAndstopBtn = document.getElementById('startAndstopBtn');
const chatLog = document.getElementById('chat-log');
const loadingIndicator = document.getElementById('loading');

let isRecording = false;
let ws = null;
let stream;
let audioCtx;
let source;
let processor;

 // state hi kehde auiooooooo ayooooooooooooooo
let audioContext;
let playheadTime = 0;

 
function getSessionId() {
    const params = new URLSearchParams(window.location.search);
    let id = params.get("session");
    if (!id) {
        id = crypto.randomUUID();
        params.set("session", id);
        window.history.replaceState({}, "", `${location.pathname}?${params}`);
    }
    return id;
}
const sessionId = getSessionId();

// ---------- Chat UI helpers ----------
function addTextMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    messageDiv.textContent = text;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function addAudioMessage(audioUrl, type) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);

    const audioPlayer = document.createElement('audio');
    audioPlayer.controls = true;
    audioPlayer.src = audioUrl;

    messageDiv.appendChild(audioPlayer);
    chatLog.appendChild(messageDiv);

    if (type === 'received') {
        audioPlayer.play();
    }
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function endtoendAudio(formdata) {
    try {
        loadingIndicator.style.display = "flex";

        const response = await fetch(`/agent/chat/${sessionId}`, {
            method: "POST",
            body: formdata
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error: ${response.status} ${errorText}`);
        }

        const data = await response.json();
        console.log("Chat History:", data.history);
        return data;

    } catch (error) {
        console.error("Error from transcribe to audio:", error.message);
        addTextMessage(`Error: ${error.message}`, 'error');
    } finally {
        loadingIndicator.style.display = "none";
    }
}

// ---------- Helpers ----------
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

// ---------- Real-time playback (fixed) ----------
function base64ToPCMFloat32(base64) {
    const binary = atob(base64);
    let offset = 0;

    // Detect and skip WAV header if present
    if (binary.length > 44 && binary.slice(0, 4) === "RIFF") {
        offset = 44;
    }

    const length = binary.length - offset;
    const byteArray = new Uint8Array(length);
    for (let i = 0; i < length; i++) {
        byteArray[i] = binary.charCodeAt(i + offset);
    }

    const view = new DataView(byteArray.buffer);
    const sampleCount = byteArray.length / 2;
    const float32Array = new Float32Array(sampleCount);

    for (let i = 0; i < sampleCount; i++) {
        const int16 = view.getInt16(i * 2, true);
        float32Array[i] = int16 / 32768;
    }
    return float32Array;
}

function playAudioChunk(base64Audio) {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 44100 });
        playheadTime = audioContext.currentTime;
    }

    const float32Array = base64ToPCMFloat32(base64Audio);
    if (!float32Array) return;

    // Create audio buffer for this chunk
    const buffer = audioContext.createBuffer(1, float32Array.length, 44100);
    buffer.copyToChannel(float32Array, 0);

    const source = audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(audioContext.destination);

    // Keep 150ms buffer headroom to absorb jitter
    const now = audioContext.currentTime;
    if (playheadTime < now + 0.15) {
        playheadTime = now + 0.15;
    }

    source.start(playheadTime);
    playheadTime += buffer.duration;
}

// ---------- Recording ----------
async function startRecording() {
    ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => console.log("WebSocket connected");
    ws.onclose = () => console.log("WebSocket closed");
    ws.onerror = (err) => console.error("WebSocket error", err);

    ws.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            console.log(msg);

            if (msg.type === "transcript") {
                addTextMessage(msg.text, "sent");

            } else if (msg.type === "ai_response") {
                addTextMessage(msg.text, "received");

            } else if (msg.type === "audio_chunk") {
                playAudioChunk(msg.audio);
            } else {
                console.log("Unknown message:", msg);
            }

        } catch (err) {
            console.error("Failed to parse server message", err, event.data);
        }
    };

    stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioCtx = new AudioContext({ sampleRate: 16000 });
    source = audioCtx.createMediaStreamSource(stream);
    processor = audioCtx.createScriptProcessor(4096, 1, 1);

    source.connect(processor);
    processor.connect(audioCtx.destination);

    processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        const pcm16 = floatTo16BitPCM(inputData);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(pcm16);
        }
    };
}

function stopRecording() {
    if (processor) {
        processor.disconnect();
        processor.onaudioprocess = null;
    }
    if (source) source.disconnect();
    if (audioCtx) audioCtx.close();

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (ws) ws.close();
}

startAndstopBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    if (!isRecording) {
        try {
            await startRecording();
            isRecording = true;
            startAndstopBtn.textContent = "Stop Recording";
            startAndstopBtn.classList.add("recording");
        } catch (err) {
            console.error("Mic error", err);
            alert("Microphone access denied.");
        }
    } else {
        stopRecording();
        isRecording = false;
        startAndstopBtn.textContent = "Start Recording";
        startAndstopBtn.classList.remove("recording");
    }
});
