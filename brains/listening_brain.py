#!/usr/bin/env python3
"""
VITA-X Listening Brain Module (V.0.6 - Max Sensitivity)
====================================================
This module handles wake word detection and speech-to-text processing.
This version uses a highly sensitive "contains" check for the wake word.
"""

import threading
import logging
import sounddevice as sd
import vosk
import json
import time
from pathlib import Path
import queue

class ListeningBrain:
    """
    Production-ready ListeningBrain with a robust state machine.
    """
    
    def __init__(self, cns, config):
        """
        Initializes the ListeningBrain.
        Args:
            cns: The Central Nervous System object.
            config: A dictionary with configuration settings.
        """
        self.cns = cns
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # State Management
        self.STATE_WAKE_WORD = "WAKE_WORD"
        self.STATE_COMMAND = "COMMAND"
        self.current_state = self.STATE_WAKE_WORD
        
        # Threading and control
        self._thread = None
        self._is_running = False
        
        # Config
        self.wake_words = self.config.get('wake_words', ['zia'])
        self.model_path = self.config.get('vosk_model_path')
        self.command_timeout = self.config.get('command_timeout', 5)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.85)
        self.sample_rate = 16000
        self.block_size = 4000
        self.command_listen_start_time = 0

        # Vosk Initialization
        self.model = None
        self.recognizer = None
        self._setup_vosk()

    def _setup_vosk(self):
        """Loads the Vosk model and prepares the recognizer."""
        try:
            if not Path(self.model_path).exists():
                self.logger.error(f"Vosk model not found at: {self.model_path}")
                raise FileNotFoundError("Vosk model path is invalid.")
            
            self.logger.info(f"Loading Vosk model from: {self.model_path}")
            self.model = vosk.Model(self.model_path)
            # Create a recognizer that we will reconfigure
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            self._configure_for_wake_word()
            self.logger.info("Vosk setup complete.")
        except Exception as e:
            self.logger.critical(f"Failed to initialize Vosk: {e}", exc_info=True)
            raise

    def _configure_for_wake_word(self):
        """Configures the recognizer to listen only for wake words."""
        self.logger.info(f"Configuring for WAKE WORD mode. Listening for: {self.wake_words}")
        # We use a grammar list for efficient wake word spotting
        grammar = json.dumps(self.wake_words, ensure_ascii=False)
        self.recognizer.SetGrammar(grammar)
        self.current_state = self.STATE_WAKE_WORD

    def run(self):
        """The main listening loop that runs in a separate thread."""
        self.logger.info("🎧 Listening Brain thread started.")
        self._is_running = True

        try:
            # Use a callback-based stream for continuous, non-blocking audio processing
            with sd.RawInputStream(samplerate=self.sample_rate, blocksize=self.block_size, 
                                   dtype='int16', channels=1, callback=self._audio_callback):
                self.logger.info(f"🎤 ZIA is now listening...")
                while self._is_running:
                    time.sleep(0.1)

        except Exception as e:
            self.logger.critical(f"Failed to start audio stream: {e}", exc_info=True)
        finally:
            self.logger.info("🎧 Listening Brain thread stopped.")

    def _audio_callback(self, indata, frames, audio_time, status):
        """This function is called for each audio block from the microphone."""
        if not self._is_running or self.current_state != self.STATE_WAKE_WORD:
            return
        if status:
            self.logger.warning(f"Audio stream status: {status}")

        # --- V.0.6 MAX SENSITIVITY LOGIC ---
        if self.recognizer.AcceptWaveform(bytes(indata)):
            result_json = json.loads(self.recognizer.Result())
            result_text = result_json.get("text", "").strip()
            
            # Check if any wake word is simply contained in the result
            if any(word in result_text for word in self.wake_words):
                self.logger.info(f"Wake word detected: '{result_text}'")
                self._handle_wake_word()

    def _handle_wake_word(self):
        """Handles the logic after a wake word is detected."""
        if self.current_state == self.STATE_WAKE_WORD:
            self.current_state = self.STATE_COMMAND # Lock the state to prevent multiple triggers
            threading.Thread(target=self._listen_for_command_task).start()

    def _listen_for_command_task(self):
        """The actual task of listening for a command."""
        self.logger.info("👂 Switching to command mode...")
        print("👂 Listening for command...")
        
        # Create a new, temporary recognizer for the command
        command_recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
        
        q = queue.Queue()

        def command_callback(indata, frames, time, status):
            q.put(bytes(indata))

        try:
            with sd.RawInputStream(samplerate=self.sample_rate, blocksize=self.block_size, 
                                   dtype='int16', channels=1, callback=command_callback):
                
                start_time = time.time()
                while time.time() - start_time < self.command_timeout:
                    try:
                        data = q.get(timeout=0.1)
                        if command_recognizer.AcceptWaveform(data):
                            result = json.loads(command_recognizer.Result())
                            command_text = result.get("text", "").strip()
                            if command_text:
                                self.cns.handle_command(command_text)
                                return 
                    except queue.Empty:
                        continue
                
                self.logger.info("⏱️ Command listening timeout.")
                print("⏱️ Command listening timeout.")

        except Exception as e:
            self.logger.error(f"Error during command listening task: {e}", exc_info=True)
        finally:
            # Always switch back to wake word mode
            self._configure_for_wake_word()
            print("🎤 Listening for wake words...")

    def start(self):
        """Starts the listening brain thread."""
        if self._is_running:
            return
        self.logger.info("🚀 Starting ListeningBrain...")
        self._is_running = True
        self._thread = threading.Thread(target=self.run, name="ListeningBrain")
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """Stops the listening brain thread."""
        if not self._is_running:
            return
        self.logger.info("🛑 Stopping ListeningBrain...")
        self._is_running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self.logger.info("✅ ListeningBrain stopped.")
