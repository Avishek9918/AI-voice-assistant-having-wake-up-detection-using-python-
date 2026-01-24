"""
ChatGPT integration module for conversational AI
"""

import openai
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ChatGPTHandler:
    def __init__(self, config):
        """Initialize ChatGPT handler"""
        self.config = config
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # System message to define assistant behavior
        self.system_message = {
            "role": "system",
            "content": """You are a helpful AI voice assistant. 
            Be concise in your responses as you're speaking, not writing.
            Keep responses under 2-3 sentences when possible.
            Be friendly and professional."""
        }
        
        logger.info("ChatGPT handler initialized")
    
    def get_response(self, user_input: str, conversation_history: List[Dict] = None):
        """
        Get response from ChatGPT
        
        Args:
            user_input: User's text input
            conversation_history: Previous conversation context
            
        Returns:
            str: ChatGPT response
        """
        try:
            # Prepare messages
            messages = [self.system_message]
            
            # history if available
            if conversation_history:
                for msg in conversation_history[-6:]:  # Last 3 exchanges
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # user input
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # response from ChatGPT
            response = self.client.chat.completions.create(
                model=self.config.CHATGPT_MODEL,
                messages=messages,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            
            assistant_response = response.choices[0].message.content
            
            logger.info(f"ChatGPT response: {assistant_response[:50]}...")
            return assistant_response
            
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            return "I'm having trouble connecting to my brain right now. Please try again."
        except Exception as e:
            logger.error(f"Error getting ChatGPT response: {e}")
            return "Sorry, I encountered an error processing your request."