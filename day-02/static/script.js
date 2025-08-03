async function generateTTS() {
  const text = document.getElementById('textInput').value;

  const formData = new FormData();
  formData.append('text', text);

  const response = await fetch('/tts', {
    method: 'POST',
    body: formData
  });

  const data = await response.json();

  if (data.audio_url) {
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.src = data.audio_url;
    audioPlayer.hidden = false;
    audioPlayer.play();
  } else {
    alert('TTS generation failed.');
    console.error(data);
  }
}
