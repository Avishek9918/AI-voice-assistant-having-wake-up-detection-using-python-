"""
Text-to-Speech engine module
"""

import pyttsx3
import logging
import threading

logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self, config):
        """Initialize TTS engine"""
        self.config = config
        self.engine = None
        self.is_speaking = False
        self.speech_thread = None
        
        self._initialize_engine()
        logger.info("TTS engine initialized")
    
    def _initialize_engine(self):
        """Initialize pyttsx3 engine"""
        try:
            self.engine = pyttsx3.init()
            
            self.engine.setProperty('rate', self.config.TTS_VOICE_RATE)
            self.engine.setProperty('volume', self.config.TTS_VOICE_VOLUME)
            
            
            voices = self.engine.getProperty('voices')
            
            
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            logger.info(f"TTS voice selected: {self.engine.getProperty('voice')}")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            raise
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
        """
        if not text or not self.engine:
            return
        
        
        self.speech_thread = threading.Thread(
            target=self._speak_sync,
            args=(text,)
        )
        self.speech_thread.daemon = True
        self.speech_thread.start()
    
    def _speak_sync(self, text):
        """Synchronous speaking method for threading"""
        self.is_speaking = True
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in TTS: {e}")
        finally:
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech"""
        if self.engine and self.is_speaking:
            self.engine.stop()
    
    def is_busy(self):
        """Check if TTS is currently speaking"""
        return self.is_speaking
    
    def cleanup(self):
        """Cleanup resources"""
        logger.debug("Cleaning up TTS engine")
        if self.engine:
            self.engine.stop()