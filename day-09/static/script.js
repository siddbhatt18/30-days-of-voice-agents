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

  // --- DAY 09: Conversational Agent Logic ---
  let mediaRecorder = null;
  let recordedChunks = [];

  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");

  startBtn.addEventListener("click", async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert("Audio recording not supported in this browser.");
      return;
    }

    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusDisplay.textContent = "Recording... Ask your question.";
    audioPlayer.hidden = true;
    recordedChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(recordedChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio_file", blob, "recording.webm");

        statusDisplay.textContent = "Thinking...";

        try {
          // Send the recorded audio to the new /llm/query endpoint
          const response = await fetch("/llm/query", {
            method: "POST",
            body: formData,
          });
          const result = await response.json();

          if (response.ok && result.audio_url) {
            statusDisplay.textContent = "Here is my response:";
            audioPlayer.src = result.audio_url;
            audioPlayer.hidden = false;
            audioPlayer.play();
          } else {
            statusDisplay.textContent = `Error: ${result.error || "Failed to get response."}`;
          }
        } catch (error) {
          console.error("Error with conversational agent:", error);
          statusDisplay.textContent = "An error occurred during the process.";
        }
      };

      mediaRecorder.start();
    } catch (err) {
      console.error("Error accessing mic:", err);
      alert("Could not access microphone. Please check permissions.");
      startBtn.disabled = false;
      stopBtn.disabled = true;
      statusDisplay.textContent = "";
    }
  });

  stopBtn.addEventListener("click", () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
    }
    stopBtn.disabled = true;
    startBtn.disabled = false;
  });
});