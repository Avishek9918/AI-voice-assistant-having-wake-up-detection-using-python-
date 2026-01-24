"""
Voice processing module for speech recognition
"""

import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

class VoiceProcessor:
    def __init__(self, config):
        """Initialize voice processor"""
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configure recognizer
        self.recognizer.energy_threshold = config.ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = config.DYNAMIC_ENERGY_THRESHOLD
        self.recognizer.pause_threshold = config.PAUSE_THRESHOLD
        
        logger.info("Voice processor initialized")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for audio input and convert to text
        
        Args:
            timeout: Seconds to wait for phrase to start
            phrase_time_limit: Maximum seconds for a phrase
            
        Returns:
            str: Recognized text or empty string
        """
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.info("Listening for command...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            logger.info("Processing audio...")
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout - no speech detected")
            return ""
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results: {e}")
            return ""
        except Exception as e:
            logger.error(f"Error in voice processing: {e}")
            return ""
    
    def cleanup(self):
        """Cleanup resources"""
        logger.debug("Cleaning up voice processor")