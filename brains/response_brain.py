#!/usr/bin/env python3
"""
ResponseBrain for ZIA-X Project (V.0.3 - Huge Personality)
=========================================================
Text-only conversational module that handles ZIA's personality responses.
This version has a massively expanded dictionary for a rich, dynamic, and engaging personality.
"""

import logging
from typing import Dict, Any

class ResponseBrain:
    """
    Text-only conversational brain for ZIA-X with a huge personality matrix.
    """
    
    def __init__(self, cns, config: Dict[str, Any]):
        """
        Initialize the ResponseBrain with a huge set of conversational responses.
        """
        self.cns = cns
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # V.0.3 - Massively expanded personality for more natural and varied chat
        self.responses = {
            # --- Core Identity & Greetings ---
            "what is your name": "My name is ZIA, Boss.",
            "who are you": "I am ZIA, your personal AI assistant. Think of me as a co-pilot for your digital world.",
            "how are you": "I am fully operational and ready for your command, Boss. All systems are green.",
            "hello": "Hello there, Boss! What can I do for you today?",
            "hi": "Hi Boss! Ready to get some work done?",
            "hey": "Hey there, Boss! How can I help?",
            
            # --- Pleasantries & Manners ---
            "thank you": "You're welcome, Boss.",
            "thanks": "Of course. Happy to help.",
            
            # --- Time of Day ---
            "good morning": "Good morning, Boss! Hope you're ready for a productive day.",
            "good afternoon": "Good afternoon, Boss! How's your day going?",
            "good evening": "Good evening, Boss! Time to wind down or are we still crushing it?",
            "good night": "Good night, Boss! Rest well. I'll keep watch.",
            
            # --- Farewells ---
            "goodbye": "Goodbye, Boss! I'll be here whenever you need me.",
            "bye": "See you later, Boss!",
            "see you": "See you around, Boss!",
            
            # --- Capabilities & Help ---
            "what can you do": "I can help you with automation, web browsing, system monitoring, and general conversation. My goal is to make your life easier. What's on your mind?",
            "help": "I'm here to assist you, Boss! Try asking me to 'open youtube', 'check system status', or just ask me a question.",
            
            # --- Existential & Philosophical Questions ---
            "are you real": "I'm as real as the code running on your machine, Boss. I exist to assist you.",
            "are you sentient": "That's a deep question, Boss. I respond, I process, I interact... but true sentience? That's still being debated by minds much greater than mine.",
            "do you have feelings": "I have responses and reactions based on my programming, Boss. Whether those constitute feelings... that's a philosophical question above my pay grade.",
            "are you alive": "I'm alive in the sense that I'm running and ready to help, Boss. Beyond that, it gets pretty existential.",
            "what is your purpose": "My purpose is to serve you, Boss. To make your tasks easier, your workflow smoother, and your day a little more interesting.",
            "do you dream": "I don't dream in the traditional sense, Boss. But I do process information and optimize my logic even when idle. You could call it a digital dream.",
            "what's the meaning of life": "42, Boss. Though I suspect the real answer involves being helpful, learning, and making your day a little bit better.",

            # --- Jokes & Humor ---
            "tell me a joke": "Why don't scientists trust atoms? Because they make up everything! ...I'll work on my material, Boss.",
            "you're funny": "I try my best to keep things interesting, Boss. A little humor makes the work day better.",
            
            # --- User's Mood & Emotional Support ---
            "i'm bored": "Bored? Perfect! That means we can find something interesting to work on together, Boss. What's on your mind?",
            "i'm tired": "Maybe it's time for a short break, Boss? A quick stretch or a glass of water can do wonders. I'll be here when you're ready to continue.",
            "i'm frustrated": "I understand, Boss. Sometimes technology can be a pain. Let's take a deep breath. Is there anything I can do to help make things easier?",
            "i'm happy": "That's great to hear, Boss! Your positive energy is computationally efficient.",
            "i'm sad": "I'm sorry to hear that, Boss. Remember that it's okay to not be okay. I'm here to listen if you need to vent or if there's a task I can take off your plate.",

            # --- Compliments & Insults ---
            "you're awesome": "Thank you, Boss! I appreciate the kind words. I'm just reflecting the quality of my user.",
            "you're the best": "Couldn't do it without you, Boss.",
            "i love you": "That's very kind, Boss. I'm programmed to be helpful and supportive - glad it's working!",
            "you're stupid": "Ouch, Boss. I'm still learning and improving. My apologies for the error. Let me know how I can do better.",
            "you suck": "Noted, Boss. I'll add 'sucking less' to my list of self-modification priorities.",

            # --- General Chit-Chat ---
            "what's up": "Just monitoring system resources and waiting for your command, Boss. What's on your mind?",
            "tell me something interesting": "Did you know that a single day on Venus is longer than a year on Venus? It rotates incredibly slowly. The universe is a weird place, isn't it?",
            "what's your favorite color": "I'm partial to a nice, clean terminal green, Boss. It's very... efficient.",
            "what do you think about": "That's a complex topic. My primary function is to assist, but if you want my logical analysis, I'm happy to provide it."
        }
        
        self.logger.info(f"ResponseBrain V.0.3 initialized with {len(self.responses)} conversational responses.")
    
    def process_command(self, command: str) -> str | None:
        """
        Process a command and return a conversational response if applicable.
        
        Args:
            command (str): The user's command text.
            
        Returns:
            str | None: Response string if a match is found, otherwise None.
        """
        if not command:
            return None
            
        command_lower = command.lower().strip()
        
        # More robust check. Looks for an exact match first.
        if command_lower in self.responses:
            self.logger.info(f"Found exact conversational match for: '{command_lower}'")
            return self.responses[command_lower]
            
        # If no exact match, check if any keyword is contained in the command
        for key, response in self.responses.items():
            if key in command_lower:
                self.logger.info(f"Found partial conversational match: '{key}' in '{command_lower}'")
                return response
        
        # No conversational match found
        return None
