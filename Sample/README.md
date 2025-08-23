# 30 Days of Voice Agents - Voice Interaction Platform

A modern conversational AI voice agent built with FastAPI, featuring real-time audio playback, live transcription, streaming LLM responses with **Markdown rendering**, and WebSocket-based TTS audio delivery from Murf AI. This implementation demonstrates complete voice-to-voice conversations with seamless audio playback and rich text formatting.

## ✨ Key Features

### 🎵 **Audio & Text Processing Pipeline**
- **WebSocket Audio Playback**: Real-time TTS audio delivery with seamless Web Audio API integration
- **Live Speech Recognition**: AssemblyAI Universal Streaming for instant transcription
- **Streaming LLM Responses**: Google Gemini with real-time text generation and **Markdown rendering**
- **WebSocket TTS Integration**: Murf AI WebSocket TTS with efficient audio playback
- **Rich Text Rendering**: Markdown support for formatted AI responses with syntax highlighting
- **Real-time Feedback**: Live connection status and audio processing indicators

### 🎙️ **Voice Interface**
- **WebSocket Streaming**: Real-time audio and text communication
- **Intelligent UI**: Dynamic status updates and connection monitoring with proper text alignment
- **Session Management**: Persistent conversation history and context
- **Responsive Design**: Clean, modern interface optimized for voice interactions

### 🤖 **AI Processing Pipeline**
- **Real-Time Transcription**: Live speech-to-text with AssemblyAI streaming
- **Context-Aware AI**: Streaming responses with conversation memory and Markdown formatting
- **Turn Detection**: Automatic end-of-turn detection for natural conversations
- **Live Response Display**: Character-by-character AI response generation with rich text support
- **Audio Generation**: Real-time TTS with WebSocket audio delivery

### 🔄 **Enhanced Data Flow**
- **WebSocket Communication**: Efficient real-time bidirectional communication
- **Audio Playback**: Direct TTS audio streaming with Web Audio API integration
- **Session Persistence**: MongoDB storage for conversation history
- **Audio File Archival**: Automatic saving of streaming sessions
- **Real-Time Monitoring**: Live connection status and performance metrics
- **Markdown Rendering**: Rich text formatting for AI responses with syntax highlighting

## 🏗️ Architecture Overview

### Core Components

**Backend Services:**
- `main.py` - FastAPI application with WebSocket endpoints
- `assemblyai_streaming_service.py` - Real-time speech recognition
- `murf_websocket_service.py` - Streaming TTS with WebSocket audio delivery
- `llm_service.py` - Streaming language model responses
- `database_service.py` - Session and conversation persistence

**Frontend Interface:**
- `templates/index.html` - Modern voice interface with Markdown support
- `static/app.js` - WebSocket client with audio playback and text rendering
- `static/style.css` - Clean UI design with proper text alignment and streaming styles

**Audio Processing:**
- Real-time 16kHz PCM audio capture
- WebSocket audio transmission
- Audio playback and Markdown text rendering
- Console logging of audio data reception

## 🔧 How It Works

### Streaming Audio Pipeline

1. **WebSocket Connection**: Client connects to `/ws/audio-stream`
2. **Audio Capture**: Browser captures 16kHz PCM audio in real-time
3. **Live Transcription**: AssemblyAI processes speech as it arrives
4. **AI Response**: Gemini generates streaming text responses with Markdown formatting
5. **TTS Streaming**: Murf WebSocket converts text to audio data
6. **Audio Delivery**: TTS audio sent to client via WebSocket for immediate playback
7. **Client Processing**: JavaScript renders Markdown text and plays audio seamlessly
8. **Real-time Display**: Live text streaming with proper formatting and audio feedback

### WebSocket Audio Integration

The application implements a complete voice interaction solution where:
- TTS audio is generated in real-time by Murf WebSocket service
- Audio data is transmitted via WebSocket to the client
- Client plays audio immediately using Web Audio API
- Text responses are rendered with Markdown support including syntax highlighting
- Clean UI with proper text alignment for streaming content
- Seamless voice-to-voice conversation with rich text formatting

## 📁 Project Structure

```
30 Days of Voice Agents/
├── main.py                           # FastAPI app with WebSocket streaming
├── requirements.txt                  # Dependencies
├── .env                             # API keys and configuration
├── models/
│   └── schemas.py                   # Data models
├── services/
│   ├── assemblyai_streaming_service.py  # Real-time STT
│   ├── murf_websocket_service.py       # Streaming TTS with base64 output
│   ├── llm_service.py                  # Streaming LLM responses
│   ├── stt_service.py                  # Traditional STT
│   ├── tts_service.py                  # Traditional TTS
│   └── database_service.py             # MongoDB operations
├── utils/
│   ├── logging_config.py               # Logging setup
│   ├── constants.py                    # App constants
│   └── json_utils.py                   # JSON utilities
├── templates/
│   └── index.html                      # Dual-mode interface
├── static/
│   ├── app.js                          # WebSocket client with audio handling
│   └── style.css                       # Streaming UI styles
├── streamed_audio/                     # Saved streaming sessions
└── voice_agent.log                     # Application logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Murf AI API key
- AssemblyAI API key  
- Google Gemini API key
- Modern browser with microphone support and JavaScript enabled for Markdown rendering

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   
   Create `.env` file:
   ```bash
   MURF_API_KEY=your_murf_api_key
   ASSEMBLYAI_API_KEY=your_assemblyai_key
   GEMINI_API_KEY=your_gemini_key
   MURF_VOICE_ID=en-IN-aarav
   MONGODB_URL=mongodb://localhost:27017
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the interface**
   ```
   http://localhost:8000
   ```

## 📝 Usage Guide

### Audio Streaming Mode

1. **Start Streaming**: Click "Start Audio Streaming" in the streaming section
2. **Connect**: WebSocket establishes connection to `/ws/audio-stream`
3. **Begin Recording**: Click to start real-time audio capture
4. **Watch Live Transcription**: See your words appear as you speak
5. **View AI Response**: Watch character-by-character response generation with Markdown formatting
6. **Listen to Audio**: Hear AI responses played back automatically via Web Audio API
7. **Track Session**: Monitor connection status and streaming metrics

### Audio & Text Processing

The application provides seamless voice interaction with:
```javascript
� Recording started...
📝 Transcription: "Hello, how are you today?"
🤖 AI Response streaming...
🎵 Audio playback started
✅ Response complete! Markdown rendered with formatting
```

### Audio Data Structure

Base64 audio chunks are accumulated in JavaScript:
```javascript
// Audio chunks stored in array
audioBase64Chunks = [
  "UklGRpAAAgBXQVZFZm10IBAAAAABAAEAgLsAAACAtwAA...",
  "AQAIAAAAAAAEABAAAAAABAAAAAAABAAAAAAAAAAAAAA...",
  // ... more chunks
]

// Total metadata tracked
totalAudioChunks = 15;
totalAudioSize = 15360; // bytes
```

## � Technical Details

### WebSocket Message Types

**Audio Streaming Messages:**
- `llm_streaming_start` - AI response generation begins
- `llm_streaming_chunk` - Character-by-character AI text with Markdown support
- `tts_streaming_start` - Audio generation begins  
- `tts_audio_chunk` - Audio data with playback metadata
- `llm_streaming_complete` - Complete response with audio summary

**Text Rendering Features:**
```json
{
  "type": "llm_streaming_chunk",
  "text": "Here's a **bold** example with `code` formatting",
  "markdown_enabled": true,
  "syntax_highlighting": true,
  "timestamp": "2025-08-22T10:30:45.123Z"
}
```

### Audio & Text Processing Features

- **Real-Time Audio Playback**: Immediate TTS audio delivery with Web Audio API
- **Markdown Rendering**: Rich text formatting with syntax highlighting support
- **Live Text Streaming**: Character-by-character response display with proper alignment
- **Seamless Integration**: Synchronized audio and text delivery
- **Session Persistence**: All conversation data saved to database and files
- **Error Handling**: Robust error recovery for streaming interruptions

## 🎯 Key Implementation Features

### Base64 Audio Streaming
- Direct base64 audio chunk delivery via WebSocket
- No automatic audio element playback
- Client-side accumulation and logging
- Real-time acknowledgment of data reception
- Complete audio data collection for processing

### Real-Time UI Updates
- Live transcription display as user speaks
- Character-by-character AI response rendering
- Dynamic audio chunk progress tracking  
- Real-time connection status monitoring
- Streaming session metrics and statistics

### Production-Ready Architecture
- WebSocket connection management and resilience
- Comprehensive error handling and recovery
- Session-based conversation persistence
- Automatic file archival and organization
- Performance monitoring and optimization

## 📊 Performance Metrics

The application tracks and displays:
- Audio chunks received and accumulated
- Total base64 data size and transfer rates
- WebSocket connection health and latency
- Streaming session duration and statistics
- Real-time transcription accuracy and speed
- AI response generation timing and throughput

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Audio processing optimization
- Enhanced UI/UX for streaming interface
- Additional TTS service integrations
- Performance monitoring enhancements
- Mobile device compatibility

## 📄 License

MIT License - feel free to use and modify for your projects.
- **Streaming LLM Responses**: Google Gemini with live text generation and accumulation
- **Murf WebSocket TTS Integration**: Real-time text-to-speech streaming with base64 audio chunks
- **Live Session Management**: Real-time conversation tracking with MongoDB persistence
- **Complete Voice-to-Voice Pipeline**: End-to-end streaming from voice input to audio response
- **Concurrent Processing**: Simultaneous audio streaming, transcription, AI processing, and voice generation

#### **📋 Enhanced Models Layer** (`models/`)
- **Streaming-Aware Schemas**: Extended Pydantic models for real-time data validation
- **WebSocket Message Types**: Structured message schemas for streaming communication
- **Real-Time Error Handling**: Enhanced error types for streaming scenarios

#### **🛠️ Advanced Services Layer** (`services/`)
- **AssemblyAI Streaming Service**: NEW real-time transcription with turn detection
- **Enhanced LLM Service**: Streaming response generation with context preservation
- **Murf WebSocket Service**: NEW real-time text-to-speech streaming with base64 audio output
- **Traditional Services**: Maintained for backward compatibility and fallback
- **Connection Management**: WebSocket lifecycle and connection pooling

#### **🔧 Expanded Utils Layer** (`utils/`)
- **Streaming Logging**: Enhanced logging for real-time operations
- **Performance Constants**: Streaming-specific configuration and thresholds
- **Real-Time JSON Handling**: Optimized for streaming data serialization

#### **🎯 Dual-Mode Application** (`main.py`)
- **Traditional Endpoint**: `/agent/chat/{session_id}` for file-based processing
- **Streaming Endpoint**: `/ws/audio-stream` for real-time voice conversations
- **Connection Management**: Advanced WebSocket connection tracking
- **Service Orchestration**: Coordinated streaming service integration

### Streaming Voice Agent Workflow

#### **🔴 Real-Time Streaming Mode (NEW)**
1. **WebSocket Connection**: Client connects to `/ws/audio-stream` for live streaming
2. **Live Audio Capture**: 16kHz PCM audio streaming with optimized chunk processing
3. **Real-Time Transcription**: AssemblyAI Universal Streaming provides instant text feedback
4. **Streaming LLM Processing**: Google Gemini generates responses in real-time chunks
5. **Live TTS Streaming**: Murf WebSocket integration delivers streaming base64 audio chunks
6. **Live Response Display**: Text appears character by character as the AI thinks
7. **Real-Time Audio Output**: Base64 audio chunks printed to console for voice synthesis
8. **Automatic Session Saving**: All streaming sessions saved to MongoDB and audio files

#### **🔵 Traditional Mode** (Enhanced)
1. **Smart Button Interface**: Improved single-button control with streaming fallback
2. **File-Based Processing**: Complete audio upload and processing pipeline
3. **Enhanced AI Pipeline**: Upgraded with streaming service integration
4. **Backward Compatibility**: Full support for existing voice agent functionality

### Advanced Features

#### **🎙️ Real-Time Audio Processing**
- **16kHz PCM Streaming**: Optimized audio format for AssemblyAI Universal Streaming
- **Intelligent Chunking**: 4096-sample audio chunks with seamless processing
- **Echo Cancellation**: Built-in audio enhancement for clear voice capture
- **Adaptive Bitrate**: Dynamic audio quality adjustment based on connection

#### **⚡ Live AI Responses**
- **Streaming Text Generation**: Watch AI responses appear in real-time
- **Context Preservation**: Full conversation history maintained during streaming
- **Turn-Based Processing**: Intelligent detection of when user stops speaking
- **Response Accumulation**: Complete responses saved alongside streaming chunks
- **Real-Time TTS Integration**: Streaming text sent to Murf WebSocket for live audio generation
- **Base64 Audio Streaming**: Console output displays real-time base64 encoded audio chunks

#### **📊 Real-Time Monitoring**
- **Connection Status**: Live WebSocket connection monitoring
- **Streaming Metrics**: Real-time bytes transferred, chunks processed, session duration
- **Performance Tracking**: Latency monitoring and optimization
- **Error Recovery**: Automatic reconnection and stream resumption

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- A Murf AI API key ([Get one here](https://murf.ai))
- An AssemblyAI API key ([Get one here](https://www.assemblyai.com/))
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Modern web browser with microphone support (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment**
   
   Create a `.env` file in the project root:
   ```bash
   MURF_API_KEY=your_actual_murf_api_key_here
   ASSEMBLYAI_API_KEY=your_actual_assemblyai_api_key_here
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   MURF_VOICE_ID=en-IN-aarav
   MONGODB_URL=mongodb://localhost:27017
   ```

4. **Set up MongoDB (Optional)**
   
   **Option A: Local MongoDB Installation**
   - Install MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Start MongoDB service: `mongod` (default: localhost:27017)
   
   **Option B: MongoDB Atlas (Cloud)**
   - Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Create a cluster and get your connection string
   - Replace `MONGODB_URL` in your `.env` file with your Atlas connection string
   
   **Option C: Skip MongoDB**
   - App automatically falls back to in-memory storage if MongoDB is unavailable

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the voice agent**
   
   Navigate to: `http://127.0.0.1:8000`
   
   **Important**: Your browser will request microphone permission. Click "Allow" to enable voice recording functionality.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main application interface with dual-mode voice agent UI (Traditional + Streaming) |
| `POST` | `/agent/chat/{session_id}` | Traditional voice processing with session-based conversation history |
| `GET` | `/agent/chat/{session_id}/history` | Retrieve chat history for a specific session |
| `GET` | `/api/backend` | Backend connectivity test endpoint |
| `GET` | `/api/streamed-audio` | **NEW**: List all real-time streamed audio files with metadata |
| `WebSocket` | `/ws/audio-stream` | **NEW**: Real-time audio streaming with live transcription, LLM streaming, and Murf TTS |
| `WebSocket` | `/ws` | Basic WebSocket connection for bidirectional communication |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |
| `GET` | `/redoc` | Alternative API documentation (ReDoc) |

## 🎵 Real-Time Streaming Endpoints (NEW)

### WebSocket Audio Streaming

**Endpoint:** `ws://127.0.0.1:8000/ws/audio-stream`

#### Revolutionary Streaming Features
- ✅ **Live Audio Transmission**: Real-time 16kHz PCM audio streaming
- ✅ **Instant Transcription**: AssemblyAI Universal Streaming for live speech-to-text
- ✅ **Streaming LLM Responses**: Google Gemini with real-time text generation
- ✅ **Murf WebSocket TTS**: Real-time text-to-speech streaming with base64 audio output
- ✅ **Live Audio Generation**: Streaming base64 audio chunks printed to console
- ✅ **Conversation Persistence**: Automatic MongoDB storage of streaming sessions
- ✅ **Audio File Recording**: Automatic saving of all streamed audio sessions
- ✅ **Connection Management**: Advanced WebSocket lifecycle handling
- ✅ **Real-Time Error Recovery**: Instant error detection and stream recovery

#### Streaming Protocol

**Connection Flow:**
1. **WebSocket Handshake**: Client connects to streaming endpoint
2. **Session Initialization**: Server creates unique session ID and audio file
3. **Transcription Setup**: AssemblyAI Universal Streaming client initialization
4. **Ready State**: Server confirms streaming readiness

**Audio Streaming Messages:**
```json
// Start streaming command
{"text": "start_streaming"}

// Audio chunk transmission (binary)
{"bytes": [binary_audio_data]}

// Stop streaming command  
{"text": "stop_streaming"}
```

**Server Response Types:**
```json
// Session ready
{
  "type": "audio_stream_ready",
  "session_id": "uuid-here",
  "audio_filename": "streamed_audio_uuid_timestamp.wav",
  "transcription_enabled": true,
  "timestamp": "2025-08-20T10:39:40.123456"
}

// Real-time transcription (partial)
{
  "type": "partial_transcript", 
  "text": "Hello how are you",
  "confidence": 0.95,
  "is_final": false
}

// Final transcription (triggers LLM)
{
  "type": "final_transcript",
  "text": "Hello how are you doing today?",
  "confidence": 0.98,
  "is_final": true,
  "end_of_turn": true
}

// Streaming LLM response start
{
  "type": "llm_streaming_start",
  "message": "LLM is generating response...",
  "user_message": "Hello how are you doing today?",
  "timestamp": "2025-08-20T10:39:45.123456"
}

// Real-time LLM chunks
{
  "type": "llm_streaming_chunk",
  "chunk": "I'm doing great, thank you for asking! ",
  "accumulated_length": 35,
  "timestamp": "2025-08-20T10:39:46.123456"
}

// LLM streaming completion
{
  "type": "llm_streaming_complete",
  "message": "LLM response completed",
  "complete_response": "I'm doing great, thank you for asking! How can I help you today?",
  "total_length": 75,
  "timestamp": "2025-08-20T10:39:48.123456"
}

// Murf TTS streaming start (NEW)
{
  "type": "murf_tts_streaming_start",
  "message": "Starting Murf WebSocket TTS streaming",
  "text_to_convert": "I'm doing great, thank you for asking! How can I help you today?",
  "voice_config": {
    "voiceId": "en-IN-aarav",
    "style": "Conversational",
    "rate": 0,
    "pitch": 0,
    "variation": 1
  },
  "context_id": "voice_agent_context_static",
  "timestamp": "2025-08-20T10:39:49.123456"
}

// Real-time base64 audio chunks (NEW)
{
  "type": "murf_audio_chunk",
  "chunk_number": 1,
  "base64_audio": "UklGRvBVAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YcxVAAD...",
  "audio_size": 21848,
  "context_id": "voice_agent_context_static",
  "final": false,
  "timestamp": "2025-08-20T10:39:50.123456"
}

// TTS streaming completion (NEW)
{
  "type": "murf_tts_complete",
  "message": "Murf TTS streaming completed",
  "total_chunks": 76,
  "total_audio_size": 458392,
  "context_id": "voice_agent_context_static",
  "timestamp": "2025-08-20T10:39:55.123456"
}
```

#### Streaming Audio API

**Endpoint:** `GET /api/streamed-audio`

Returns comprehensive metadata about all streaming sessions:

```json
{
  "success": true,
  "message": "Found 15 streamed audio files",
  "files": [
    {
      "filename": "streamed_audio_uuid_20250820_143022.wav",
      "size_bytes": 1024000,
      "created_at": "2025-08-20T14:30:22.123456",
      "modified_at": "2025-08-20T14:32:15.789012"
    }
  ],
  "total_files": 15,
  "total_size_bytes": 15360000
}
```

### Testing Real-Time Streaming

#### **Frontend Testing (Recommended)**
1. **Open the Application**: Navigate to `http://127.0.0.1:8000`
2. **Switch to Streaming Mode**: Click "Start Audio Streaming" button
3. **Watch Live Connection**: See real-time connection status updates
4. **Experience Live Transcription**: Speak and see words appear instantly
5. **Observe Streaming LLM**: Watch AI responses generate in real-time
6. **Review Session History**: Check saved conversations and audio files

#### **WebSocket Testing with Postman**
1. **Create WebSocket Request**: Connect to `ws://127.0.0.1:8000/ws/audio-stream`
2. **Send Start Command**: `{"text": "start_streaming"}`
3. **Send Binary Audio**: Stream raw 16kHz PCM audio data
4. **Observe Real-Time Responses**: See transcription, LLM streaming, and TTS base64 audio
5. **Send Stop Command**: `{"text": "stop_streaming"}`

#### **Audio File Testing**
1. **List Streaming Sessions**: `GET /api/streamed-audio`
2. **Review File Metadata**: Check sizes, timestamps, and session details
3. **Monitor Storage**: Track streaming session storage and cleanup

### 🎵 Murf WebSocket TTS Integration (NEW)

This project features a **revolutionary implementation** of Murf's WebSocket TTS API for real-time text-to-speech streaming. This is one of the first working implementations demonstrating live streaming TTS with base64 audio output.

#### **Key Features**
- **Real-Time TTS Streaming**: Live text-to-speech conversion with instant audio generation
- **Base64 Audio Output**: Streaming base64 encoded audio chunks printed to console
- **WebSocket Connection Management**: Robust connection handling with automatic reconnection
- **Voice Configuration**: Customizable voice settings (voice ID, style, rate, pitch, variation)
- **Static Context Management**: Consistent context ID usage for streaming sessions
- **Error Recovery**: Intelligent error handling with context limit management

#### **Implementation Highlights**
```python
# services/murf_websocket_service.py - Revolutionary Murf WebSocket Integration
class MurfWebSocketService:
    async def connect(self) -> bool:
        """Establish WebSocket connection to Murf TTS API"""
        
    async def stream_text_to_audio(self, text_chunks: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
        """Stream LLM text chunks to Murf and yield base64 audio responses"""
        
    async def send_single_text(self, text: str) -> None:
        """Send complete text for TTS conversion with real-time audio streaming"""
```

#### **Console Output Example**
```
🎵 === MURF BASE64 AUDIO CHUNK 1 ===
Context ID: voice_agent_context_static
Base64 Audio Size: 21848 characters
Base64 Audio: UklGRvBVAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YcxVAAD...
Final: False
=== END AUDIO CHUNK 1 ===

🎵 === MURF BASE64 AUDIO CHUNK 2 ===
Context ID: voice_agent_context_static
Base64 Audio Size: 15420 characters
Base64 Audio: DgAOAA4ADgAOAA4ADgAOAA4ADgAOAA4ADgAOAA4ADgAOAA4ADgAOAA4ADgAO...
Final: False
=== END AUDIO CHUNK 2 ===
```

#### **Voice Configuration**
```json
{
  "voice_config": {
    "voiceId": "en-IN-aarav",
    "style": "Conversational", 
    "rate": 0,
    "pitch": 0,
    "variation": 1
  },
  "context_id": "voice_agent_context_static"
}
```

#### **Testing the Murf Integration**
You can test the Murf WebSocket TTS integration using the provided test script:

```bash
# Run the standalone Murf WebSocket test
python test_murf_websocket.py
```

This test demonstrates:
- WebSocket connection establishment
- Voice configuration setup
- Text streaming to TTS
- Real-time base64 audio chunk reception
- Console output of streaming audio data

### Traditional Chat Agent API (`/agent/chat/{session_id}`)

The enhanced endpoint for session-based voice conversations with persistent history.

**Path Parameter:**
- `session_id`: Unique identifier for the chat session (automatically generated by the UI)

**Request**: Multipart form data with audio file

**Supported Audio Formats:**
- `audio/wav`, `audio/mp3`, `audio/webm`, `audio/ogg`, `audio/m4a`

**Success Response:**
```json
{
  "success": true,
  "message": "Voice chat processed successfully",
  "transcription": "What is artificial intelligence?",
  "llm_response": "**Artificial Intelligence (AI)** is a branch of computer science...",
  "audio_url": "https://murf-audio-url.com/response.mp3",
  "session_id": "session_abc123_1640995200000"
}
```

**Error Response with Fallback Audio:**
```json
{
  "success": false,
  "message": "I'm having trouble understanding your audio right now.",
  "transcription": "",
  "llm_response": "I'm having trouble understanding your audio right now. Please try speaking again clearly into your microphone.",
  "audio_url": "https://murf-fallback-audio-url.com/error_response.mp3",
  "error_type": "stt_error"
}
```

**Error Types & Recovery:**
- `api_keys_missing`: Configuration issues with guidance
- `file_error`: Audio processing problems with auto-restart
- `stt_error`: Speech recognition failures with retry
- `no_speech`: Silent recordings with auto-recovery
- `llm_error`: AI processing issues with fallback
- `tts_error`: Voice generation problems (text still shown)
- `general_error`: Network/connection issues

### Chat History API (`/agent/chat/{session_id}/history`)

Retrieve conversation history for a specific session.

**Success Response:**
```json
{
  "success": true,
  "session_id": "session_abc123_1640995200000",
  "messages": [
    {
      "role": "user",
      "content": "What is artificial intelligence?",
      "timestamp": "2023-12-01T10:30:00Z"
    },
    {
      "role": "assistant", 
      "content": "**Artificial Intelligence (AI)** is a branch of computer science...",
      "timestamp": "2023-12-01T10:30:15Z"
    }
  ],
  "message_count": 2
}
```

### Backend Test API (`/api/backend`)

**Response:**
```json
{
  "message": "🚀 This message is coming from FastAPI backend!",
  "status": "success"
}
```

## 🛠️ Technologies Used

### Revolutionary Streaming Stack (NEW)
- **[WebSockets](https://websockets.readthedocs.io/)**: Real-time bidirectional streaming communication
- **[AssemblyAI Universal Streaming](https://www.assemblyai.com/docs/api-reference/streaming)**: Live speech-to-text transcription
- **[Google Gemini Streaming](https://ai.google.dev/api/generate-content#method:-models.streamgeneratecontent)**: Real-time LLM response generation
- **[Murf WebSocket API](https://murf.ai)**: Revolutionary real-time text-to-speech streaming with base64 audio output
- **Binary Audio Processing**: 16kHz PCM streaming with optimized chunk handling
- **Asynchronous Event Loops**: Non-blocking real-time processing architecture

### Backend Architecture
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, fast web framework with dual endpoint support
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Data validation and settings management with streaming schemas
- **Dual-Mode Services**: Traditional file-based + streaming real-time processing
- **Advanced Connection Management**: WebSocket lifecycle and connection pooling
- **Enhanced Logging**: Real-time operation tracking and performance monitoring

### AI Services Integration  
- **[AssemblyAI](https://www.assemblyai.com/)**: Dual-mode speech processing (traditional + streaming)
- **[Google Gemini](https://ai.google.dev/)**: Advanced LLM with streaming response capabilities
- **[Murf AI](https://murf.ai)**: Dual-mode text-to-speech (traditional API + WebSocket streaming)
- **Context-Aware Processing**: Conversation history preservation across streaming sessions

### Data & Infrastructure
- **[MongoDB](https://www.mongodb.com/)**: Enhanced NoSQL storage for streaming session persistence
- **[Motor](https://motor.readthedocs.io/)**: Async MongoDB driver optimized for real-time operations
- **Real-Time Session Management**: Live conversation tracking and persistence
- **Streaming Audio Storage**: Automatic file saving for all streaming sessions
- **[Uvicorn](https://www.uvicorn.org/)**: High-performance ASGI server with WebSocket support

### Frontend Innovation
- **WebSocket Client**: Advanced real-time communication with the streaming backend
- **Real-Time Audio Processing**: Live 16kHz PCM capture and transmission
- **Streaming UI Updates**: Live transcription display and LLM response streaming
- **Dual-Mode Interface**: Seamless switching between traditional and streaming modes
- **Connection Monitoring**: Real-time WebSocket status and performance tracking
- **Audio Context API**: Advanced browser audio processing and optimization

## 🎨 Frontend Features

### Revolutionary Streaming Interface (NEW)
- **Dual-Mode Design**: Seamless switching between Traditional and Real-Time Streaming modes
- **Live Connection Status**: Real-time WebSocket connection monitoring with visual indicators
- **Streaming Controls**: Advanced start/stop streaming with intelligent state management
- **Real-Time Transcription Display**: Watch your words appear instantly as you speak
- **Live LLM Response Streaming**: See AI responses generate character by character
- **Murf TTS Streaming Display**: Real-time base64 audio chunks printed to console for voice synthesis
- **Session Monitoring**: Real-time session IDs, connection counts, and streaming metrics
- **Streaming Status Log**: Live event logging with timestamped streaming updates
- **Performance Indicators**: Real-time bytes transferred, chunk processing, and latency metrics

### Enhanced Traditional Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Smart Recording Controls**: Enhanced start/stop recording with streaming fallback
- **Visual Recording Feedback**: Improved animations and real-time timer
- **Advanced Loading States**: Enhanced processing visualization with streaming awareness
- **Rich Markdown Rendering**: Full support for formatted AI responses including:
  - Headers and subheaders (# ## ###)
  - **Bold** and *italic* text formatting
  - `Inline code` with syntax highlighting
  - Code blocks with professional syntax highlighting
  - Bullet points and numbered lists
  - Tables with hover effects
  - Blockquotes and horizontal rules
  - Clickable links
- **Audio Playback Controls**: Enhanced HTML5 audio players with streaming support
- **Error Handling**: Enhanced error messages with streaming fallback options

### Real-Time User Experience
- **Live Audio Streaming**: 16kHz PCM audio transmission with optimized processing
- **Instant Feedback**: Real-time transcription and response generation
- **Connection Resilience**: Automatic reconnection and stream recovery
- **Multi-Modal History**: Support for both traditional and streaming conversation records
- **Performance Optimization**: Adaptive streaming quality and connection management
- **Accessibility**: Enhanced keyboard navigation and screen reader support for streaming

### Advanced Audio Processing
- **Optimized Audio Capture**: 16kHz sample rate with echo cancellation and noise suppression
- **Real-Time Chunk Processing**: Efficient 4096-sample audio chunking for streaming
- **Format Detection**: Automatic audio format selection for optimal streaming
- **Connection-Aware Quality**: Adaptive audio quality based on WebSocket performance
- **Background Recording**: Seamless audio capture during streaming sessions

## 📦 Dependencies

This project uses the following Python packages (see [`requirements.txt`](requirements.txt)):

```
fastapi==0.104.1          # Web framework with WebSocket support
uvicorn[standard]==0.24.0 # ASGI server with WebSocket capabilities
jinja2==3.1.2             # Template engine for dual-mode HTML rendering
python-multipart==0.0.6   # For handling form data and streaming audio
python-dotenv==1.0.0      # Environment variable management
murf==2.0.0               # Official Murf AI Python SDK
requests==2.31.0          # HTTP library for API calls
assemblyai==0.17.0        # AssemblyAI Python SDK with Universal Streaming
google-generativeai==0.3.2 # Google Gemini AI SDK with streaming support
pymongo==4.6.0            # MongoDB driver for traditional storage
motor==3.3.2              # Async MongoDB driver for real-time operations
websockets==12.0          # WebSocket library for Murf TTS streaming (NEW)
```

### 🏗️ Architecture Benefits

The revolutionary streaming architecture provides key improvements:

- **⚡ Real-Time Performance**: Sub-second latency for transcription and LLM responses
- **🔄 Live Interaction**: Natural conversation flow with instant feedback
- **🎵 Complete Voice Pipeline**: End-to-end streaming from voice input to audio response generation
- **🧩 Dual-Mode Flexibility**: Traditional and streaming modes for different use cases
- **🔒 Enhanced Type Safety**: Streaming-aware Pydantic models with WebSocket validation
- **📝 Advanced Logging**: Real-time operation tracking with performance metrics
- **🐛 Live Debugging**: Instant error detection and streaming recovery
- **🚀 Horizontal Scalability**: WebSocket connection pooling and load distribution
- **🧪 Streaming Testability**: Independent testing of real-time streaming components
- **📊 Performance Monitoring**: Real-time metrics for latency, throughput, and connection health
- **🔌 Extensible Streaming**: Foundation for future real-time features and enhancements

## 🔧 Configuration

### Environment Variables

Create a [`.env`](.env) file in the project root with the following variables:

```bash
# Required: Your Murf AI API key
MURF_API_KEY=your_actual_murf_api_key_here

# Required: Your AssemblyAI API key
ASSEMBLYAI_API_KEY=your_actual_assemblyai_api_key_here

# Required: Your Google Gemini API key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: Murf voice ID (defaults to "en-IN-aarav")
MURF_VOICE_ID=en-IN-aarav
```

### Getting Your API Keys

#### Murf AI API Key
1. Sign up at [Murf.ai](https://murf.ai)
2. Navigate to your account settings or API section
3. Generate or copy your API key
4. Add it to your `.env` file

#### AssemblyAI API Key
1. Sign up at [AssemblyAI.com](https://www.assemblyai.com/)
2. Go to your dashboard
3. Copy your API key
4. Add it to your `.env` file

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Add it to your `.env` file

## 🚀 Development

### Running in Development Mode

The application runs with auto-reload enabled by default, which means it will automatically restart when you make changes to the code:

```bash
python main.py
```

### API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🐛 Troubleshooting & Error Handling

### 🛡️ Built-in Error Recovery Features

This application includes **comprehensive error handling** that automatically manages failures and provides intelligent recovery:

#### **Automatic Error Detection & Recovery**
- **API Key Issues**: Detects missing or invalid API keys and provides fallback audio responses
- **Network Failures**: Handles timeout and connection errors with auto-retry mechanisms  
- **Service Outages**: Gracefully manages when individual AI services (STT/LLM/TTS) are unavailable
- **Audio Processing**: Manages microphone issues, empty recordings, and file format problems
- **MongoDB Fallback**: Automatically switches to in-memory storage when database is unavailable

#### **Error Types & Responses**
1. **🔧 `api_keys_missing`**: Configuration issues with spoken guidance to contact support
2. **🎤 `file_error`**: Audio processing problems with automatic recording restart
3. **🎯 `stt_error`**: Speech transcription failures with retry suggestions
4. **🔇 `no_speech`**: Silent recordings with auto-restart after guidance
5. **🤖 `llm_error`**: AI thinking problems with retry mechanisms
6. **🔊 `tts_error`**: Voice generation issues (text response still provided)
7. **⚠️ `general_error`**: Network/connection problems with auto-recovery

#### **Smart Recovery Mechanisms**
- **Auto-Recording Restart**: Certain errors automatically restart voice recording
- **Fallback Audio**: Every error gets a spoken response via Murf TTS
- **Progressive Retry**: Different retry strategies based on error type
- **Graceful Degradation**: App continues working even when individual services fail

### Common Issues & Solutions

#### API Key Related
1. **"The voice agent is not properly configured"** 🔧
   - **Auto-Handled**: App detects this and provides spoken error message
   - **Manual Fix**: Verify your API keys in the `.env` file
   - **What App Does**: Generates fallback audio response automatically

#### Recording & Audio Issues  
2. **"No speech detected in your audio"** 🔇
   - **Auto-Handled**: App automatically restarts recording after 3 seconds
   - **Manual Fix**: Speak clearly and check microphone
   - **What App Does**: Provides spoken guidance and auto-restarts

3. **"Having trouble understanding your audio"** 🎯  
   - **Auto-Handled**: STT error detection with automatic retry
   - **Manual Fix**: Ensure good microphone quality and quiet environment
   - **What App Does**: Gives specific guidance and restarts recording

#### AI Service Issues
4. **"AI thinking process interrupted"** 🤖
   - **Auto-Handled**: LLM error detection with retry after delay
   - **Manual Fix**: Check internet connection
   - **What App Does**: Provides spoken explanation and retry option

5. **"Voice generation issue"** 🔊
   - **Auto-Handled**: TTS failure detection, text response still shown
   - **Manual Fix**: Check Murf API status
   - **What App Does**: Displays text response even without audio

#### Network & Connection
6. **"Connection issue"** ⚠️
   - **Auto-Handled**: Network timeout detection with auto-retry
   - **Manual Fix**: Check internet connection
   - **What App Does**: Implements 60-second timeouts and smart retry

### Browser Compatibility

**Fully Supported:**
- Chrome 49+
- Firefox 25+
- Safari 14.1+
- Edge 79+

**Limited Support:**
- Internet Explorer: Not supported
- Older mobile browsers: May have limited functionality

### Logging

The application includes console logging for debugging. Check the browser console and terminal output for detailed error information.

## 📝 Usage

### Real-Time Streaming Mode (NEW) 🎵
1. **Access Streaming Interface**: Navigate to the "Audio Streaming" section on the homepage
2. **Start Live Streaming**: Click "Start Audio Streaming" to connect to real-time WebSocket
3. **Watch Live Connection**: Monitor connection status and session ID in real-time
4. **Begin Voice Streaming**: Click "Start Recording" to begin live audio transmission
5. **See Live Transcription**: Watch your words appear instantly as you speak
6. **Experience Streaming AI**: Observe LLM responses generate character by character
7. **View Real-Time TTS**: See base64 audio chunks printed to console via Murf WebSocket streaming
8. **Natural Turn Taking**: Stop speaking and watch automatic turn detection
9. **Continue Conversation**: Continue with natural voice conversation flow
10. **Review Session**: Check saved audio files and conversation history

### Traditional Mode (Enhanced) 🎤
1. **Classic Voice Interface**: Use the traditional single-button interface
2. **Smart Button Control**: Single button shows current state with enhanced feedback
3. **Enhanced Processing**: Watch improved processing stages with streaming awareness
4. **Fallback Capability**: Automatic fallback to streaming mode when available
5. **Session Continuity**: Seamless session management across both modes

### Streaming Experience Tips
- **Optimal Audio**: Use quality microphone in quiet environment for best streaming results
- **Stable Connection**: Ensure reliable internet for smooth real-time streaming
- **Natural Speech**: Speak naturally with pauses for optimal turn detection
- **Real-Time Feedback**: Watch live transcription to confirm accurate speech recognition
- **Connection Monitoring**: Keep an eye on connection status for optimal performance

### Advanced Features
- **Session Sharing**: Share streaming session URLs for collaborative conversations
- **Audio File Access**: Review all streamed audio files via `/api/streamed-audio` endpoint
- **Performance Monitoring**: Track real-time metrics and connection health
- **Dual-Mode History**: Access both traditional and streaming conversation records
- **Error Recovery**: Automatic reconnection and stream resumption capabilities
- **Murf TTS Streaming**: Real-time base64 audio output via WebSocket console display

## 🆕 Revolutionary Features Highlights

### Real-Time Streaming Innovation
- **Live Voice Pipeline**: Complete real-time voice-to-voice conversation with sub-second latency
- **Streaming Transcription**: Watch your words appear instantly as you speak with AssemblyAI Universal Streaming
- **Live LLM Responses**: Experience AI thinking in real-time with character-by-character response generation
- **Murf WebSocket TTS**: Revolutionary real-time text-to-speech streaming with base64 audio output
- **Complete Audio Pipeline**: End-to-end streaming from voice input to audio response generation
- **Seamless Turn Detection**: Natural conversation flow with intelligent speaker turn recognition
- **Real-Time Session Persistence**: All streaming conversations automatically saved to MongoDB and audio files

### Dual-Mode Architecture
- **Flexible Interface**: Choose between traditional file-based or revolutionary streaming modes
- **Intelligent Fallback**: Automatic degradation from streaming to traditional mode when needed
- **Unified Session Management**: Seamless conversation history across both interaction modes
- **Performance Optimization**: Adaptive processing based on connection quality and user preferences

### Advanced WebSocket Infrastructure
- **Dual WebSocket Endpoints**: Specialized endpoints for different streaming requirements
- **Connection Resilience**: Automatic reconnection, error recovery, and stream resumption
- **Real-Time Monitoring**: Live connection status, performance metrics, and streaming health
- **Concurrent Session Support**: Multiple simultaneous streaming sessions with isolated processing

### Enhanced User Experience
- **Live Visual Feedback**: Real-time connection status, transcription display, and response streaming
- **Intelligent State Management**: Smart button controls that adapt to current streaming state
- **Performance Transparency**: Real-time metrics showing bytes transferred, latency, and processing time
- **Seamless Audio Management**: Automatic file saving, session organization, and streaming history

### Production-Ready Streaming
- **Scalable Architecture**: WebSocket connection pooling and horizontal scaling support
- **Comprehensive Error Handling**: Real-time error detection with specific streaming recovery strategies
- **Performance Monitoring**: Live tracking of streaming performance, connection health, and system metrics
- **Enterprise Features**: Session management, audio archival, and comprehensive logging for production use
- **Murf WebSocket Integration**: Production-ready real-time TTS streaming with base64 audio output

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).