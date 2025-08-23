import google.generativeai as genai
from typing import List, Dict, Optional, AsyncGenerator
import logging

logger = logging.getLogger(__name__)


class LLMService:    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def format_chat_history_for_llm(self, messages: List[Dict]) -> str:
        if not messages:
            return ""
        
        formatted_history = "\n\nPrevious conversation context:\n"
        for msg in messages[-10:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_history += f"{role}: {msg['content']}\n"
        
        return formatted_history
    
    async def generate_response(self, user_message: str, chat_history: List[Dict]) -> str:
        try:
            history_context = self.format_chat_history_for_llm(chat_history)
            
            llm_prompt = f"""Please provide a helpful and well-formatted response to the following user message. 
                            Guidelines:
                            - Keep your response under 3000 characters to ensure it can be converted to speech effectively
                            - Use Markdown formatting when appropriate:
                              - Use **bold** for emphasis
                              - Use `code` for technical terms or code snippets
                              - Use bullet points (-) or numbered lists (1.) when listing items
                              - Use code blocks (```) for longer code examples
                              - Use headers (##) for sections if needed
                              - Use tables when organizing data
                            - Structure your response clearly and logically
                            - Be concise but comprehensive
                            - Consider the conversation history to provide relevant and contextual responses
                            
                            {history_context}
                            
                            Current user message: {user_message}"""
            
            llm_response = self.model.generate_content(llm_prompt)
            
            if not llm_response.candidates:
                raise Exception("No response candidates generated from LLM")
            
            response_text = ""
            for part in llm_response.candidates[0].content.parts:
                if hasattr(part, 'text'):
                    response_text += part.text
            
            if not response_text.strip():
                raise Exception("Empty response text from LLM")
            
            response_text = response_text.strip()
            logger.info(f"LLM response generated successfully: {len(response_text)} characters")
            return response_text
            
        except Exception as e:
            logger.error(f"LLM response generation error: {str(e)}")
            raise

    async def generate_streaming_response(self, user_message: str, chat_history: List[Dict]) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the LLM"""
        try:
            history_context = self.format_chat_history_for_llm(chat_history)
            
            llm_prompt = f"""Please provide a helpful and well-formatted response to the following user message. 
                            Guidelines:
                            - Keep your response under 3000 characters to ensure it can be converted to speech effectively
                            - Use Markdown formatting when appropriate:
                              - Use **bold** for emphasis
                              - Use `code` for technical terms or code snippets
                              - Use bullet points (-) or numbered lists (1.) when listing items
                              - Use code blocks (```) for longer code examples
                              - Use headers (##) for sections if needed
                              - Use tables when organizing data
                            - Structure your response clearly and logically
                            - Be concise but comprehensive
                            - Consider the conversation history to provide relevant and contextual responses
                            
                            {history_context}
                            
                            Current user message: {user_message}"""
            
            # Use stream_generate_content for streaming response
            response_stream = self.model.generate_content(llm_prompt, stream=True)
            
            accumulated_response = ""
            for chunk in response_stream:
                if chunk.candidates and len(chunk.candidates) > 0:
                    candidate = chunk.candidates[0]
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                accumulated_response += part.text
                                yield part.text
            
            if not accumulated_response.strip():
                raise Exception("Empty response text from LLM")
            
            logger.info(f"LLM streaming response completed: {len(accumulated_response)} characters")
            
        except Exception as e:
            logger.error(f"LLM streaming response generation error: {str(e)}")
            raise
