#!/usr/bin/env python3
"""
decision_brain.py - ZIA-X Enhanced DecisionBrain Module V2.0

This module acts as ZIA's enhanced mastermind, providing intelligent analysis
of natural language commands with advanced intent recognition, context awareness,
and sophisticated decision-making capabilities.

Author: ZIA-X Development Team
Version: 2.0 - Production-Ready Enhanced Edition
"""

import logging
import re
import json
import time
import datetime
from typing import Dict, List, Union, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, Counter
import threading
from contextlib import contextmanager

@dataclass
class DecisionResult:
    """Structured decision result for better handling."""
    success: bool
    action: Optional[str] = None
    automation_command: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    confidence: float = 0.0
    intent: Optional[str] = None
    clarification_needed: bool = False
    clarification_message: Optional[str] = None
    execution_time: float = 0.0
    alternatives: Optional[List[str]] = None

@dataclass
class IntentMatch:
    """Represents an intent match with confidence scoring."""
    intent: str
    confidence: float
    matched_pattern: str
    extracted_entities: Dict[str, Any]

class DecisionBrain:
    """
    Enhanced intelligent decision-making brain for ZIA with advanced capabilities.
    Features context awareness, learning capabilities, and sophisticated NLP.
    """
    
    def __init__(self, cns, config):
        """
        Initialize the Enhanced DecisionBrain with advanced features.
        
        Args:
            cns: Central Nervous System object for inter-module communication
            config: Configuration object containing system settings
        """
        self.cns = cns
        self.config = config
        self.logger = self._setup_logger()
        
        # Enhanced configuration
        self.confidence_threshold = self.config.get('decision_brain', {}).get('confidence_threshold', 0.7)
        self.max_alternatives = self.config.get('decision_brain', {}).get('max_alternatives', 3)
        self.learning_enabled = self.config.get('decision_brain', {}).get('learning_enabled', True)
        self.context_window = self.config.get('decision_brain', {}).get('context_window', 5)
        
        # Initialize core components
        self._setup_knowledge_base()
        self._setup_intent_patterns()
        self._setup_entity_extractors()
        self._setup_context_manager()
        self._setup_learning_system()
        self._setup_performance_tracking()
        
        # Thread safety
        self._decision_lock = threading.Lock()
        
        self.logger.info("Enhanced DecisionBrain V2.0 initialized successfully")

    def _setup_logger(self) -> logging.Logger:
        """Setup enhanced logging."""
        logger = logging.getLogger(__name__)
        # Assuming CNS handles handler setup, just get the logger
        return logger

    def _setup_knowledge_base(self):
        """Setup enhanced knowledge base with hierarchical organization."""
        self.knowledge_base = {
            # Entertainment & Media
            "find_video": { "actions": ["search_youtube", "check_local_videos"], "priority": ["search_youtube"], "context_sensitive": True, "requires_topic": True },
            "play_music": { "actions": ["open_spotify", "search_youtube_music"], "priority": ["open_spotify"], "context_sensitive": True, "requires_topic": False },
            "entertainment": { "actions": ["search_youtube", "open_netflix", "open_spotify"], "priority": ["search_youtube"], "context_sensitive": True, "requires_topic": False },
            
            # Information & Search
            "get_info": { "actions": ["search_google", "search_wikipedia"], "priority": ["search_google"], "context_sensitive": True, "requires_topic": True },
            "search_web": { "actions": ["search_google", "search_bing"], "priority": ["search_google"], "context_sensitive": False, "requires_topic": True },
            "news_update": { "actions": ["search_google_news", "open_news_website"], "priority": ["search_google_news"], "context_sensitive": True, "requires_topic": False },
            
            # Web Navigation
            "open_website": { "actions": ["open_website"], "priority": ["open_website"], "context_sensitive": False, "requires_topic": True },
            "social_media": { "actions": ["open_facebook", "open_twitter", "open_instagram"], "priority": ["open_facebook"], "context_sensitive": True, "requires_topic": False },
            
            # System & Applications
            "system_check": { "actions": ["get_system_status", "check_performance"], "priority": ["get_system_status"], "context_sensitive": False, "requires_topic": False },
            "launch_app": { "actions": ["open_application"], "priority": ["open_application"], "context_sensitive": False, "requires_topic": True },
            
            # Productivity & Work
            "work_task": { "actions": ["open_notepad", "open_calculator"], "priority": ["open_notepad"], "context_sensitive": True, "requires_topic": False },
            "file_management": { "actions": ["open_explorer", "search_files"], "priority": ["open_explorer"], "context_sensitive": True, "requires_topic": False },
            "productivity": { "actions": ["open_calendar", "create_reminder"], "priority": ["open_calendar"], "context_sensitive": True, "requires_topic": False },
            
            # Learning & Education
            "learning": { "actions": ["search_educational_content", "find_tutorials"], "priority": ["search_educational_content"], "context_sensitive": True, "requires_topic": True },
            
            # Communication
            "communication": { "actions": ["open_email", "open_messaging"], "priority": ["open_email"], "context_sensitive": True, "requires_topic": False },
            
            # Shopping & Commerce
            "shopping": { "actions": ["search_products", "open_shopping_site"], "priority": ["search_products"], "context_sensitive": True, "requires_topic": True }
        }

    def _setup_intent_patterns(self):
        """Setup enhanced intent patterns with confidence scoring."""
        self.intent_patterns = {
            "find_video": {
                "high_confidence": [r"show me.*video.*about\s+(.+)", r"find.*video.*on\s+(.+)", r"search.*video.*(.+)", r"want.*watch.*video.*(.+)"],
                "medium_confidence": [r"show me.*(.+).*video", r"find.*(.+).*video", r"watch.*(.+)", r"video.*(.+)"],
                "low_confidence": [r"video", r"watch", r"show"]
            },
            "play_music": {
                "high_confidence": [r"play.*music.*by\s+(.+)", r"listen.*to\s+(.+).*music", r"put on.*(.+).*music"],
                "medium_confidence": [r"play.*music", r"listen.*music", r"some.*music"],
                "low_confidence": [r"music", r"song", r"play"]
            },
            "get_info": {
                "high_confidence": [r"what.*is\s+(.+)", r"tell me.*about\s+(.+)", r"search.*for\s+(.+)", r"explain\s+(.+)"],
                "medium_confidence": [r"what.*(.+)", r"about.*(.+)", r"info.*(.+)"],
                "low_confidence": [r"what", r"info", r"tell"]
            },
            "open_website": {
                "high_confidence": [r"open\s+(https?://[^\s]+)", r"go to\s+(www\.[^\s]+)"],
                "medium_confidence": [r"open\s+([a-zA-Z0-9-]+\.[a-zA-Z]{2,})", r"go to\s+([a-zA-Z0-9-]+\.[a-zA-Z]{2,})"],
                "low_confidence": [r"open.*\.com", r"website"]
            },
            "system_check": {
                "high_confidence": [r"system.*status", r"check.*system.*performance", r"performance.*report"],
                "medium_confidence": [r"check.*system", r"system.*info", r"performance"],
                "low_confidence": [r"system", r"status", r"check"]
            },
            "launch_app": {
                "high_confidence": [r"open\s+(notepad|calculator|paint|word|excel)", r"launch\s+(notepad|calculator|paint)"],
                "medium_confidence": [r"open\s+([a-zA-Z]+)", r"launch\s+([a-zA-Z]+)"],
                "low_confidence": [r"open", r"launch", r"start"]
            },
            "search_web": {
                "high_confidence": [r"google.*for\s+(.+)", r"search.*google.*(.+)", r"look up.*(.+).*online"],
                "medium_confidence": [r"google.*(.+)", r"search.*(.+)", r"look up.*(.+)"],
                "low_confidence": [r"google", r"search"]
            },
            "entertainment": {
                "high_confidence": [r"entertain.*me", r"something.*fun.*to.*do", r"i.*am.*bored"],
                "medium_confidence": [r"something.*fun", r"bored", r"entertainment"],
                "low_confidence": [r"fun", r"entertain"]
            },
            "work_task": {
                "high_confidence": [r"need.*help.*with.*work", r"work.*related.*task"],
                "medium_confidence": [r"work.*task", r"office.*task", r"document.*work"],
                "low_confidence": [r"work", r"office"]
            },
            "file_management": {
                "high_confidence": [r"find.*file.*named\s+(.+)", r"open.*folder.*(.+)"],
                "medium_confidence": [r"find.*file", r"open.*folder", r"browse.*files"],
                "low_confidence": [r"file", r"folder", r"explorer"]
            },
            "news_update": {
                "high_confidence": [r"latest.*news.*about\s+(.+)", r"news.*today.*(.+)"],
                "medium_confidence": [r"latest.*news", r"news.*today", r"current.*events"],
                "low_confidence": [r"news", r"events"]
            },
            "social_media": {
                "high_confidence": [r"open\s+(facebook|twitter|instagram|linkedin|tiktok)", r"check\s+(facebook|twitter|instagram)"],
                "medium_confidence": [r"social.*media", r"check.*social"],
                "low_confidence": [r"social", r"facebook", r"twitter"]
            },
            "learning": {
                "high_confidence": [r"learn.*about\s+(.+)", r"tutorial.*on\s+(.+)", r"teach.*me\s+(.+)"],
                "medium_confidence": [r"learn.*(.+)", r"tutorial.*(.+)", r"how.*to.*(.+)"],
                "low_confidence": [r"learn", r"tutorial", r"teach"]
            },
            "productivity": {
                "high_confidence": [r"schedule.*appointment.*(.+)", r"reminder.*for\s+(.+)", r"organize.*(.+)"],
                "medium_confidence": [r"schedule.*(.+)", r"calendar.*(.+)", r"reminder.*(.+)"],
                "low_confidence": [r"schedule", r"calendar", r"reminder"]
            },
            "communication": {
                "high_confidence": [r"send.*email.*to\s+(.+)", r"call\s+(.+)", r"message\s+(.+)"],
                "medium_confidence": [r"send.*email", r"make.*call", r"send.*message"],
                "low_confidence": [r"email", r"call", r"message"]
            },
            "shopping": {
                "high_confidence": [r"buy\s+(.+)", r"shop.*for\s+(.+)", r"purchase\s+(.+)"],
                "medium_confidence": [r"shopping.*(.+)", r"buy.*(.+)", r"price.*(.+)"],
                "low_confidence": [r"buy", r"shop", r"purchase"]
            }
        }

    def _setup_entity_extractors(self):
        """Setup enhanced entity extraction patterns."""
        self.entity_extractors = {
            "time": [r"at\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)", r"(\d{1,2}\s*(?:am|pm))"],
            "date": [r"(\d{1,2}/\d{1,2}/\d{2,4})", r"(\d{1,2}-\d{1,2}-\d{2,4})"],
            "person": [r"(?:call|to|message|email)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"],
            "location": [r"(?:in|at|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"],
        }

    def _setup_context_manager(self):
        """Setup context management for conversation awareness."""
        self.conversation_history = []
        self.session_context = { "last_intent": None, "time_of_day": self._get_time_context() }

    def _setup_learning_system(self):
        """Setup learning and adaptation system."""
        self.user_preferences = defaultdict(Counter)
        # Placeholder for loading/saving learning data
        self.learning_data_path = Path("config/learning_data.json")

    def _setup_performance_tracking(self):
        """Setup comprehensive performance tracking."""
        self.performance_stats = {
            'total_decisions': 0, 'successful_decisions': 0, 'clarifications_needed': 0,
            'average_confidence': 0.0, 'average_processing_time': 0.0,
            'intent_distribution': Counter(), 'session_start_time': datetime.datetime.now()
        }
    @contextmanager
    def _performance_timer(self):
        """Context manager for performance timing."""
        start_time = time.time()
        try:
            yield
        finally:
            execution_time = time.time() - start_time
            self._update_performance_stats(execution_time)

    def _update_performance_stats(self, execution_time: float):
        """Update performance statistics."""
        total = self.performance_stats['total_decisions']
        current_avg_time = self.performance_stats['average_processing_time']
        self.performance_stats['average_processing_time'] = (
            (current_avg_time * total + execution_time) / (total + 1)
        )

    def _get_time_context(self) -> str:
        """Get current time context."""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12: return "morning"
        elif 12 <= hour < 17: return "afternoon"
        elif 17 <= hour < 21: return "evening"
        else: return "night"

    def _determine_intent_with_confidence(self, command: str) -> List[IntentMatch]:
        """Enhanced intent determination with confidence scoring."""
        command_lower = command.lower().strip()
        intent_matches = []
        
        for intent, pattern_groups in self.intent_patterns.items():
            best_confidence = 0.0
            best_pattern = ""
            best_entities = {}
            
            for confidence_level, base_confidence in [("high_confidence", 0.9), ("medium_confidence", 0.6), ("low_confidence", 0.3)]:
                if confidence_level not in pattern_groups: continue
                
                for pattern in pattern_groups[confidence_level]:
                    match = re.search(pattern, command_lower)
                    if match:
                        pattern_confidence = base_confidence
                        if match.group(0) == command_lower: pattern_confidence += 0.1
                        match_ratio = len(match.group(0)) / len(command_lower)
                        pattern_confidence += match_ratio * 0.1
                        
                        entities = self._extract_entities_from_match(match, command)
                        
                        if pattern_confidence > best_confidence:
                            best_confidence = pattern_confidence
                            best_pattern = pattern
                            best_entities = entities
            
            if best_confidence > 0:
                intent_matches.append(IntentMatch(
                    intent=intent,
                    confidence=min(best_confidence, 1.0),
                    matched_pattern=best_pattern,
                    extracted_entities=best_entities
                ))
        
        intent_matches.sort(key=lambda x: x.confidence, reverse=True)
        return self._apply_context_boosting(intent_matches, command)

    def _extract_entities_from_match(self, match, command: str) -> Dict[str, Any]:
        """Extract entities from regex match and command."""
        entities = {}
        if match.groups():
            entities['primary_entity'] = match.group(1).strip()
        
        for entity_type, patterns in self.entity_extractors.items():
            for pattern in patterns:
                entity_match = re.search(pattern, command, re.IGNORECASE)
                if entity_match:
                    entities[entity_type] = entity_match.group(1)
                    break
        return entities

    def _apply_context_boosting(self, intent_matches: List[IntentMatch], command: str) -> List[IntentMatch]:
        """Apply context-based confidence boosting."""
        if self.session_context['last_intent']:
            for match in intent_matches:
                if match.intent == self.session_context['last_intent']:
                    match.confidence = min(1.0, match.confidence + 0.1)
        
        time_context = self.session_context['time_of_day']
        time_boosts = {
            "morning": ["news_update", "productivity"],
            "evening": ["entertainment", "find_video"],
            "night": ["entertainment", "play_music"]
        }
        for match in intent_matches:
            if match.intent in time_boosts.get(time_context, []):
                match.confidence = min(1.0, match.confidence + 0.05)
        
        intent_matches.sort(key=lambda x: x.confidence, reverse=True)
        return intent_matches
    def _extract_enhanced_parameters(self, command: str, intent_match: IntentMatch) -> Dict[str, Any]:
        """Enhanced parameter extraction with entity recognition."""
        parameters = intent_match.extracted_entities.copy()
        command_lower = command.lower()
        intent = intent_match.intent
        
        # Standardize primary entity to a common key like 'topic' or 'target'
        if 'primary_entity' in parameters:
            if intent in ["find_video", "get_info", "search_web", "learning"]:
                parameters['topic'] = parameters['primary_entity']
            elif intent in ["play_music"]:
                parameters['music_query'] = parameters['primary_entity']
            elif intent in ["open_website"]:
                parameters['url'] = parameters['primary_entity']
            elif intent in ["launch_app"]:
                parameters['application'] = parameters['primary_entity']
        
        return parameters

    def _create_enhanced_clarification(self, intent: str, possible_actions: List[str], parameters: Dict[str, Any]) -> str:
        """Create enhanced clarification messages with context awareness."""
        clarification_templates = {
            "find_video": "CLARIFY:I can search YouTube for '{topic}' or check your local files. Which one, Boss?",
            "play_music": "CLARIFY:I can play '{music_query}' on Spotify or YouTube Music. What's your preference?",
        }
        
        template = clarification_templates.get(intent)
        if template:
            # Use a default value if a parameter is missing for the template
            topic = parameters.get('topic', 'videos')
            music_query = parameters.get('music_query', 'music')
            return template.format(topic=topic, music_query=music_query)
        
        action_list = ", ".join([act.replace("_", " ") for act in possible_actions[:3]])
        return f"CLARIFY:I have a few options for that: {action_list}. Which should I use, Boss?"
    def _map_action_to_automation_enhanced(self, action: str, parameters: Dict[str, Any], intent: str) -> Dict[str, Any]:
        """Enhanced action mapping with context awareness and parameter integration."""
        command = action # Default command is the action itself
        
        if action == "search_youtube":
            command = f"search youtube for {parameters.get('topic', 'videos')}"
        elif action == "search_youtube_music":
            command = f"search youtube for {parameters.get('music_query', 'music')} music"
        elif action == "open_spotify":
            command = "open spotify.com"
        elif action == "search_google":
            command = f"search for {parameters.get('topic', 'information')}"
        elif action == "open_website":
            command = f"open {parameters.get('url', 'google.com')}"
        elif action == "open_application":
            command = f"open {parameters.get('application', 'notepad')}"
        
        return {
            'action': action,
            'automation_command': command,
            'description': f"Execute {action} for intent {intent}",
            'intent': intent,
            'parameters': parameters
        }

    def make_decision(self, command: str) -> Union[DecisionResult, str, None]:
        """Enhanced main decision-making method with comprehensive analysis."""
        if not command or not command.strip():
            return DecisionResult(success=False, clarification_message="Boss, I need a command to process.")
            
        self.logger.info(f"Making enhanced decision for command: {command}")
        
        with self._decision_lock, self._performance_timer() as timer:
            try:
                self.performance_stats['total_decisions'] += 1
                
                intent_matches = self._determine_intent_with_confidence(command)
                if not intent_matches:
                    return None
                
                best_match = intent_matches[0]
                intent, confidence = best_match.intent, best_match.confidence
                
                self.logger.info(f"Best intent: {intent} (confidence: {confidence:.2f})")
                
                if confidence < self.confidence_threshold:
                    alternatives = [match.intent for match in intent_matches[:self.max_alternatives]]
                    return DecisionResult(
                        success=False, intent=intent, confidence=confidence, clarification_needed=True,
                        clarification_message=f"CLARIFY:I'm not entirely sure, Boss. Did you mean: {', '.join(alternatives)}?",
                        alternatives=alternatives
                    )
                
                parameters = self._extract_enhanced_parameters(command, best_match)
                
                intent_config = self.knowledge_base.get(intent, {})
                possible_actions = intent_config.get("actions", [])
                
                if not possible_actions: return None
                
                action_to_take = possible_actions[0]
                if len(possible_actions) > 1:
                    if intent_config.get("context_sensitive"):
                        action_to_take = self._select_best_action(intent, parameters, self.session_context)
                    else:
                        self.performance_stats['clarifications_needed'] += 1
                        clarification = self._create_enhanced_clarification(intent, possible_actions, parameters)
                        return DecisionResult(
                            success=False, intent=intent, confidence=confidence, clarification_needed=True,
                            clarification_message=clarification, alternatives=possible_actions
                        )
                
                automation_mapping = self._map_action_to_automation_enhanced(action_to_take, parameters, intent)
                
                result = DecisionResult(
                    success=True, action=action_to_take,
                    automation_command=automation_mapping['automation_command'],
                    parameters=parameters, confidence=confidence, intent=intent
                )
                
                self._update_conversation_history(command, intent, result)
                self._learn_from_interaction(command, intent, True)
                self.performance_stats['successful_decisions'] += 1
                
                return result
                
            except Exception as e:
                self.logger.error(f"Error in enhanced decision making: {str(e)}", exc_info=True)
                self._learn_from_interaction(command, "", False)
                return DecisionResult(success=False, clarification_message=f"Boss, I had an error in my thought process: {type(e).__name__}")
    def _select_best_action(self, intent: str, parameters: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Intelligently select the best action based on context and user preferences."""
        intent_config = self.knowledge_base[intent]
        possible_actions = intent_config["actions"]
        priority_actions = intent_config.get("priority", possible_actions)
        
        # Start with the highest priority action
        best_action = priority_actions[0]
        
        # Check user preferences
        if self.user_preferences[intent]:
            # Get the most common action the user prefers for this intent
            most_common_action = self.user_preferences[intent].most_common(1)[0][0]
            if most_common_action in possible_actions:
                best_action = most_common_action
        
        return best_action

    def _update_conversation_history(self, command: str, intent: str, result: DecisionResult):
        """Update conversation history for context awareness."""
        history_entry = {'command': command, 'intent': intent, 'action': result.action}
        self.conversation_history.append(history_entry)
        if len(self.conversation_history) > self.context_window:
            self.conversation_history.pop(0)
        self.session_context['last_intent'] = intent

    def _learn_from_interaction(self, command: str, intent: str, success: bool, user_feedback: str = None):
        """Learn from user interactions to improve future decisions."""
        if not self.learning_enabled: return
        
        if success and intent:
            # This is a simplified learning mechanism
            # A real one would adjust weights or retrain models
            self.user_preferences[intent][command] += 1

    def _load_learning_data(self):
        """Load existing learning data from storage."""
        if self.learning_data_path.exists():
            try:
                with open(self.learning_data_path, 'r') as f:
                    data = json.load(f)
                    self.user_preferences = defaultdict(Counter, {k: Counter(v) for k, v in data.get("user_preferences", {}).items()})
                self.logger.info("Learning data loaded successfully")
            except Exception as e:
                self.logger.warning(f"Could not load learning data: {e}")

    def _save_learning_data(self):
        """Save learning data to storage."""
        if not self.learning_enabled: return
        try:
            with open(self.learning_data_path, 'w') as f:
                serializable_prefs = {k: dict(v) for k, v in self.user_preferences.items()}
                json.dump({"user_preferences": serializable_prefs}, f, indent=2)
            self.logger.info("Learning data saved successfully")
        except Exception as e:
            self.logger.warning(f"Could not save learning data: {e}")

    def handle_clarification_response(self, original_command: str, clarification_response: str) -> Union[DecisionResult, None]:
        """Handle user response to clarification requests."""
        self.logger.info(f"Handling clarification response: {clarification_response}")
        # This is a simplified handler. A more advanced version would parse the choice.
        # For now, we assume the user's response contains a keyword for the desired action.
        
        intent_matches = self._determine_intent_with_confidence(original_command)
        if not intent_matches: return None
        
        best_match = intent_matches[0]
        intent = best_match.intent
        possible_actions = self.knowledge_base.get(intent, {}).get("actions", [])
        
        for action in possible_actions:
            if action.replace("_", " ") in clarification_response.lower():
                parameters = self._extract_enhanced_parameters(original_command, best_match)
                automation_mapping = self._map_action_to_automation_enhanced(action, parameters, intent)
                
                result = DecisionResult(
                    success=True, action=action,
                    automation_command=automation_mapping['automation_command'],
                    parameters=parameters, confidence=best_match.confidence, intent=intent
                )
                self._learn_from_interaction(original_command, intent, True, clarification_response)
                return result

        return DecisionResult(success=False, clarification_needed=True, clarification_message="CLARIFY:I didn't understand that choice, Boss.")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        total = self.performance_stats['total_decisions']
        success_rate = (self.performance_stats['successful_decisions'] / total * 100) if total > 0 else 0
        uptime = datetime.datetime.now() - self.performance_stats['session_start_time']
        
        return {
            **self.performance_stats,
            'success_rate_percent': round(success_rate, 1),
            'session_uptime': str(uptime).split('.')[0]
        }

    def shutdown(self):
        """Graceful shutdown of Enhanced DecisionBrain."""
        self.logger.info("Enhanced DecisionBrain shutting down...")
        self._save_learning_data()
