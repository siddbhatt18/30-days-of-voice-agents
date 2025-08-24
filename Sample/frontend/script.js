const startAndstopBtn = document.getElementById('startAndstopBtn');
const chatLog = document.getElementById('chat-log');
const loadingIndicator = document.getElementById('loading');

let isRecording = false;
let ws = null;
let stream;
let audioCtx;
let source;
let processor;

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

/*  Start Recording with Web Audio API */
async function startRecording() {
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

/* Play base64 audio chunks as they arrive */
let audioQueue = [];
let isPlaying = false;

function playAudioChunk(b64) {
    const audioData = Uint8Array.from(atob(b64), c => c.charCodeAt(0)).buffer;
    audioCtx.decodeAudioData(audioData.slice(0))
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
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    source.connect(audioCtx.destination);
    source.onended = () => playNextChunk();
    source.start();
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
