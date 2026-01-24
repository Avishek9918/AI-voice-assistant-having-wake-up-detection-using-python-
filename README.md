# AI Voice Assistant

An intelligent voice-activated assistant that combines wake-word detection, speech recognition, and conversational AI to provide hands-free interaction.

## Project Overview

This project is a full-featured voice assistant application built with Python that listens for a wake word, processes voice commands, generates intelligent responses using OpenAI's GPT, and synthesizes speech responses. It demonstrates integration of multiple AI/ML technologies and real-time audio processing.

## Key Features

- **Wake Word Detection**: Continuously monitors for wake words ("hey assistant", "hello assistant", "wake up")
- **Speech Recognition**: Converts voice input to text using Google Speech Recognition API
- **Conversational AI**: Generates contextually-aware responses using OpenAI's GPT-3.5-turbo
- **Text-to-Speech**: Converts responses back to natural-sounding speech using pyttsx3
- **Conversation Management**: Maintains conversation history for context-aware interactions
- **Configurable Settings**: Customizable audio parameters, sensitivity levels, and model settings
- **Logging & Error Handling**: Comprehensive logging and graceful error handling throughout

## Architecture

### Project Structure
```
AI voice assistant/
├── main.py                          # Entry point & main application logic
├── config.py                        # Configuration settings
├── requirements.txt                 # Python dependencies
├── test.py                          # Unit tests
├── layout.txt                       # UI layout configuration
├── modules/
│   ├── wake_word_detector.py        # Keyword spotting & wake word detection
│   ├── voice_processor.py           # Speech-to-text conversion
│   ├── chatgpt_handler.py           # OpenAI API integration
│   └── tts_engine.py                # Text-to-speech synthesis
└── utils/
    ├── audio_utils.py               # Audio processing utilities
    └── config_loader.py             # Configuration management
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│         AIVoiceAssistant (Main Orchestrator)            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │ WakeWordDetector │  │ VoiceProcessor   │             │
│  │ (Audio → Text)   │  │ (Speech → Text)  │             │
│  └────────┬─────────┘  └────────┬─────────┘             │
│           │                     │                       │
│           └─────────────┬───────┘                       │
│                         │                               │
│                   ┌─────▼──────┐                        │
│                   │ChatGPTHandler│                      │
│                   │(Text → Text) │                      │
│                   └─────┬────────┘                      │
│                         │                               │
│                    ┌────▼─────────┐                     │
│                    │ TTSEngine    │                     │
│                    │ (Text → Audio)│                    │
│                    └──────────────┘                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Core Modules

### 1. **WakeWordDetector** (`modules/wake_word_detector.py`)
- Continuously monitors microphone input
- Detects configured wake words with configurable sensitivity
- Initializes microphone and normalizes ambient noise
- **Key Method**: `detect()` - returns boolean for wake word presence

### 2. **VoiceProcessor** (`modules/voice_processor.py`)
- Captures audio from microphone with adaptive noise adjustment
- Converts speech to text using Google Speech Recognition
- Configurable timeout and phrase detection parameters
- **Key Method**: `listen(timeout=5, phrase_time_limit=10)` - returns recognized text

### 3. **ChatGPTHandler** (`modules/chatgpt_handler.py`)
- Interfaces with OpenAI API for conversational responses
- Maintains conversation context with message history
- Implements token limits and response length constraints
- System prompt ensures concise voice-appropriate responses
- **Key Method**: `get_response(user_input, conversation_history)` - returns AI response

### 4. **TTSEngine** (`modules/tts_engine.py`)
- Converts text responses to natural speech
- Configurable voice rate (words per minute) and volume
- Supports multiple voices with preference for female voices
- Thread-safe speech synthesis
- **Key Method**: `speak(text)` - plays audio response

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Speech Recognition | SpeechRecognition (Google API), PyAudio |
| NLP/AI | OpenAI GPT-3.5-turbo API |
| Text-to-Speech | pyttsx3 |
| Audio Processing | scipy, numpy, sounddevice |
| ML Models | PyTorch, Transformers |
| Environment | Python 3.8+, python-dotenv |

## Dependencies

```
openai>=1.0.0              # OpenAI API client
speechrecognition>=3.10.0  # Speech recognition
pyaudio>=0.2.11            # Audio I/O
pyttsx3>=2.90              # Text-to-speech
python-dotenv>=1.0.0       # Environment variables
numpy>=1.24.0              # Numerical computing
scipy>=1.10.0              # Scientific computing
sounddevice>=0.4.6         # Audio device interface
torch>=2.0.0               # PyTorch for ML
transformers>=4.30.0       # HuggingFace transformers
wakeword>=0.2.0            # Wake word detection
playsound>=1.3.0           # Audio playback
```

## Configuration

Key settings are managed in [config.py](config.py):

```python
# Wake Word Configuration
WAKE_WORDS = ["hey assistant", "hello assistant", "wake up"]
WAKE_WORD_SENSITIVITY = 0.5

# AI Model Configuration
CHATGPT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 150
TEMPERATURE = 0.7

# Audio Configuration
SAMPLE_RATE = 16000
ENERGY_THRESHOLD = 300
PAUSE_THRESHOLD = 0.8

# TTS Configuration
TTS_VOICE_RATE = 170  # Words per minute
TTS_VOICE_VOLUME = 0.9
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Microphone and speakers
- OpenAI API key

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "AI voice assistant"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   - Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## Usage

Once started, the assistant will:
1. Listen continuously for wake words
2. Upon detecting a wake word, say "Yes? How can I help you?"
3. Wait for your command
4. Process your voice input, send to ChatGPT, and speak the response
5. Continue listening for more commands
6. Exit on voice command like "goodbye" or keyboard interrupt (Ctrl+C)

### Example Interaction
```
User: "Hey assistant"
Assistant: "Yes? How can I help you?"
User: "What's the weather today?"
Assistant: [Speaks weather information from ChatGPT]
```

## Key Design Decisions

### 1. **Modular Architecture**
- Each component (wake detection, speech processing, AI, TTS) is independently encapsulated
- Allows easy testing, replacement, and scaling of individual modules

### 2. **Asynchronous Processing**
- Uses threading for concurrent audio processing and speech synthesis
- Prevents UI/response delays

### 3. **Configuration-Driven**
- All settings externalized to `config.py`
- Enables quick tuning without code changes
- Environment variables for sensitive data (API keys)

### 4. **Logging & Monitoring**
- Comprehensive logging at INFO level for debugging
- Structured error handling with try-catch blocks
- Helps identify bottlenecks and issues

### 5. **Conversation Context**
- Maintains conversation history for context-aware responses
- Implements token limit to avoid exceeding API limits
- Provides more natural multi-turn conversations

## Development Workflow

### Testing
Run unit tests:
```bash
python test.py
```

### Debugging
- Check logs in console output
- Adjust `LOG_LEVEL` in config.py for more verbose output
- Test individual components separately

### Performance Optimization
- Adjust `ENERGY_THRESHOLD` to filter background noise
- Tune `PAUSE_THRESHOLD` for faster command recognition
- Set `MAX_TOKENS` based on response quality vs. latency needs

## Error Handling

The application gracefully handles:
- Microphone unavailability
- Network/API failures
- Speech recognition failures
- Audio processing errors
- Keyboard interrupts for clean shutdown

## Interview Talking Points

1. **Full Stack Integration**: Demonstrates integration of multiple APIs (Google Speech Recognition, OpenAI, pyttsx3)

2. **Real-time Audio Processing**: Handles continuous audio stream with ambient noise adjustment

3. **Conversational Context**: Maintains conversation history for stateful interactions

4. **Configuration Management**: Externalized settings for flexibility and testing

5. **Error Resilience**: Comprehensive error handling and logging

6. **Modular Design**: Clean separation of concerns enabling independent component testing

7. **Performance Considerations**: Thread-safety, token management, and latency optimization

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Wake word customization at runtime
- [ ] Database storage for conversation history
- [ ] Integration with external APIs (weather, calendar, etc.)
- [ ] Advanced NLU for intent recognition
- [ ] Multi-user support with voice authentication
- [ ] Edge device optimization (TensorFlow Lite for wake word detection)
- [ ] Custom voice model training

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No audio detected | Check microphone permissions and ENERGY_THRESHOLD setting |
| Poor wake word detection | Adjust WAKE_WORD_SENSITIVITY in config.py |
| API errors | Verify OPENAI_API_KEY is set and has available credits |
| Speech synthesis issues | Check system audio output and TTS voice installation |


## Author

ABHISHEK
