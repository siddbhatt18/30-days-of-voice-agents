// --- Fallback voices in case API call fails
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
  voices.forEach(v => {
    voiceSelector.add(new Option(v.displayName, v.voiceId));
  });
}

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
    const response = await fetch('/tts', { method: 'POST', body: formData });
    const data = await response.json();

    if (response.ok && data.audio_url) {
      audioPlayer.src = data.audio_url;
      audioPlayer.hidden = false;
      audioPlayer.play();
    } else {
      errorDisplay.textContent = `Error: ${data.error || 'TTS failed.'}`;
      console.error(data);
    }
  } catch (err) {
    errorDisplay.textContent = 'An unexpected error occurred.';
    console.error(err);
  } finally {
    button.disabled = false;
    button.textContent = 'Generate Voice';
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  // Populate voices
  try {
    const res = await fetch('/voices');
    const voices = (await res.json()) || [];
    populateVoiceSelector(voices.length ? voices : fallbackVoices);
  } catch (e) {
    console.warn('Falling back to default voices.', e);
    populateVoiceSelector(fallbackVoices);
  }

  // --- Echo Bot Logic ---
  let mediaRecorder = null;
  let recordedChunks = [];

  const startBtn = document.getElementById('startBtn');
  const stopBtn = document.getElementById('stopBtn');
  const echoAudio = document.getElementById('echoAudio');

  startBtn.addEventListener('click', async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      alert('Audio recording not supported in this browser.');
      return;
    }

    startBtn.disabled = true;
    stopBtn.disabled = false;
    recordedChunks = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        echoAudio.src = url;
        echoAudio.hidden = false;
        echoAudio.play();
      };

      mediaRecorder.start();
    } catch (err) {
      console.error('Error accessing mic:', err);
      startBtn.disabled = false;
      stopBtn.disabled = true;
    }
  });

  stopBtn.addEventListener('click', () => {
    stopBtn.disabled = true;
    mediaRecorder.stop();
    startBtn.disabled = false;
  });
});
