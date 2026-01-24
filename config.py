"""
Configuration settings for the AI Voice Assistant
"""

class Config:
    # Wake word
    WAKE_WORDS = ["hey assistant", "hello assistant", "wake up","meow meow","meow",]
    WAKE_WORD_SENSITIVITY = 0.5
    
    # OpenAI settings
    CHATGPT_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 150
    TEMPERATURE = 0.7
    
    # Speech recognition settings
    ENERGY_THRESHOLD = 300  
    DYNAMIC_ENERGY_THRESHOLD = True
    PAUSE_THRESHOLD = 0.8  
    
    # Text-to-speech settings
    TTS_VOICE_RATE = 170  
    TTS_VOICE_VOLUME = 0.9  
    
    # Audio settings
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1024
    FORMAT = 'int16'
    CHANNELS = 1
    
    # System settings
    LOG_LEVEL = "INFO"
    SAVE_CONVERSATIONS = True
    CONVERSATION_HISTORY_FILE = "conversation_history.json"