// A predefined list of fallback voices, now matching the API's key names.
const fallbackVoices = [
  { displayName: 'Natalie (Female)', voiceId: 'en-US-natalie' },
  { displayName: 'Aria (Female)', voiceId: 'en-US-aria' },
  { displayName: 'Guy (Male)', voiceId: 'en-US-guy' },
  { displayName: 'Davis (Male)', voiceId: 'en-US-davis' },
  { displayName: 'Sara (Female)', voiceId: 'en-US-sara' }
];

// Function to populate the voice selector dropdown.
function populateVoiceSelector(voices) {
  const voiceSelector = document.getElementById('voiceSelector');
  voiceSelector.innerHTML = ''; // Clear existing options

  voices.forEach(voice => {
    // **FIX**: Use `voice.displayName` for the text and `voice.voiceId` for the value.
    const option = new Option(voice.displayName, voice.voiceId);
    voiceSelector.add(option);
  });
}

// When the page is loaded, try to fetch voices from the API.
// If it fails, use the fallback list.
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch('/voices');
    if (!response.ok) {
      throw new Error('API response was not ok.');
    }
    // The key from the API is just 'voices', not 'voices.voices'
    const data = await response.json();
    
    if (data && data.length > 0) {
      populateVoiceSelector(data);
    } else {
      populateVoiceSelector(fallbackVoices);
    }
  } catch (error) {
    console.error("Failed to fetch voices from API, using fallback list.", error);
    populateVoiceSelector(fallbackVoices);
  }
});


async function generateTTS() {
  const text = document.getElementById('textInput').value;
  const voiceId = document.getElementById('voiceSelector').value;
  const button = document.getElementById('generateBtn');
  const errorDisplay = document.getElementById('errorDisplay');
  const audioPlayer = document.getElementById('audioPlayer');

  // Clear previous state
  errorDisplay.textContent = '';
  audioPlayer.hidden = true;

  // Set loading state
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
      // Display error message on the page
      errorDisplay.textContent = `Error: ${data.error || 'TTS generation failed.'}`;
      console.error(data);
    }
  } catch (err) {
    errorDisplay.textContent = 'An unexpected error occurred. Please try again.';
    console.error(err);
  } finally {
    // Reset button state
    button.disabled = false;
    button.textContent = 'Generate Voice';
  }
}
