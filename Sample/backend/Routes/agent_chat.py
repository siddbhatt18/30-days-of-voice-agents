# from fastapi import APIRouter, HTTPException, File, UploadFile
# from Services.Stt_service import transcribe_audio
# from Services.Tts_service import generate_speech
# from Services.Gemini_service import get_response_from_gemini

# router = APIRouter()

# chat_store = {}


# @router.post("/agent/chat/{session_id}")
# async def chat_with_history(session_id: str, file: UploadFile = File(...)):
#     allowed_types = ["audio/mp3", "audio/webm", "audio/wav", "audio/ogg"]
#     if file.content_type not in allowed_types:
#         raise HTTPException(status_code=400, detail="Invalid file type")

#     try:
#         # 1. Transcribe audio
#         audio_bytes = await file.read()
#         transcription = transcribe_audio(audio_bytes)
#         user_message = {"role": "user", "text": transcription}

#         # 2. Manage conversation history
#         if session_id not in chat_store:
#             chat_store[session_id] = []
#         chat_store[session_id].append(user_message)

#         # 3. Get AI response
#         ai_reply = get_response_from_gemini(chat_store[session_id])
#         assistant_message = {"role": "assistant", "text": ai_reply}
#         chat_store[session_id].append(assistant_message)

#         # 4. Generate speech
#         audio_url = generate_speech(ai_reply)

#         return {
#             "audio_url": audio_url,
#             "text": ai_reply,
#             "history": chat_store[session_id]
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
