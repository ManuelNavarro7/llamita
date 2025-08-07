#!/usr/bin/env python3
"""
Configuration file for Voice Assistant
Modify these settings to customize your experience
"""

# Ollama Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3:8b"  # Using the model you have installed

# Available models you can use (recommended for Llamita):
# - "llama3.2:3b" - Very fast, lightweight, great for chat (RECOMMENDED)
# - "llama3.2:1b" - Ultra-fast, smallest model
# - "gemma2:2b" - Fast and efficient
# - "phi3:mini" - Microsoft's lightweight model
# - "qwen2.5:0.5b" - Very small but surprisingly capable
# - "mistral:7b" - Good balance if you want more capability
# - "llama3:8b" - More capable but slower
# - "codellama:7b" - Specialized for coding tasks

# Speech Recognition Configuration
SPEECH_TIMEOUT = 5  # Seconds to wait for speech input
PHRASE_TIME_LIMIT = 10  # Maximum length of a phrase in seconds
AMBIENT_NOISE_DURATION = 1  # Seconds to adjust for ambient noise

# Text-to-Speech Configuration
TTS_VOICE = None  # Set to a specific voice (e.g., "Alex", "Victoria") or None for default
TTS_RATE = None  # Speech rate (words per minute) or None for default
SPEECH_PREPARATION_DELAY = 0.2  # Seconds to wait before starting speech
RESPONSE_PREPARATION_DELAY = 0.5  # Seconds to wait after getting response before speaking
VOICE_INTERRUPTION_ENABLED = True  # Enable voice interruption during speech
VOICE_INTERRUPTION_TIMEOUT = 1  # Seconds to wait for interruption detection

# GUI Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "🦙 Llamita - Voice Assistant"

# Color Scheme
COLORS = {
    'background': '#2c3e50',
    'secondary': '#34495e',
    'text': '#ecf0f1',
    'text_secondary': '#bdc3c7',
    'success': '#3498db',  # Blue
    'warning': '#f39c12',  # Orange
    'error': '#e74c3c',    # Red
    'info': '#3498db',     # Blue
    'button_bg': '#3498db', # Blue button background
    'button_fg': '#ffffff', # White button text color
    'button_active': '#2980b9',  # Darker blue for active state
    'button_disabled': '#95a5a6'  # Gray for disabled state
}

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE = False  # Set to True to save logs to a file
LOG_FILE = "voice_assistant.log"

# Advanced Configuration
ENABLE_DEBUG_MODE = False  # Set to True for verbose logging
SAVE_CONVERSATIONS = True  # Save conversation history
CONVERSATION_FILE = "conversations.txt"

# System Prompts (optional - for more advanced model control)
SYSTEM_PROMPTS = {
    "default": "You are Llamita, an intelligent and helpful AI assistant. You are friendly, knowledgeable, and always ready to help with any questions or tasks. Keep your responses clear, informative, and conversational. You have expertise in many areas and can assist with coding, writing, analysis, problem-solving, and general conversation.",
    "coding": "You are Llamita, a coding assistant. Provide clear, practical code examples and explanations.",
    "creative": "You are Llamita, a creative assistant. Be imaginative, engaging, and inspiring in your responses."
}

# Voice Commands (optional - for custom voice shortcuts)
VOICE_COMMANDS = {
    "stop listening": "stop_listening",
    "clear chat": "clear_chat",
    "what time is it": "get_time",
    "what's the date": "get_date"
}
