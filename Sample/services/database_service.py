from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self, mongodb_url: str = "mongodb://localhost:27017"):
        self.mongodb_url = mongodb_url
        self.client = None
        self.db = None
        self.in_memory_store = {}
    
    async def connect(self) -> bool:
        try:
            self.client = AsyncIOMotorClient(self.mongodb_url)
            self.db = self.client.voice_agents
            await self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB successfully")
            return True
        except Exception as e:
            logger.warning(f"⚠️  MongoDB connection failed: {e}")
            logger.info("💾 Using in-memory storage as fallback")
            self.client = None
            self.db = None
            return False
    
    async def get_chat_history(self, session_id: str) -> List[Dict]:
        if self.db is not None:
            try:
                chat_history = await self.db.chat_sessions.find_one({"session_id": session_id})
                if chat_history and "messages" in chat_history:
                    return chat_history["messages"]
                return []
            except Exception as e:
                logger.error(f"Failed to get chat history from MongoDB: {str(e)}")
                return []
        else:
            return self.in_memory_store.get(session_id, [])
    
    async def add_message_to_history(self, session_id: str, role: str, content: str) -> bool:
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        }
        
        if self.db is not None:
            try:
                await self.db.chat_sessions.update_one(
                    {"session_id": session_id},
                    {
                        "$push": {"messages": message},
                        "$set": {"last_updated": datetime.now()}
                    },
                    upsert=True
                )
                return True
            except Exception as e:
                logger.error(f"Failed to save message to MongoDB: {str(e)}")
                if session_id not in self.in_memory_store:
                    self.in_memory_store[session_id] = []
                self.in_memory_store[session_id].append(message)
                return True
        else:
            if session_id not in self.in_memory_store:
                self.in_memory_store[session_id] = []
            self.in_memory_store[session_id].append(message)
            return True
    
    async def close(self):
        if self.client:
            self.client.close()
            logger.info("Database connection closed")
