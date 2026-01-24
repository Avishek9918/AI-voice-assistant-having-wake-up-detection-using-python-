"""
Main entry point for the AI Voice Assistant
"""

import os
import time
import logging
from dotenv import load_dotenv
from modules.wake_word_detector import WakeWordDetector
from modules.voice_processor import VoiceProcessor
from modules.chatgpt_handler import ChatGPTHandler
from modules.tts_engine import TTSEngine
from utils.config_loader import load_config

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIVoiceAssistant:
    def __init__(self):
        """Initialize the AI Voice Assistant"""
        self.config = load_config()
        self.is_active = False
        self.conversation_history = []
        
        # Initialize
        logger.info("Initializing AI Voice Assistant...")
        
        try:
            self.wake_detector = WakeWordDetector(self.config)
            self.voice_processor = VoiceProcessor(self.config)
            self.chatgpt = ChatGPTHandler(self.config)
            self.tts = TTSEngine(self.config)
            
            logger.info("AI Voice Assistant initialized successfully!")
        except Exception as e:
            logger.error(f"Failed to initialize assistant: {e}")
            raise
    
    def listen_for_wake_word(self):
        """Continuously listen for wake word"""
        logger.info("Listening for wake word...")
        
        while True:
            try:
                # Check for wake word
                if self.wake_detector.detect():
                    logger.info("Wake word detected!")
                    self.is_active = True
                    self.tts.speak("Yes? How can I help you?")
                    self.listen_for_command()
                
                time.sleep(0.1)  # Prevent CPU overuse
                
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                self.cleanup()
                break
            except Exception as e:
                logger.error(f"Error in wake word detection: {e}")
                time.sleep(1)
    
    def listen_for_command(self):
        """Listen for user command after wake word"""
        logger.info("Listening for command...")
        
        try:
            # Listen for user input
            self.tts.speak("I'm listening")
            audio_text = self.voice_processor.listen()
            
            if audio_text:
                logger.info(f"User said: {audio_text}")
                
                
                if self.is_exit_command(audio_text):
                    self.tts.speak("Goodbye!")
                    self.is_active = False
                    return
                #response from ChatGPT
                response = self.chatgpt.get_response(audio_text, self.conversation_history)
                
                #conversation history
                self.update_conversation_history(audio_text, response)
                
                #response
                self.tts.speak(response)
                
                #Save
                if self.config.SAVE_CONVERSATIONS:
                    self.save_conversation()
                    
            else:
                logger.info("No command detected")
                self.tts.speak("I didn't catch that. Please try again.")
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.tts.speak("Sorry, I encountered an error. Please try again.")
    
    def is_exit_command(self, text):
        """Check if the command is an exit command"""
        exit_keywords = ["exit", "quit", "goodbye", "stop", "shutdown"]
        return any(keyword in text.lower() for keyword in exit_keywords)
    
    def update_conversation_history(self, user_input, assistant_response):
        """Update conversation history"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": time.time()
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_response,
            "timestamp": time.time()
        })
        
        # Keep only last 10 conversations to manage memory
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def save_conversation(self):
        """Save conversation to file"""
        try:
            import json
            with open(self.config.CONVERSATION_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        self.wake_detector.cleanup()
        self.voice_processor.cleanup()
        self.tts.cleanup()
    
    def run(self):
        """Main run loop"""
        logger.info("Starting AI Voice Assistant...")
        print("\n" + "="*50)
        print("AI Voice Assistant - Ready for Commands")
        print("="*50)
        print("Say one of the wake words:")
        for word in self.config.WAKE_WORDS:
            print(f"  {word}")
        print("Press Ctrl+C to exit")
        print("="*50 + "\n")
        
        self.listen_for_wake_word()

if __name__ == "__main__":
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    try:
        assistant = AIVoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")