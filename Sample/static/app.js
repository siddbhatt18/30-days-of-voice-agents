document.addEventListener("DOMContentLoaded", function () {
  console.log("Voice Agents App Loaded!");
  let voiceQueryRecorder;
  let voiceQueryChunks = [];
  let voiceQueryStream;
  let voiceQueryStartTime;
  let voiceQueryTimerInterval;
  let sessionId =
    getSessionIdFromUrl() || window.SESSION_ID || generateSessionId();
  initializeSession();

  const voiceQueryBtn = document.getElementById("voiceQueryBtn");
  const voiceQueryStatus = document.getElementById("voiceQueryStatus");
  const voiceQueryTimer = document.getElementById("voiceQueryTimer");
  const voiceQueryMessageDisplay = document.getElementById(
    "voiceQueryMessageDisplay"
  );
  const voiceQueryContainer = document.getElementById("voiceQueryContainer");
  const voiceQueryTranscription = document.getElementById(
    "voiceQueryTranscription"
  );
  const voiceQueryLLMResponse = document.getElementById(
    "voiceQueryLLMResponse"
  );
  const voiceQueryAudioPlayer = document.getElementById(
    "voiceQueryAudioPlayer"
  );
  const askAgainBtn = document.getElementById("askAgainBtn");
  const toggleChatHistoryBtn = document.getElementById("toggleChatHistory");
  const chatHistoryContainer = document.getElementById("chatHistoryContainer");
  if (toggleChatHistoryBtn) {
    toggleChatHistoryBtn.addEventListener("click", toggleChatHistory);
  }

  function getSessionIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("session_id");
  }
  function generateSessionId() {
    return (
      "session_" + Math.random().toString(36).substr(2, 9) + "_" + Date.now()
    );
  }

  function updateUrlWithSessionId(sessionId) {
    const url = new URL(window.location);
    url.searchParams.set("session_id", sessionId);
    window.history.replaceState({}, "", url);
    const sessionIdElement = document.getElementById("sessionId");
    if (sessionIdElement) {
      sessionIdElement.textContent = sessionId;
    }
  }

  async function initializeSession() {
    updateUrlWithSessionId(sessionId);
    console.log(`Initializing session: ${sessionId}`);
    await loadChatHistory();
  }

  async function loadChatHistory() {
    try {
      const response = await fetch(`/agent/chat/${sessionId}/history`);
      const data = await response.json();
      if (data.success && data.messages.length > 0) {
        console.log(
          `Loaded ${data.message_count} messages for session ${sessionId}`
        );
        displayChatHistory(data.messages);
        showVoiceQueryMessage(
          `Previous session loaded with ${data.message_count} messages. Click "Show Chat History" to view them.`,
          "success"
        );
      } else {
        console.log(`No previous messages found for session ${sessionId}`);
      }
    } catch (error) {
      console.error("Failed to load chat history:", error);
    }
  }

  function displayChatHistory(messages) {
    const chatHistoryList = document.getElementById("chatHistoryList");
    if (!chatHistoryList) return;

    chatHistoryList.innerHTML = "";

    if (messages.length === 0) {
      chatHistoryList.innerHTML =
        '<p class="no-history">No previous messages in this session.</p>';
      return;
    }

    // Group messages by conversation pairs (user + assistant)
    const conversations = [];
    for (let i = 0; i < messages.length; i += 2) {
      const userMsg = messages[i];
      const assistantMsg = messages[i + 1];
      if (
        userMsg &&
        assistantMsg &&
        userMsg.role === "user" &&
        assistantMsg.role === "assistant"
      ) {
        conversations.push({
          user: userMsg,
          assistant: assistantMsg,
          timestamp: userMsg.timestamp,
        });
      }
    }

    if (conversations.length === 0) {
      chatHistoryList.innerHTML =
        '<p class="no-history">No complete conversations found.</p>';
      return;
    }

    conversations.forEach((conv, index) => {
      const conversationDiv = document.createElement("div");
      conversationDiv.className = "conversation-card";
      conversationDiv.style.cursor = "pointer";

      let timestamp;
      try {
        const dateObj = new Date(conv.timestamp);
        timestamp = dateObj.toLocaleString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
          hour: "numeric",
          minute: "2-digit",
          hour12: true,
        });
      } catch (error) {
        console.error("Error parsing timestamp:", error);
        timestamp = "Just now";
      }

      const userPreview =
        conv.user.content.length > 80
          ? conv.user.content.substring(0, 80) + "..."
          : conv.user.content;
      const assistantPreview =
        conv.assistant.content.length > 100
          ? conv.assistant.content.substring(0, 100) + "..."
          : conv.assistant.content;

      conversationDiv.innerHTML = `
        <div class="conversation-header">
          <span class="conversation-number">Conversation ${
            conversations.length - index
          }</span>
          <span class="conversation-time">${timestamp}</span>
        </div>
        <div class="conversation-content">
          <div class="user-preview">
            <span class="role-label">👤 You:</span>
            <span class="preview-text">${userPreview}</span>
          </div>
          <div class="assistant-preview">
            <span class="role-label">🤖 AI:</span>
            <span class="preview-text">${assistantPreview}</span>
          </div>
        </div>
      `;

      conversationDiv.addEventListener("click", function () {
        displayConversationInMainArea(
          conv.user.content,
          conv.assistant.content
        );
        toggleChatHistory();
      });

      chatHistoryList.appendChild(conversationDiv);
    });
  }

  function displayConversationInMainArea(userQuestion, assistantResponse) {
    if (voiceQueryContainer) {
      voiceQueryContainer.style.display = "block";
    }
    if (voiceQueryTranscription) {
      voiceQueryTranscription.innerHTML = userQuestion;
    }

    if (voiceQueryLLMResponse) {
      try {
        if (typeof marked !== "undefined") {
          marked.setOptions({
            breaks: true,
            gfm: true,
            sanitize: false,
            highlight: function (code, lang) {
              if (
                typeof hljs !== "undefined" &&
                lang &&
                hljs.getLanguage(lang)
              ) {
                try {
                  return hljs.highlight(code, { language: lang }).value;
                } catch (err) {}
              }
              return code;
            },
          });
          const markdownHtml = marked.parse(assistantResponse);
          voiceQueryLLMResponse.innerHTML = markdownHtml;

          // Apply syntax highlighting
          if (typeof hljs !== "undefined") {
            voiceQueryLLMResponse
              .querySelectorAll("pre code")
              .forEach((block) => {
                hljs.highlightElement(block);
              });
          }
        } else {
          voiceQueryLLMResponse.innerHTML = assistantResponse.replace(
            /\n/g,
            "<br>"
          );
        }
      } catch (error) {
        console.error("Markdown parsing error:", error);
        voiceQueryLLMResponse.innerHTML = assistantResponse.replace(
          /\n/g,
          "<br>"
        );
      }
    }

    if (voiceQueryAudioPlayer) {
      voiceQueryAudioPlayer.src = "";
    }

    const responseAudioSection = document.querySelector(
      ".response-audio-section"
    );
    if (responseAudioSection) {
      responseAudioSection.style.display = "none";
    }

    voiceQueryContainer.scrollIntoView({ behavior: "smooth" });

    showVoiceQueryMessage(
      "Previous conversation loaded successfully!",
      "success"
    );
  }

  function toggleChatHistory() {
    const container = document.getElementById("chatHistoryContainer");
    const button = document.getElementById("toggleChatHistory");

    if (container.style.display === "none" || !container.style.display) {
      container.style.display = "block";
      button.textContent = "Hide Chat History";
      loadChatHistory();
    } else {
      container.style.display = "none";
      button.textContent = "Show Chat History";
    }
  }

  if (voiceQueryAudioPlayer) {
    voiceQueryAudioPlayer.addEventListener("ended", function () {
      console.log("Audio playback ended, starting auto-recording...");
      setTimeout(() => {
        if (!voiceQueryRecorder || voiceQueryRecorder.state !== "recording") {
          updateVoiceQueryButton("ready");
          startVoiceQuery();
        }
      }, 1000);
    });
  }

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    if (voiceQueryBtn) {
      showVoiceQueryMessage(
        "Your browser doesn't support audio recording. Please use a modern browser like Chrome, Firefox, or Safari.",
        "error"
      );
      voiceQueryBtn.disabled = true;
    }
  } else {
    if (voiceQueryBtn) {
      voiceQueryBtn.addEventListener("click", toggleVoiceQuery);

      if (askAgainBtn) {
        askAgainBtn.addEventListener("click", function () {
          hideVoiceQuery();
          resetVoiceQueryState();
          // Don't auto-start recording when manually clicking "Ask Again"
        });
      }
    }
  }

  function toggleVoiceQuery() {
    const currentState = voiceQueryBtn.getAttribute("data-state");

    if (currentState === "ready" || currentState === "completed") {
      startVoiceQuery();
    } else if (currentState === "recording") {
      stopVoiceQuery();
    }
  }

  function updateVoiceQueryButton(state) {
    if (!voiceQueryBtn) return;

    const btnIcon = voiceQueryBtn.querySelector(".btn-icon");
    const btnText = voiceQueryBtn.querySelector(".btn-text");

    voiceQueryBtn.setAttribute("data-state", state);

    switch (state) {
      case "ready":
        voiceQueryBtn.disabled = false;
        voiceQueryBtn.className = "btn primary";
        btnIcon.textContent = "🎤";
        btnText.textContent = "Start Recording";
        break;
      case "recording":
        voiceQueryBtn.disabled = false;
        voiceQueryBtn.className = "btn secondary recording";
        btnIcon.textContent = "⏹️";
        btnText.textContent = "Stop Recording";
        break;
      case "processing":
        voiceQueryBtn.disabled = true;
        voiceQueryBtn.className = "btn processing";
        btnIcon.textContent = "⏳";
        btnText.textContent = "Processing...";
        break;
      case "completed":
        voiceQueryBtn.disabled = false;
        voiceQueryBtn.className = "btn primary";
        btnIcon.textContent = "🎤";
        btnText.textContent = "Ask Another Question";
        break;
    }
  }

  function getSupportedMimeType() {
    const mimeTypes = ["audio/webm"];

    for (let mimeType of mimeTypes) {
      if (MediaRecorder.isTypeSupported(mimeType)) {
        return mimeType;
      }
    }

    return "audio/webm";
  }
  async function startVoiceQuery() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      showVoiceQueryMessage(
        "Your browser doesn't support audio recording.",
        "error"
      );
      return;
    }

    try {
      voiceQueryChunks = [];
      voiceQueryStartTime = Date.now();
      voiceQueryStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      voiceQueryRecorder = new MediaRecorder(voiceQueryStream, {
        mimeType: getSupportedMimeType(),
      });

      voiceQueryRecorder.onstart = function () {
        console.log("Voice query recording started");
        voiceQueryStatus.style.display = "block";
        updateVoiceQueryButton("recording");
        hideVoiceQuery();
        showVoiceQueryMessage(
          "Recording your question! Speak clearly into your microphone.",
          "success"
        );

        startVoiceQueryTimer();
      };

      voiceQueryRecorder.ondataavailable = function (event) {
        if (event.data.size > 0) {
          voiceQueryChunks.push(event.data);
        }
      };

      voiceQueryRecorder.onstop = function () {
        console.log("Voice query recording stopped");
        const recordingDuration = Math.round(
          (Date.now() - voiceQueryStartTime) / 1000
        );

        const audioBlob = new Blob(voiceQueryChunks, {
          type: getSupportedMimeType(),
        });
        processVoiceQuery(audioBlob);

        if (voiceQueryStream) {
          voiceQueryStream.getTracks().forEach((track) => track.stop());
        }

        resetVoiceQueryState();
      };

      voiceQueryRecorder.onerror = function (event) {
        console.error("Voice query recorder error:", event.error);
        showVoiceQueryMessage("Recording failed. Please try again.", "error");
        resetVoiceQueryState();
      };

      voiceQueryRecorder.start();
    } catch (error) {
      console.error("Error starting voice query:", error);

      if (error.name === "NotAllowedError") {
        showVoiceQueryMessage(
          "Microphone access denied. Please allow microphone access and try again.",
          "error"
        );
      } else if (error.name === "NotFoundError") {
        showVoiceQueryMessage(
          "No microphone found. Please connect a microphone and try again.",
          "error"
        );
      } else if (error.name === "NotSupportedError") {
        showVoiceQueryMessage(
          "Audio recording not supported in your browser.",
          "error"
        );
      } else {
        showVoiceQueryMessage(
          "Failed to start recording: " + error.message,
          "error"
        );
      }

      resetVoiceQueryState();
    }
  }

  function stopVoiceQuery() {
    if (voiceQueryRecorder && voiceQueryRecorder.state === "recording") {
      voiceQueryRecorder.stop();
      stopVoiceQueryTimer();
      showVoiceQueryMessage(
        "Recording stopped! Preparing to process...",
        "loading"
      );
    } else {
      console.log("No active voice query recording to stop");
      resetVoiceQueryState();
    }
  }

  function startVoiceQueryTimer() {
    if (voiceQueryTimer) {
      let seconds = 0;
      voiceQueryTimer.textContent = "0s";

      voiceQueryTimerInterval = setInterval(() => {
        seconds++;
        voiceQueryTimer.textContent = `${seconds}s`;
      }, 1000);
    }
  }

  function stopVoiceQueryTimer() {
    if (voiceQueryTimerInterval) {
      clearInterval(voiceQueryTimerInterval);
      voiceQueryTimerInterval = null;
    }
  }

  function resetVoiceQueryState() {
    updateVoiceQueryButton("ready");
    if (voiceQueryStatus) voiceQueryStatus.style.display = "none";

    stopVoiceQueryTimer();

    if (voiceQueryStream) {
      voiceQueryStream.getTracks().forEach((track) => track.stop());
      voiceQueryStream = null;
    }
  }

  async function processVoiceQuery(audioBlob) {
    try {
      updateVoiceQueryButton("processing");
      showVoiceQueryProcessing();

      const formData = new FormData();
      const filename = `voice_query_${Date.now()}.wav`;
      formData.append("audio", audioBlob, filename);
      updateProcessingStep("transcribing");

      setTimeout(() => updateProcessingStep("analyzing"), 1000);
      setTimeout(() => updateProcessingStep("generating"), 2000);
      setTimeout(() => updateProcessingStep("speech"), 3000);

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000);

      const response = await fetch(`/agent/chat/${sessionId}`, {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const data = await response.json();

      if (response.ok && data.success) {
        updateProcessingStep("completed");

        // Small delay to show completion
        setTimeout(() => {
          hideVoiceQueryProcessing();
          updateVoiceQueryButton("completed");
          showVoiceQuery(data.transcription, data.llm_response, data.audio_url);
          showVoiceQueryMessage(
            "AI response generated successfully! Audio will auto-play and then start recording for your next question.",
            "success"
          );

          if (
            chatHistoryContainer &&
            chatHistoryContainer.style.display === "block"
          ) {
            loadChatHistory();
          }
        }, 1000);
      } else {
        hideVoiceQueryProcessing();
        updateVoiceQueryButton("ready");
        const errorType = data.error_type || "general_error";
        const errorMessage = data.message || "An unexpected error occurred";

        console.error(`Voice query error (${errorType}):`, errorMessage);
        let userMessage = "";
        switch (errorType) {
          case "api_keys_missing":
            userMessage =
              "🔧 Configuration issue detected. Please contact support.";
            break;
          case "file_error":
            userMessage = "🎤 Audio file issue. Please try recording again.";
            break;
          case "stt_error":
            userMessage =
              "🎯 Having trouble understanding your audio. Please speak clearly and try again.";
            break;
          case "no_speech":
            userMessage =
              "🔇 No speech detected. Please speak clearly into your microphone.";
            break;
          case "llm_error":
            userMessage =
              "🤖 AI thinking process interrupted. Please try again in a moment.";
            break;
          case "tts_error":
            userMessage =
              "🔊 Voice generation issue. The text response is still available.";
            break;
          default:
            userMessage =
              "⚠️ Connection issue. Please check your internet and try again.";
        }

        showVoiceQueryMessage(userMessage, "error");
        if (data.audio_url || data.llm_response || data.transcription) {
          setTimeout(() => {
            showVoiceQuery(
              data.transcription || "",
              data.llm_response || errorMessage,
              data.audio_url
            );
            if (data.audio_url && voiceQueryAudioPlayer) {
              setTimeout(() => {
                voiceQueryAudioPlayer.play().catch((e) => {
                  console.log("Auto-play failed for fallback audio:", e);
                });
              }, 500);
            }
          }, 2000);
        }
        if (["no_speech", "stt_error", "file_error"].includes(errorType)) {
          setTimeout(() => {
            if (
              !voiceQueryRecorder ||
              voiceQueryRecorder.state !== "recording"
            ) {
              console.log("Auto-restarting recording after error...");
              updateVoiceQueryButton("ready");
              startVoiceQuery();
            }
          }, 3000);
        }
      }
    } catch (error) {
      console.error("Voice query processing error:", error);
      hideVoiceQueryProcessing();
      updateVoiceQueryButton("ready");

      if (error.name === "TypeError" && error.message.includes("fetch")) {
        showVoiceQueryMessage(
          "🌐 Network connection error. Please check your internet connection and try again.",
          "error"
        );
      } else if (error.name === "AbortError") {
        showVoiceQueryMessage(
          "⏱️ Request timed out. Please try again.",
          "error"
        );
      } else {
        showVoiceQueryMessage(`❌ Unexpected error: ${error.message}`, "error");
      }
      setTimeout(() => {
        if (!voiceQueryRecorder || voiceQueryRecorder.state !== "recording") {
          console.log("Auto-restarting recording after network error...");
          updateVoiceQueryButton("ready");
          startVoiceQuery();
        }
      }, 4000);
    }
  }

  function showVoiceQuery(transcription, llmResponse, audioUrl) {
    if (
      voiceQueryContainer &&
      voiceQueryTranscription &&
      voiceQueryLLMResponse &&
      voiceQueryAudioPlayer
    ) {
      voiceQueryTranscription.innerHTML = transcription;
      try {
        if (typeof marked !== "undefined") {
          marked.setOptions({
            breaks: true,
            gfm: true,
            sanitize: false,
            highlight: function (code, lang) {
              if (
                typeof hljs !== "undefined" &&
                lang &&
                hljs.getLanguage(lang)
              ) {
                try {
                  return hljs.highlight(code, { language: lang }).value;
                } catch (err) {}
              }
              return code;
            },
          });
          const markdownHtml = marked.parse(llmResponse);
          voiceQueryLLMResponse.innerHTML = markdownHtml;
          if (typeof hljs !== "undefined") {
            voiceQueryLLMResponse
              .querySelectorAll("pre code")
              .forEach((block) => {
                hljs.highlightElement(block);
              });
          }
        } else {
          voiceQueryLLMResponse.innerHTML = llmResponse.replace(/\n/g, "<br>");
        }
      } catch (error) {
        console.error("Markdown parsing error:", error);
        voiceQueryLLMResponse.innerHTML = llmResponse.replace(/\n/g, "<br>");
      }
      const responseAudioSection = document.querySelector(
        ".response-audio-section"
      );
      if (responseAudioSection) {
        responseAudioSection.style.display = "none";
      }

      voiceQueryAudioPlayer.src = audioUrl;
      voiceQueryAudioPlayer.style.display = "none";
      voiceQueryContainer.style.display = "block";
      voiceQueryContainer.scrollIntoView({ behavior: "smooth" });
      setTimeout(() => {
        voiceQueryAudioPlayer.play().catch((e) => {
          console.log("Auto-play failed (browser policy):", e);
        });
      }, 500);
    }
  }

  function hideVoiceQuery() {
    if (voiceQueryContainer) {
      voiceQueryContainer.style.display = "none";
    }
    if (voiceQueryAudioPlayer && voiceQueryAudioPlayer.src) {
      voiceQueryAudioPlayer.src = "";
    }
    if (voiceQueryTranscription) {
      voiceQueryTranscription.innerHTML = "";
    }
    if (voiceQueryLLMResponse) {
      voiceQueryLLMResponse.innerHTML = "";
    }
  }

  function showVoiceQueryMessage(message, type) {
    if (voiceQueryMessageDisplay) {
      voiceQueryMessageDisplay.style.display = "flex";

      if (type === "loading") {
        voiceQueryMessageDisplay.innerHTML = `
          <div class="${type}-message">
            <div class="loading-spinner"></div>
            ${message}
          </div>
        `;
      } else {
        voiceQueryMessageDisplay.innerHTML = `
          <div class="${type}-message">
            ${message}
          </div>
        `;
      }

      // Auto-hide success and error messages after different durations
      if (type === "success") {
        setTimeout(() => {
          voiceQueryMessageDisplay.innerHTML = "";
          voiceQueryMessageDisplay.style.display = "none";
        }, 5000);
      } else if (type === "error") {
        setTimeout(() => {
          voiceQueryMessageDisplay.innerHTML = "";
          voiceQueryMessageDisplay.style.display = "none";
        }, 8000); // Show errors a bit longer
      }
    }
  }

  function showVoiceQueryProcessing() {
    if (voiceQueryMessageDisplay) {
      voiceQueryMessageDisplay.style.display = "flex";
      voiceQueryMessageDisplay.innerHTML = `
        <div class="processing-container">
          <div class="processing-title">🤖 AI is processing your question...</div>
          <div class="processing-steps">
            <div class="processing-step active" id="step-transcribing">
              <div class="step-icon loading"></div>
              <span>Transcribing audio</span>
            </div>
            <div class="processing-step" id="step-analyzing">
              <div class="step-icon"></div>
              <span>Analyzing question</span>
            </div>
            <div class="processing-step" id="step-generating">
              <div class="step-icon"></div>
              <span>Generating response</span>
            </div>
            <div class="processing-step" id="step-speech">
              <div class="step-icon"></div>
              <span>Creating speech</span>
            </div>
          </div>
        </div>
      `;
    }
  }

  function updateProcessingStep(currentStep) {
    const steps = {
      transcribing: ["step-transcribing"],
      analyzing: ["step-transcribing", "step-analyzing"],
      generating: ["step-transcribing", "step-analyzing", "step-generating"],
      speech: [
        "step-transcribing",
        "step-analyzing",
        "step-generating",
        "step-speech",
      ],
      completed: [
        "step-transcribing",
        "step-analyzing",
        "step-generating",
        "step-speech",
      ],
    };

    // Reset all steps
    document.querySelectorAll(".processing-step").forEach((step) => {
      step.classList.remove("active", "completed");
      const icon = step.querySelector(".step-icon");
      icon.classList.remove("loading", "completed");
    });

    const activeSteps = steps[currentStep] || [];

    activeSteps.forEach((stepId, index) => {
      const stepElement = document.getElementById(stepId);
      const icon = stepElement?.querySelector(".step-icon");

      if (index < activeSteps.length - 1 || currentStep === "completed") {
        stepElement?.classList.add("completed");
        icon?.classList.add("completed");
      } else {
        // Current active step
        stepElement?.classList.add("active");
        icon?.classList.add("loading");
      }
    });
  }

  function hideVoiceQueryProcessing() {
    if (voiceQueryMessageDisplay) {
      voiceQueryMessageDisplay.innerHTML = "";
      voiceQueryMessageDisplay.style.display = "none";
    }
  }

  let audioStreamSocket;
  let audioStreamRecorder;
  let audioStreamChunks = [];
  let audioStreamStream;
  let isStreaming = false;
  
  // Audio streaming variables for base64 chunks
  let audioBase64Chunks = [];
  let totalAudioChunks = 0;
  let totalAudioSize = 0;
  
  // Audio playback variables (based on Murf's streaming reference)
  let audioContext = null;
  let audioChunks = []; // Store PCM audio chunks for playback
  let playheadTime = 0;
  let isPlaying = false;
  let wavHeaderSet = true;
  const SAMPLE_RATE = 44100;

  const audioStreamBtn = document.getElementById("audioStreamBtn");
  const audioStreamStatus = document.getElementById("audioStreamStatus");
  const streamingStatusLog = document.getElementById("streamingStatusLog");
  const connectionStatus = document.getElementById("connectionStatus");
  const streamingSessionId = document.getElementById("streamingSessionId");
  
  if (audioStreamBtn) {
    audioStreamBtn.addEventListener("click", toggleAudioStreaming);
  }

  async function toggleAudioStreaming() {
    if (!isStreaming) {
      await startAudioStreaming();
    } else {
      await stopAudioStreaming();
    }
  }

  function resetStreamingState() {
    // Reset audio streaming variables
    audioBase64Chunks = [];
    totalAudioChunks = 0;
    totalAudioSize = 0;
    
    // Reset audio playback state
    resetAudioPlayback();
    
    // Hide previous streaming UI elements
    const elementsToHide = [
      'llmStreamingArea',
      'ttsStreamingArea', 
      'streamingSummaryArea',
      'noSpeechArea'
    ];
    
    elementsToHide.forEach(id => {
      const element = document.getElementById(id);
      if (element) {
        element.style.display = 'none';
      }
    });
    
    console.log("🔄 Streaming state reset - ready for new session");
  }

  async function startAudioStreaming() {
    try {
      console.log("Starting audio streaming...");
      
      // Reset streaming state and UI
      resetStreamingState();
      
      updateConnectionStatus("connecting", "Connecting...");

      // Clear any previous transcriptions
      clearPreviousTranscriptions();

      // Connect to WebSocket
      audioStreamSocket = new WebSocket(`ws://localhost:8000/ws/audio-stream`);

      audioStreamSocket.onopen = function (event) {
        console.log("Audio streaming WebSocket connected");
        updateConnectionStatus("connected", "Connected");
        updateStreamingStatus("Connected to server", "success");
      };

      audioStreamSocket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log("WebSocket message:", data);

        if (data.type === "audio_stream_ready") {
          updateStreamingStatus(
            `Ready to stream audio with transcription. Session: ${data.session_id}`,
            "info"
          );
          streamingSessionId.textContent = `Session: ${data.session_id}`;
          if (data.transcription_enabled) {
            updateStreamingStatus("🎙️ Real-time transcription enabled", "success");
          }
          startRecordingForStreaming();
        } else if (data.type === "chunk_ack") {
          updateStreamingStatus(
            `Chunk ${data.chunk_number} sent (${data.chunk_size} bytes)`,
            "success"
          );
        } else if (data.type === "command_response") {
          updateStreamingStatus(data.message, "info");
        } else if (data.type === "transcription_ready") {
          updateStreamingStatus("🎯 " + data.message, "success");
        } else if (data.type === "final_transcript") {
          // Display final transcription prominently only if we have text
          if (data.text && data.text.trim()) {
            updateStreamingStatus(`🎙️ FINAL: "${data.text}"`, "recording");
          }
        } else if (data.type === "partial_transcript") {
          // Show partial transcripts in real-time for feedback
          if (data.text && data.text.trim()) {
            updateStreamingStatus(`🎙️ ${data.text}`, "info");
          }
        } else if (data.type === "turn_end") {
          // Handle turn detection - user has stopped talking
          updateStreamingStatus("🛑 Turn ended - User stopped talking", "success");
          if (data.final_transcript && data.final_transcript.trim()) {
            updateStreamingStatus(`✅ TURN COMPLETE: "${data.final_transcript}"`, "success");
          } else {
            updateStreamingStatus("⚠️ Turn ended but no speech detected", "warning");
            showNoSpeechMessage();
          }
        } else if (data.type === "transcription_complete") {
          if (data.text && data.text.trim()) {
            updateStreamingStatus(`✅ COMPLETE TRANSCRIPTION: "${data.text}"`, "success");
            // showCompleteTranscription(data.text);
          } else {
            updateStreamingStatus("⚠️ No speech detected in recording", "warning");
            showNoSpeechMessage();
          }
        } else if (data.type === "streaming_complete") {
          updateStreamingStatus(`🎯 ${data.message}`, "success");
          if (data.transcription && data.transcription.trim()) {
            // Backend transcription processing continues silently
          } else {
            updateStreamingStatus("⚠️ Recording completed but no speech was detected", "warning");
            showNoSpeechMessage();
          }
        } else if (data.type === "transcription_error") {
          updateStreamingStatus("❌ Transcription error: " + data.message, "error");
        } else if (data.type === "transcription_stopped") {
          updateStreamingStatus("🛑 " + data.message, "warning");
        } else if (data.type === "llm_streaming_start") {
          // LLM is starting to generate response
          updateStreamingStatus(`🤖 ${data.message}`, "info");
          // Reset audio chunk collection for new response
          audioBase64Chunks = [];
          totalAudioChunks = 0;
          totalAudioSize = 0;
          resetAudioPlayback();
          displayLLMStreamingStart(data.user_message);
        } else if (data.type === "llm_streaming_chunk") {
          // Display LLM text chunks as they arrive
          displayLLMTextChunk(data.chunk, data.accumulated_length);
        } else if (data.type === "tts_streaming_start") {
          updateStreamingStatus(`🎵 ${data.message}`, "info");
          displayTTSStreamingStart();
        } else if (data.type === "tts_audio_chunk") {
          // Handle audio base64 chunks from TTS
          handleAudioChunk(data);
        } else if (data.type === "tts_status") {
          updateStreamingStatus(`🎵 TTS Status: ${JSON.stringify(data.data)}`, "info");
        } else if (data.type === "llm_streaming_complete") {
          updateStreamingStatus(`✅ ${data.message}`, "success");
          displayStreamingComplete(data);
        } else if (data.type === "llm_streaming_error") {
          updateStreamingStatus(`❌ ${data.message}`, "error");
        } else if (data.type === "tts_streaming_error") {
          updateStreamingStatus(`❌ ${data.message}`, "error");
        }
      };

      audioStreamSocket.onerror = function (error) {
        console.error("WebSocket error:", error);
        updateConnectionStatus("error", "Connection Error");
        updateStreamingStatus("WebSocket connection error", "error");
      };

      audioStreamSocket.onclose = function (event) {
        console.log("WebSocket connection closed");
        updateConnectionStatus("disconnected", "Disconnected");
        updateStreamingStatus("Connection closed", "warning");
      };
    } catch (error) {
      console.error("Error starting audio streaming:", error);
      updateConnectionStatus("error", "Error");
      updateStreamingStatus(
        "Error starting streaming: " + error.message,
        "error"
      );
    }
  }

  async function startRecordingForStreaming() {
    try {
      audioStreamStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,  // 16kHz for AssemblyAI
          channelCount: 1,    // Mono
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        },
      });

      const audioContext = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 16000
      });
      
      const source = audioContext.createMediaStreamSource(audioStreamStream);
      const processor = audioContext.createScriptProcessor(4096, 1, 1);
      
      processor.onaudioprocess = function(e) {
        if (audioStreamSocket && audioStreamSocket.readyState === WebSocket.OPEN) {
          const inputData = e.inputBuffer.getChannelData(0);
          const pcmData = new Int16Array(inputData.length);
          for (let i = 0; i < inputData.length; i++) {
            pcmData[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32767));
          }
          audioStreamSocket.send(pcmData.buffer);
        }
      };

      source.connect(processor);
      processor.connect(audioContext.destination);
      
      // Store references for cleanup
      audioStreamRecorder = {
        stop: () => {
          processor.disconnect();
          source.disconnect();
          audioContext.close();
        }
      };
      
      isStreaming = true;
      if (audioStreamBtn) {
        audioStreamBtn.innerHTML =
          '<span class="btn-icon">⏹️</span><span class="btn-text">Stop Audio Streaming</span>';
        audioStreamBtn.className = "btn danger";
        audioStreamBtn.setAttribute("data-state", "recording");
      }

      updateConnectionStatus("recording", "Recording & Streaming");
      updateStreamingStatus("Recording and streaming audio...", "recording");
      if (
        audioStreamSocket &&
        audioStreamSocket.readyState === WebSocket.OPEN
      ) {
        audioStreamSocket.send("start_streaming");
      }
    } catch (error) {
      console.error("Error starting recording for streaming:", error);
      updateConnectionStatus("error", "Recording Error");
      updateStreamingStatus(
        "Error starting recording: " + error.message,
        "error"
      );
    }
  }

  async function stopAudioStreaming() {
    try {
      isStreaming = false;
      
      // Stop the audio recording (either MediaRecorder or custom processor)
      if (audioStreamRecorder) {
        if (typeof audioStreamRecorder.stop === 'function') {
          audioStreamRecorder.stop();
        }
        audioStreamRecorder = null;
      }

      // Stop media stream
      if (audioStreamStream) {
        audioStreamStream.getTracks().forEach((track) => track.stop());
        audioStreamStream = null;
      }
      if (
        audioStreamSocket &&
        audioStreamSocket.readyState === WebSocket.OPEN
      ) {
        audioStreamSocket.send("stop_streaming");
      }

      // Close WebSocket after a short delay to allow final messages
      setTimeout(() => {
        if (audioStreamSocket) {
          audioStreamSocket.close();
        }
      }, 1000);

      // Update UI
      if (audioStreamBtn) {
        audioStreamBtn.innerHTML =
          '<span class="btn-icon">🎤</span><span class="btn-text">Start Audio Streaming</span>';
        audioStreamBtn.className = "btn secondary";
        audioStreamBtn.setAttribute("data-state", "ready");
      }

      updateConnectionStatus("disconnected", "Disconnected");
      updateStreamingStatus("Audio streaming stopped", "info");
    } catch (error) {
      console.error("Error stopping audio streaming:", error);
      updateStreamingStatus(
        "Error stopping streaming: " + error.message,
        "error"
      );
    }
  }

  function updateConnectionStatus(status, text) {
    if (connectionStatus) {
      connectionStatus.className = `status-badge ${status}`;
      connectionStatus.textContent = text;
    }
  }

  function updateStreamingStatus(message, type) {
    if (streamingStatusLog && audioStreamStatus) {
      audioStreamStatus.style.display = "block";

      const statusEntry = document.createElement("div");
      statusEntry.className = `streaming-status ${type}`;
      statusEntry.innerHTML = `
        <strong>${new Date().toLocaleTimeString()}</strong>: ${message}
      `;

      streamingStatusLog.appendChild(statusEntry);
      streamingStatusLog.scrollTop = streamingStatusLog.scrollHeight;
    }
    console.log(`[Audio Stream] ${message}`);
  }

  // Function to clear previous transcription displays
  function clearPreviousTranscriptions() {
    // Clear live transcription area
    const liveArea = document.getElementById('liveTranscriptionArea');
    if (liveArea) {
      liveArea.style.display = 'none';
      const transcriptionText = document.getElementById('transcriptionText');
      if (transcriptionText) {
        transcriptionText.innerHTML = '';
      }
    }
    
    // Clear complete transcription area
    const completeArea = document.getElementById('completeTranscriptionArea');
    if (completeArea) {
      completeArea.style.display = 'none';
    }
    
    // Clear no speech area
    const noSpeechArea = document.getElementById('noSpeechArea');
    if (noSpeechArea) {
      noSpeechArea.style.display = 'none';
    }
  }

  // Function to display transcription on the UI (disabled for clean UI)
  function displayTranscriptionOnUI(text, isFinal) {
    // Transcription processing happens in backend, UI display disabled
    console.log('Transcription processed (UI hidden):', text, 'Final:', isFinal);
  }

  // Function to show complete final transcription (disabled for clean UI)
  function showCompleteTranscription(text) {
    // Transcription processing happens in backend, UI display disabled
    console.log('Complete transcription processed (UI hidden):', text);
  }

  // Function to show a message when no speech is detected (disabled for clean UI)
  function showNoSpeechMessage() {
    // Speech detection happens in backend, UI display disabled
    console.log('No speech detected (UI hidden)');
  }

  // Function to handle audio base64 chunks from TTS
  function handleAudioChunk(audioData) {
    // Store the base64 audio chunk
    audioBase64Chunks.push(audioData.audio_base64);
    totalAudioChunks++;
    totalAudioSize += audioData.chunk_size;
    
    // Log acknowledgement to console
    console.log(`🎵 Audio chunk received: #${audioData.chunk_number}, Size: ${audioData.chunk_size} bytes, Total chunks: ${totalAudioChunks}`);
    console.log(`📊 Accumulated ${audioBase64Chunks.length} audio chunks, Total size: ${totalAudioSize} bytes`);
    
    // Play the audio chunk as it arrives for seamless streaming
    playAudioChunk(audioData.audio_base64);
    
    // Update UI with audio streaming progress
    updateStreamingStatus(
      `🎵 Audio chunk #${audioData.chunk_number} received (${audioData.chunk_size} bytes) - Total: ${totalAudioChunks} chunks, ${totalAudioSize} bytes`,
      "success"
    );
    
    // Display audio chunk in UI
    displayAudioChunkReceived(audioData);
    
    // If this is the final chunk
    if (audioData.is_final) {
      updateStreamingStatus(
        `✅ Audio streaming complete! Received ${totalAudioChunks} chunks totaling ${totalAudioSize} bytes`,
        "success"
      );
      
      // Set a timeout to hide the playback indicator after the audio finishes
      setTimeout(() => {
        if (!isPlaying && audioChunks.length === 0) {
          updatePlaybackStatus('Audio streaming complete!');
          setTimeout(() => {
            hideAudioPlaybackIndicator();
          }, 2000);
        }
      }, 1000);
      
      displayAudioStreamingComplete();
    }
  }

  // Function to display LLM streaming start
  function displayLLMStreamingStart(userMessage) {
    let llmArea = document.getElementById('llmStreamingArea');
    
    if (!llmArea) {
      llmArea = document.createElement('div');
      llmArea.id = 'llmStreamingArea';
      llmArea.className = 'llm-streaming-area';
      llmArea.innerHTML = `
        <h4>🤖 AI Response Generation</h4>
        <div class="user-query">
          <strong>Your question:</strong> "${userMessage}"
        </div>
        <div class="llm-response">
          <strong>AI Response:</strong>
          <div id="llmResponseText" class="llm-response-text"></div>
        </div>
      `;
      
      // Insert after the complete transcription area or streaming status
      const completeArea = document.getElementById('completeTranscriptionArea');
      const statusContainer = document.getElementById('audioStreamStatus');
      const insertAfter = completeArea || statusContainer;
      
      if (insertAfter) {
        insertAfter.parentNode.insertBefore(llmArea, insertAfter.nextSibling);
      }
    }
    
    llmArea.style.display = 'block';
    
    // Clear previous response
    const responseText = document.getElementById('llmResponseText');
    if (responseText) {
      responseText.innerHTML = '<em>Generating response...</em>';
      responseText.setAttribute('data-raw-text', '');
    }
  }

  // Function to display LLM text chunks
  function displayLLMTextChunk(chunk, accumulatedLength) {
    const responseText = document.getElementById('llmResponseText');
    if (responseText) {
      // Append the new chunk
      let currentText = responseText.getAttribute('data-raw-text') || '';
      if (currentText === 'Generating response...') {
        currentText = '';
      }
      
      // Accumulate the raw text
      const newText = currentText + chunk;
      responseText.setAttribute('data-raw-text', newText);
      
      // Parse as Markdown and display
      try {
        if (typeof marked !== 'undefined') {
          const markdownHtml = marked.parse(newText);
          responseText.innerHTML = markdownHtml;
          
          // Apply syntax highlighting if available
          if (typeof hljs !== 'undefined') {
            responseText.querySelectorAll('pre code').forEach((block) => {
              hljs.highlightElement(block);
            });
          }
        } else {
          // Fallback to simple line break replacement
          responseText.innerHTML = newText.replace(/\n/g, '<br>');
        }
      } catch (error) {
        console.warn('Markdown parsing error:', error);
        responseText.innerHTML = newText.replace(/\n/g, '<br>');
      }
      
      // Scroll to bottom
      responseText.scrollTop = responseText.scrollHeight;
    }
  }

  // Function to display TTS streaming start
  function displayTTSStreamingStart() {
    let ttsArea = document.getElementById('ttsStreamingArea');
    
    if (!ttsArea) {
      ttsArea = document.createElement('div');
      ttsArea.id = 'ttsStreamingArea';
      ttsArea.className = 'tts-streaming-area';
      ttsArea.innerHTML = `
        <h4>🎵 Audio Generation</h4>
        <div class="audio-chunks-info">
          <div id="audioChunksProgress" class="audio-progress">
            <span class="chunk-count">Chunks received: <strong id="chunkCount">0</strong></span>
            <span class="total-size">Total size: <strong id="totalSize">0 bytes</strong></span>
          </div>
          <div id="audioChunksList" class="audio-chunks-list"></div>
        </div>
      `;
      
      // Insert after the LLM area or streaming status
      const llmArea = document.getElementById('llmStreamingArea');
      const statusContainer = document.getElementById('audioStreamStatus');
      const insertAfter = llmArea || statusContainer;
      
      if (insertAfter) {
        insertAfter.parentNode.insertBefore(ttsArea, insertAfter.nextSibling);
      }
    }
    
    ttsArea.style.display = 'block';
    
    // Reset counters
    const chunkCount = document.getElementById('chunkCount');
    const totalSizeEl = document.getElementById('totalSize');
    const chunksList = document.getElementById('audioChunksList');
    
    if (chunkCount) chunkCount.textContent = '0';
    if (totalSizeEl) totalSizeEl.textContent = '0 bytes';
    if (chunksList) chunksList.innerHTML = '';
  }

  // Function to display audio chunk received
  function displayAudioChunkReceived(audioData) {
    // Update counters
    const chunkCount = document.getElementById('chunkCount');
    const totalSizeEl = document.getElementById('totalSize');
    
    if (chunkCount) chunkCount.textContent = totalAudioChunks.toString();
    if (totalSizeEl) totalSizeEl.textContent = `${totalAudioSize} bytes`;
    
    // Add chunk to list (show only last 5 chunks to avoid UI clutter)
    const chunksList = document.getElementById('audioChunksList');
    if (chunksList) {
      const chunkElement = document.createElement('div');
      chunkElement.className = 'audio-chunk-item';
      chunkElement.innerHTML = `
        <span class="chunk-info">
          Chunk #${audioData.chunk_number}: ${audioData.chunk_size} bytes
          ${audioData.is_final ? '<strong>(FINAL)</strong>' : ''}
        </span>
        <span class="chunk-time">${new Date().toLocaleTimeString()}</span>
      `;
      
      chunksList.appendChild(chunkElement);
      
      // Keep only last 5 chunks visible
      while (chunksList.children.length > 5) {
        chunksList.removeChild(chunksList.firstChild);
      }
      
      // Scroll to bottom
      chunksList.scrollTop = chunksList.scrollHeight;
    }
  }

  // Function to display streaming complete summary
  function displayStreamingComplete(data) {
    let summaryArea = document.getElementById('streamingSummaryArea');
    
    if (!summaryArea) {
      summaryArea = document.createElement('div');
      summaryArea.id = 'streamingSummaryArea';
      summaryArea.className = 'streaming-summary-area';
      
      // Insert after the TTS area or streaming status
      const ttsArea = document.getElementById('ttsStreamingArea');
      const statusContainer = document.getElementById('audioStreamStatus');
      const insertAfter = ttsArea || statusContainer;
      
      if (insertAfter) {
        insertAfter.parentNode.insertBefore(summaryArea, insertAfter.nextSibling);
      }
    }
    
    summaryArea.innerHTML = `
      <h4>✅ Streaming Complete</h4>
      <div class="streaming-summary">
        <div class="summary-item">
          <strong>Complete Response:</strong>
          <div class="final-response" id="finalResponseContent"></div>
        </div>
        <div class="summary-stats">
          <div class="stat-item">
            <span class="stat-label">Response Length:</span>
            <span class="stat-value">${data.total_length} characters</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Audio Chunks:</span>
            <span class="stat-value">${data.audio_chunks_received} chunks</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Total Audio Size:</span>
            <span class="stat-value">${data.total_audio_size} bytes</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Base64 Chunks Collected:</span>
            <span class="stat-value">${audioBase64Chunks.length} chunks</span>
          </div>
        </div>
      </div>
    `;
    
    summaryArea.style.display = 'block';
    
    // Render the final response as Markdown
    const finalResponseElement = document.getElementById('finalResponseContent');
    if (finalResponseElement && data.complete_response) {
      try {
        if (typeof marked !== 'undefined') {
          const markdownHtml = marked.parse(data.complete_response);
          finalResponseElement.innerHTML = markdownHtml;
          
          // Apply syntax highlighting if available
          if (typeof hljs !== 'undefined') {
            finalResponseElement.querySelectorAll('pre code').forEach((block) => {
              hljs.highlightElement(block);
            });
          }
        } else {
          // Fallback to simple line break replacement
          finalResponseElement.innerHTML = data.complete_response.replace(/\n/g, '<br>');
        }
      } catch (error) {
        console.warn('Markdown parsing error in final response:', error);
        finalResponseElement.innerHTML = data.complete_response.replace(/\n/g, '<br>');
      }
    }
    
    // Scroll into view
    summaryArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Function to display audio streaming complete
  function displayAudioStreamingComplete() {
    console.log(`🎉 Audio streaming complete! Collected ${audioBase64Chunks.length} base64 audio chunks:`);
    
    // Log some sample data for verification (first few characters of each chunk)
    audioBase64Chunks.forEach((chunk, index) => {
      console.log(`   Chunk ${index + 1}: ${chunk.substring(0, 50)}... (${chunk.length} characters)`);
    });
    
    console.log(`📊 Total audio data: ${audioBase64Chunks.join('').length} base64 characters`);
  }

  // ==================== AUDIO STREAMING PLAYBACK FUNCTIONS ====================
  // Based on Murf's WebSocket streaming reference implementation
  
  /**
   * Initialize audio context for streaming playback
   */
  function initializeAudioContext() {
    try {
      if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        playheadTime = audioContext.currentTime;
        console.log('🎛️ Audio context initialized for streaming playback');
      }
      return true;
    } catch (error) {
      console.error('❌ Failed to initialize audio context:', error);
      return false;
    }
  }

  /**
   * Convert base64 audio data to PCM Float32 array for Web Audio API playback
   * @param {string} base64 - Base64 encoded audio data
   * @returns {Float32Array} - PCM audio data as Float32 array
   */
  function base64ToPCMFloat32(base64) {
    try {
      let binary = atob(base64);
      const offset = wavHeaderSet ? 44 : 0; // Skip WAV header if present
      
      if (wavHeaderSet) {
        console.log('🎵 WAV header detected in first chunk:', binary.substring(0, 44));
        wavHeaderSet = false; // Only process header once
      }
      
      const length = binary.length - offset;
      const buffer = new ArrayBuffer(length);
      const byteArray = new Uint8Array(buffer);
      
      for (let i = 0; i < byteArray.length; i++) {
        byteArray[i] = binary.charCodeAt(i + offset);
      }

      const view = new DataView(byteArray.buffer);
      const sampleCount = byteArray.length / 2; // 16-bit samples
      const float32Array = new Float32Array(sampleCount);

      for (let i = 0; i < sampleCount; i++) {
        const int16 = view.getInt16(i * 2, true); // Little endian
        float32Array[i] = int16 / 32768; // Convert to float32 range [-1, 1]
      }

      return float32Array;
    } catch (error) {
      console.error('❌ Error converting base64 to PCM:', error);
      return null;
    }
  }

  /**
   * Play audio chunks using Web Audio API for seamless streaming
   */
  function chunkPlay() {
    if (audioChunks.length > 0) {
      const chunk = audioChunks.shift();
      
      if (audioContext.state === "suspended") {
        audioContext.resume();
      }
      
      try {
        const buffer = audioContext.createBuffer(1, chunk.length, SAMPLE_RATE);
        buffer.copyToChannel(chunk, 0);
        
        const source = audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(audioContext.destination);
        
        const now = audioContext.currentTime;
        if (playheadTime < now) {
          playheadTime = now + 0.05; // Add small delay to prevent audio gaps
        }
        
        source.start(playheadTime);
        playheadTime += buffer.duration;
        
        console.log(`🔊 Playing audio chunk: ${chunk.length} samples, duration: ${buffer.duration.toFixed(3)}s`);
        
        // Update playback status
        updatePlaybackStatus(`Playing audio chunk (${chunk.length} samples, ${buffer.duration.toFixed(2)}s)`);
        
        // Continue playing remaining chunks
        if (audioChunks.length > 0) {
          chunkPlay();
        } else {
          isPlaying = false;
          updatePlaybackStatus('Audio streaming paused - waiting for more chunks...');
          console.log('🎵 Audio chunk queue empty, playback paused');
        }
      } catch (error) {
        console.error('❌ Error playing audio chunk:', error);
        isPlaying = false;
        hideAudioPlaybackIndicator();
      }
    }
  }

  /**
   * Process and play individual audio chunk as it arrives
   * @param {string} base64Audio - Base64 encoded audio data
   */
  function playAudioChunk(base64Audio) {
    try {
      // Initialize audio context if not already done
      if (!initializeAudioContext()) {
        return;
      }

      // Show audio playback indicator
      showAudioPlaybackIndicator();

      // Convert base64 to PCM data
      const float32Array = base64ToPCMFloat32(base64Audio);
      if (!float32Array || float32Array.length === 0) {
        console.warn('⚠️ Empty or invalid audio chunk received');
        return;
      }

      console.log(`🎵 Received audio chunk: ${float32Array.length} samples`);
      
      // Add chunk to playback queue
      audioChunks.push(float32Array);

      // Start playback if not already playing and we have enough audio buffered
      if (!isPlaying && (playheadTime <= audioContext.currentTime + 0.1 || audioChunks.length >= 2)) {
        isPlaying = true;
        audioContext.resume().then(() => {
          console.log('🎛️ Starting seamless audio playback');
          chunkPlay();
        });
      }
    } catch (error) {
      console.error('❌ Error in playAudioChunk:', error);
    }
  }

  /**
   * Reset audio streaming playback state
   */
  function resetAudioPlayback() {
    audioChunks = [];
    isPlaying = false;
    wavHeaderSet = true;
    
    if (audioContext) {
      playheadTime = audioContext.currentTime;
    }
    
    // Hide audio playback indicator
    hideAudioPlaybackIndicator();
    
    console.log('🔄 Audio playback state reset');
  }

  /**
   * Show the audio playback indicator with animation
   */
  function showAudioPlaybackIndicator() {
    const playbackContainer = document.getElementById('audioPlaybackStatus');
    if (playbackContainer) {
      playbackContainer.style.display = 'block';
      
      // Update status text
      const statusText = document.getElementById('playbackStatusText');
      if (statusText) {
        statusText.textContent = 'Audio is streaming and playing...';
      }
    }
  }

  /**
   * Hide the audio playback indicator
   */
  function hideAudioPlaybackIndicator() {
    const playbackContainer = document.getElementById('audioPlaybackStatus');
    if (playbackContainer) {
      playbackContainer.style.display = 'none';
    }
  }

  /**
   * Update playback status text
   */
  function updatePlaybackStatus(text) {
    const statusText = document.getElementById('playbackStatusText');
    if (statusText) {
      statusText.textContent = text;
    }
  }
});
