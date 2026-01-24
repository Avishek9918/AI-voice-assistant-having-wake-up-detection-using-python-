"""
Audio utility functions
"""

import numpy as np
import sounddevice as sd
import logging

logger = logging.getLogger(__name__)

def play_audio(audio_data, sample_rate=16000):
    """
    Play audio data
    
    Args:
        audio_data: NumPy array of audio data
        sample_rate: Sample rate in Hz
    """
    try:
        sd.play(audio_data, sample_rate)
        sd.wait()
    except Exception as e:
        logger.error(f"Error playing audio: {e}")

def record_audio(duration=5, sample_rate=16000):
    """
    Record audio from microphone
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Sample rate in Hz
        
    Returns:
        numpy.ndarray: Audio data
    """
    try:
        logger.info(f"Recording audio for {duration} seconds...")
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        return recording.flatten()
    except Exception as e:
        logger.error(f"Error recording audio: {e}")
        return None