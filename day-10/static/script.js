// static/script.js

const fallbackVoices = [
  { name: "Natalie", gender: "Female", voiceId: "en-US-natalie" },
  { name: "Aria", gender: "Female", voiceId: "en-US-aria" },
  { name: "Guy", gender: "Male", voiceId: "en-US-guy" },
  { name: "Davis", gender: "Male", voiceId: "en-US-davis" },
  { name: "Sara", gender: "Female", voiceId: "en-US-sara" },
];

function populateVoiceSelector(voices) {
  const voiceSelector = document.getElementById("voiceSelector");
  voiceSelector.innerHTML = "";
  voices.forEach((v) => {
    voiceSelector.add(new Option(`${v.name} (${v.gender})`, v.voiceId));
  });
}

async function generateTTS() {
  const text = document.getElementById("textInput").value;
  const voiceId = document.getElementById("voiceSelector").value;
  const button = document.getElementById("generateBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");

  statusDisplay.textContent = "";
  audioPlayer.hidden = true;
  button.disabled = true;
  button.textContent = "Generating...";

  const formData = new FormData();
  formData.append("text", text);
  formData.append("voiceId", voiceId);

  try {
    const response = await fetch("/tts", { method: "POST", body: formData });
    const data = await response.json();

    if (response.ok && data.audio_url) {
      audioPlayer.src = data.audio_url;
      audioPlayer.hidden = false;
      audioPlayer.play();
      statusDisplay.textContent = ""; 
    } else {
      statusDisplay.textContent = `Error: ${data.error || "TTS failed."}`;
    }
  } catch (err) {
    statusDisplay.textContent = "An unexpected error occurred.";
  } finally {
    button.disabled = false;
    button.textContent = "Generate Voice";
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  // --- SESSION MANAGEMENT ---
  const urlParams = new URLSearchParams(window.location.search);
  let sessionId = urlParams.get('session_id');
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    window.history.replaceState({}, '', `?session_id=${sessionId}`);
  }

  document.getElementById("generateBtn").addEventListener("click", generateTTS);

  try {
    const res = await fetch("/voices");
    if (!res.ok) throw new Error("Failed to fetch voices from API");
    const data = (await res.json()) || {};
    const voices = data.voices || [];
    populateVoiceSelector(voices.length ? voices : fallbackVoices);
  } catch (e) {
    console.warn("API call for voices failed. Using fallback list.", e);
    populateVoiceSelector(fallbackVoices);
  }

  // --- DAY 10: Conversational Agent Logic ---
  let mediaRecorder = null;
  let recordedChunks = [];

  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");

  // When the agent's audio finishes playing, automatically start recording.
  audioPlayer.addEventListener('ended', () => {
      statusDisplay.textContent = "I'm listening... Click Stop to send.";
      // Instead of simulating a click, directly call the start recording logic
      // and manually set the button states for reliability.
      startRecording();
  });
  
  const startRecording = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert("Audio recording not supported in this browser.");
      return;
    }

    startBtn.disabled = true;
    stopBtn.disabled = false; // Explicitly enable the stop button
    statusDisplay.textContent = "Recording... Click Stop when you're done.";
    audioPlayer.hidden = true;
    recordedChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };

      mediaRecorder.onstop = handleStopRecording;
      mediaRecorder.start();

    } catch (err) {
      console.error("Error accessing mic:", err);
      alert("Could not access microphone. Please check permissions.");
      startBtn.disabled = false;
      stopBtn.disabled = true;
      statusDisplay.textContent = "Ready to chat!";
    }
  };


  const handleStopRecording = async () => {
    const blob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio_file", blob, "recording.webm");

    statusDisplay.textContent = "Thinking...";
    startBtn.disabled = true;
    stopBtn.disabled = true;

    try {
      const currentSessionId = new URLSearchParams(window.location.search).get('session_id');
      if (!currentSessionId) {
          statusDisplay.textContent = "Error: Session ID is missing.";
          startBtn.disabled = false;
          return;
      }

      const response = await fetch(`/agent/chat/${currentSessionId}`, {
        method: "POST",
        body: formData,
      });
      const result = await response.json();

      if (response.ok && result.audio_url) {
        statusDisplay.textContent = "Here is my response:";
        audioPlayer.src = result.audio_url;
        audioPlayer.hidden = false;
        audioPlayer.play();
        // The 'ended' event on the audio player will now automatically start the next recording.
      } else {
        statusDisplay.textContent = `Error: ${result.error || "Failed to get response."}`;
        startBtn.disabled = false; // Re-enable start on error to allow user to try again.
      }
    } catch (error) {
      console.error("Error with conversational agent:", error);
      statusDisplay.textContent = "An error occurred. Please try again.";
      startBtn.disabled = false; // Re-enable start on error.
    }
  };

  // The start button now only initiates the very first recording.
  startBtn.addEventListener("click", startRecording);

  stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
    }
  });
});
