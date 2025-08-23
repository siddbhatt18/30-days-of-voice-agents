"""
Simple test script to demonstrate Murf WebSocket base64 audio output
"""

import asyncio
import websockets
import json
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_murf_simple():
    """Simple test with Murf WebSocket API"""
    
    api_key = os.getenv("MURF_API_KEY")
    voice_id = os.getenv("MURF_VOICE_ID", "en-US-amara")
    
    if not api_key:
        print("❌ MURF_API_KEY not found")
        return
    
    # WebSocket URL
    ws_url = f"wss://api.murf.ai/v1/speech/stream-input?api-key={api_key}&sample_rate=44100&channel_type=MONO&format=WAV"
    
    try:
        print("🔌 Connecting to Murf WebSocket...")
        async with websockets.connect(ws_url) as ws:
            print("✅ Connected successfully!")
            
            # Send voice configuration
            voice_config = {
                "voice_config": {
                    "voiceId": voice_id,
                    "style": "Conversational",
                    "rate": 0,
                    "pitch": 0,
                    "variation": 1
                }
            }
            
            print(f"📤 Sending voice config...")
            await ws.send(json.dumps(voice_config))
            
            # Send text to convert
            test_text = "Hello! This is a test of the Murf WebSocket API. You should see base64 audio in the console."
            
            text_message = {
                "context_id": "test_context_123",
                "text": test_text,
                "end": True
            }
            
            print(f"📤 Sending text: {test_text}")
            await ws.send(json.dumps(text_message))
            
            # Listen for responses
            audio_chunk_count = 0
            print("🎵 Waiting for audio responses...")
            
            while True:
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=30.0)
                    data = json.loads(response)
                    
                    print(f"📥 Received response: {list(data.keys())}")
                    
                    if "audio" in data:
                        audio_chunk_count += 1
                        audio_base64 = data["audio"]
                        
                        print(f"\n🎵 === MURF BASE64 AUDIO CHUNK {audio_chunk_count} ===")
                        print(f"Context ID: {data.get('context_id', 'N/A')}")
                        print(f"Base64 Audio Size: {len(audio_base64)} characters")
                        print(f"Base64 Audio Preview: {audio_base64[:100]}...")
                        # print(f"Base64 Audio (Full): {audio_base64}")
                        print(f"Final: {data.get('final', False)}")
                        print(f"=== END AUDIO CHUNK {audio_chunk_count} ===\n")
                        
                        if data.get("final"):
                            print(f"🎉 Final audio chunk received! Total chunks: {audio_chunk_count}")
                            break
                    else:
                        print(f"📊 Non-audio response: {data}")
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
                except websockets.exceptions.ConnectionClosed:
                    print("🔌 Connection closed")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    break
            
            print(f"\n📊 Test Summary:")
            print(f"   Audio chunks received: {audio_chunk_count}")
            print(f"   Text sent: {len(test_text)} characters")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Simple Murf WebSocket Test")
    print("=" * 50)
    asyncio.run(test_murf_simple())
    print("✅ Test completed!")
