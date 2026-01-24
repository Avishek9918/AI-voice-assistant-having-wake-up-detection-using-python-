"""
Wake word detection module using keyword spotting
"""

import speech_recognition as sr
import numpy as np
import logging
from threading import Thread
import queue

logger = logging.getLogger(__name__)

class WakeWordDetector:
    def __init__(self, config):
        """Initialize wake word detector"""
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        #for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        self.recognizer.energy_threshold = config.ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = config.DYNAMIC_ENERGY_THRESHOLD
        self.recognizer.pause_threshold = config.PAUSE_THRESHOLD
        
        logger.info("Wake word detector initialized")
    
    def detect(self):
        """Detect wake word in audio stream"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=1,
                    phrase_time_limit=2
                )
            
            # Convert audio to text
            try:
                text = self.recognizer.recognize_google(audio).lower()
                logger.debug(f"Heard: {text}")
                
                # Check for wake words
                for wake_word in self.config.WAKE_WORDS:
                    if wake_word in text:
                        return True
                        
            except sr.UnknownValueError:
                pass  # No speech detected
            except sr.RequestError as e:
                logger.error(f"Could not request results: {e}")
        
        except sr.WaitTimeoutError:
            pass  # No audio input
        
        return False
    
    def cleanup(self):
        """Cleanup resources"""
        logger.debug("Cleaning up wake word detector")