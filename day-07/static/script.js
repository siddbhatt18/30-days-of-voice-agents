// static/script.js

// --- DAY 07 FIX: Updated fallback voices to match the expected object structure ---
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
    // This function now correctly works with both the API response and the fallback list
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
      statusDisplay.textContent = ""; // Clear status on success
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
  // Add event listener for the TTS button
  document.getElementById("generateBtn").addEventListener("click", generateTTS);

  // Populate voices for TTS
  try {
    const res = await fetch("/voices");
    if (!res.ok) throw new Error("Failed to fetch voices from API");
    const data = (await res.json()) || {};
    // The Murf API nests the voices in a "voices" key
    const voices = data.voices || [];
    populateVoiceSelector(voices.length ? voices : fallbackVoices);
  } catch (e) {
    console.warn("API call for voices failed. Using fallback list.", e);
    populateVoiceSelector(fallbackVoices);
  }

  // --- DAY 07: Echo Bot Logic ---
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
    statusDisplay.textContent = "Recording...";
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

        statusDisplay.textContent = "Transcribing and generating echo...";

        try {
          const response = await fetch("/tts/echo", {
            method: "POST",
            body: formData,
          });
          const result = await response.json();

          if (response.ok && result.audio_url) {
            statusDisplay.textContent = `I heard: "${result.text}"`;
            audioPlayer.src = result.audio_url;
            audioPlayer.hidden = false;
            audioPlayer.play();
          } else {
            statusDisplay.textContent = `Error: ${result.error || "Echo failed"}`;
          }
        } catch (error) {
          console.error("Error echoing audio:", error);
          statusDisplay.textContent = "An error occurred during the echo process.";
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
