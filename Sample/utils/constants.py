from models.schemas import ErrorType

FALLBACK_MESSAGES = {
    ErrorType.STT_ERROR: "I'm having trouble understanding your audio right now. Please try speaking again clearly into your microphone.",
    ErrorType.LLM_ERROR: "I'm experiencing some technical difficulties with my thinking process. Please try again in a moment.",
    ErrorType.TTS_ERROR: "I can understand you, but I'm having trouble generating speech right now. Please check your connection.",
    ErrorType.GENERAL_ERROR: "I'm having trouble connecting right now. Please check your connection and try again.",
    ErrorType.NO_SPEECH: "I didn't detect any speech in your audio. Please try speaking clearly into your microphone.",
    ErrorType.API_KEYS_MISSING: "The voice agent is not properly configured. Please contact support.",
    ErrorType.FILE_ERROR: "There was an issue processing your audio file. Please try recording again.",
    ErrorType.TIMEOUT_ERROR: "The request is taking longer than expected. Please try again."
}


def get_fallback_message(error_type: ErrorType) -> str:
    return FALLBACK_MESSAGES.get(error_type, FALLBACK_MESSAGES[ErrorType.GENERAL_ERROR])
