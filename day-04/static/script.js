// ========== Text-to-Speech (TTS) ==========
const fallbackVoices = [
  { displayName: 'Natalie (Female)', voiceId: 'en-US-natalie' },
  { displayName: 'Aria (Female)', voiceId: 'en-US-aria' },
  { displayName: 'Guy (Male)', voiceId: 'en-US-guy' },
  { displayName: 'Davis (Male)', voiceId: 'en-US-davis' },
  { displayName: 'Sara (Female)', voiceId: 'en-US-sara' }
];

function populateVoiceSelector(voices) {
  const voiceSelector = document.getElementById('voiceSelector');
  voiceSelector.innerHTML = '';
  voices.forEach(voice => {
    const option = new Option(voice.displayName, voice.voiceId);
    voiceSelector.add(option);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/voices');
    if (!response.ok) throw new Error('Failed to fetch voices');
    const data = await response.json();
    if (Array.isArray(data) && data.length > 0) {
      populateVoiceSelector(data);
    } else {
      populateVoiceSelector(fallbackVoices);
    }
  } catch (error) {
    console.error("Using fallback voices due to error:", error);
    populateVoiceSelector(fallbackVoices);
  }
});

async function generateTTS() {
  const text = document.getElementById('textInput').value;
  const voiceId = document.getElementById('voiceSelector').value;
  const button = document.getElementById('generateBtn');
  const errorDisplay = document.getElementById('errorDisplay');
  const audioPlayer = document.getElementById('audioPlayer');

  errorDisplay.textContent = '';
  audioPlayer.hidden = true;

  button.disabled = true;
  button.textContent = 'Generating...';

  const formData = new FormData();
  formData.append('text', text);
  formData.append('voiceId', voiceId);

  try {
    const response = await fetch('/tts', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (response.ok && data.audio_url) {
      audioPlayer.src = data.audio_url;
      audioPlayer.hidden = false;
      audioPlayer.play();
    } else {
      errorDisplay.textContent = `Error: ${data.error || 'TTS generation failed.'}`;
      console.error(data);
    }
  } catch (err) {
    errorDisplay.textContent = 'An unexpected error occurred. Please try again.';
    console.error(err);
  } finally {
    button.disabled = false;
    button.textContent = 'Generate Voice';
  }
}


// ========== Echo Bot (Voice Recording) ==========

let mediaRecorder = null;
let mediaStream = null;
let audioChunks = [];
let currentAudioUrl = null;

const startBtn = document.getElementById('startRecordingBtn');
const stopBtn = document.getElementById('stopRecordingBtn');
const echoAudio = document.getElementById('echoAudio');
const echoError = document.getElementById('echoError');

startBtn.addEventListener('click', async () => {
  echoError.textContent = '';
  echoAudio.hidden = true;
  echoAudio.pause();
  echoAudio.removeAttribute('src');
  audioChunks = [];

  if (currentAudioUrl) {
    URL.revokeObjectURL(currentAudioUrl);
    currentAudioUrl = null;
  }

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(mediaStream);

    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      currentAudioUrl = URL.createObjectURL(audioBlob);
      echoAudio.src = currentAudioUrl;
      echoAudio.hidden = false;
      echoAudio.load();
      echoAudio.play();

      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
      }
    };

    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;

  } catch (err) {
    echoError.textContent = 'Microphone access denied or unavailable.';
    console.error('Microphone error:', err);
  }
});

stopBtn.addEventListener('click', () => {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
  }
});
