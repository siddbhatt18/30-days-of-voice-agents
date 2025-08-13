// static/script.js

document.addEventListener("DOMContentLoaded", async () => {
  // --- SESSION MANAGEMENT ---
  const urlParams = new URLSearchParams(window.location.search);
  let sessionId = urlParams.get('session_id');
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    window.history.replaceState({}, '', `?session_id=${sessionId}`);
  }

  // --- Conversational Agent Logic ---
  let mediaRecorder = null;
  let recordedChunks = [];
  let isRecording = false;

  const recordBtn = document.getElementById("recordBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");

  // When the agent's audio finishes playing, automatically start recording.
  audioPlayer.addEventListener('ended', () => {
      statusDisplay.textContent = "I'm listening...";
      startRecording();
  });

  const startRecording = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert("Audio recording not supported in this browser.");
      return;
    }

    isRecording = true;
    recordBtn.classList.add("recording");
    statusDisplay.textContent = "Recording... Press the button to stop.";
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
      isRecording = false;
      recordBtn.classList.remove("recording");
      statusDisplay.textContent = "Ready to chat!";
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
      isRecording = false;
      recordBtn.classList.remove("recording");
    }
  };

  const handleStopRecording = async () => {
    const blob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio_file", blob, "recording.webm");

    statusDisplay.textContent = "Thinking...";
    recordBtn.disabled = true;

    try {
      const currentSessionId = new URLSearchParams(window.location.search).get('session_id');
      if (!currentSessionId) {
          statusDisplay.textContent = "Error: Session ID is missing.";
          recordBtn.disabled = false;
          return;
      }

      const response = await fetch(`/agent/chat/${currentSessionId}`, {
        method: "POST",
        body: formData,
      });

      if (response.headers.get("X-Error") === "true") {
           statusDisplay.textContent = "I'm having trouble connecting right now.";
           const audioBlob = await response.blob();
           const audioUrl = URL.createObjectURL(audioBlob);
           audioPlayer.src = audioUrl;
           audioPlayer.hidden = true;
           audioPlayer.play();
           recordBtn.disabled = false; // Re-enable to try again
           return;
      }

      const result = await response.json();

      if (response.ok && result.audio_url) {
        statusDisplay.textContent = "Here is my response:";
        audioPlayer.src = result.audio_url;
        audioPlayer.hidden = true;
        audioPlayer.play();
      } else {
        statusDisplay.textContent = `Error: ${result.error || "Failed to get response."}`;
      }
    } catch (error) {
      console.error("Error with conversational agent:", error);
      statusDisplay.textContent = "An error occurred. Please try again.";
    } finally {
        recordBtn.disabled = false;
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