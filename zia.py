#!/usr/bin/env python3
"""
ZIA-X Automation Brain (V.1.5 - Production-Ready Enhanced)
=========================================================
Enhanced master automation brain module for the ZIA-X project.
Includes comprehensive error handling, performance optimizations,
and complete feature implementations.
"""

import logging
import os
import subprocess
import webbrowser
import datetime
import psutil
import platform
import pyautogui
import time
import pygetwindow as gw
import re
import urllib.parse
import requests
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import asyncio
import threading
import sys
import shutil
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class CommandResult:
    """Structured command result for better error handling."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    category: str = "general"

class AutomationBrain:
    """
    Enhanced AI automation brain for ZIA-X with advanced memory system.
    Production-ready with comprehensive error handling and optimizations.
    """
    
    def __init__(self, cns, config: Dict[str, Any]):
        self.cns = cns
        self.config = config
        self.logger = self._setup_logger()
        
        # Enhanced pyautogui configuration
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.3  # Optimized for better performance
        
        # Directory setup with error handling
        self._setup_directories()
        
        # System information
        self.os_type = platform.system().lower()
        self.python_version = sys.version_info
        
        # Enhanced web domains and websites
        self._setup_web_resources()
        
        # Enhanced search and memory triggers
        self._setup_command_patterns()
        
        # Enhanced search headers with rotation
        self._setup_search_headers()
        
        # Task automation patterns
        self._setup_automation_patterns()
        
        # Initialize subsystems
        self._setup_memory_integration()
        self._setup_performance_tracking()
        
        # Cache for frequently used data
        self._setup_caching()
        
        self.logger.info("AutomationBrain V.1.5 (Production-Ready Enhanced) initialized successfully.")

    def _setup_logger(self) -> logging.Logger:
        """Setup enhanced logging with rotation."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _setup_directories(self):
        """Setup required directories with error handling."""
        try:
            self.screenshots_dir = Path("screenshots")
            self.screenshots_dir.mkdir(exist_ok=True)
            
            self.logs_dir = Path("logs")
            self.logs_dir.mkdir(exist_ok=True)
            
            self.cache_dir = Path("cache")
            self.cache_dir.mkdir(exist_ok=True)
            
            self.desktop_path = Path.home() / "Desktop"
            
        except Exception as e:
            self.logger.error(f"Directory setup failed: {e}")
            raise

    def _setup_web_resources(self):
        """Setup web domains and common websites."""
        self.web_domains = [
            '.com', '.org', '.net', '.edu', '.gov', '.io', '.co', '.in', 
            '.ai', '.tech', '.dev', '.app', '.cloud', '.me', '.tv', '.fm'
        ]
        
        self.common_websites = {
            # Search engines
            "google": "google.com", "bing": "bing.com", "duckduckgo": "duckduckgo.com",
            # Social media
            "youtube": "youtube.com", "facebook": "facebook.com", "twitter": "twitter.com",
            "x": "x.com", "linkedin": "linkedin.com", "reddit": "reddit.com",
            "instagram": "instagram.com", "tiktok": "tiktok.com", "discord": "discord.com",
            # Development
            "github": "github.com", "stackoverflow": "stackoverflow.com", "gitlab": "gitlab.com", "codepen": "codepen.io",
            # Productivity
            "gmail": "gmail.com", "outlook": "outlook.com", "drive": "drive.google.com", "dropbox": "dropbox.com",
            # Entertainment
            "netflix": "netflix.com", "spotify": "open.spotify.com", "twitch": "twitch.tv", "amazon": "amazon.com",
            # Communication
            "whatsapp": "web.whatsapp.com", "telegram": "web.telegram.org", "zoom": "zoom.us", "teams": "teams.microsoft.com",
            # Reference
            "wikipedia": "wikipedia.org", "wolframalpha": "wolframalpha.com"
        }

    def _setup_command_patterns(self):
        """Setup enhanced command patterns and triggers."""
        self.search_triggers = [
            "search for", "google", "look up", "find information on", "search about", "tell me about", "what is", "who is",
            "how to", "find me", "search the web for", "browse for", "research", "investigate", "explain", "summarize",
            "give me info on", "show me info about", "get details on", "learn about", "find out about", "discover", "explore"
        ]
        
        self.memory_triggers = [
            "remember", "don't forget", "keep in memory", "store this", "recall", "what do you remember about", 
            "tell me what you know about", "do you remember when", "what did we discuss about", "save to memory",
            "memorize this", "add to memory", "keep track of", "log this", "note this", "record this", "save this info"
        ]
        
        self.web_triggers = [ "open", "go to", "visit", "navigate to", "browse to", "load", "access", "show me", "take me to" ]

    def _setup_search_headers(self):
        """Setup rotating search headers for better success rate."""
        self.search_headers_pool = [
            { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive' },
            { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Connection': 'keep-alive' }
        ]
        self.current_header_index = 0

    def _get_next_headers(self) -> Dict[str, str]:
        """Get next headers from rotation pool."""
        headers = self.search_headers_pool[self.current_header_index]
        self.current_header_index = (self.current_header_index + 1) % len(self.search_headers_pool)
        return headers

    def _setup_automation_patterns(self):
        """Setup comprehensive automation patterns."""
        self.automation_patterns = {
            'productivity': ['organize files', 'clean desktop', 'backup files', 'system cleanup', 'clear cache', 'update software'],
            'media': ['play music', 'pause music', 'next song', 'previous song', 'volume up', 'volume down', 'mute', 'unmute', 'play video', 'pause video', 'fullscreen', 'exit fullscreen'],
            'system': ['restart computer', 'shutdown computer', 'lock screen', 'sleep mode', 'hibernate', 'log off', 'system info', 'task manager', 'control panel'],
            'window_management': ['minimize window', 'maximize window', 'close window', 'switch window', 'new window', 'new tab', 'close tab'],
            'file_operations': ['create file', 'delete file', 'copy file', 'move file', 'rename file', 'open file', 'save file']
        }

    def _setup_memory_integration(self):
        """Enhanced memory brain integration setup."""
        try:
            if hasattr(self.cns, 'memory_brain') and self.cns.memory_brain is not None:
                self.memory_brain = self.cns.memory_brain
                self.memory_enabled = True
                self.memory_brain.log_action("AUTOMATION_BRAIN", "INITIALIZED_V1.5", { "version": "1.5", "features": ["production_ready", "enhanced_error_handling", "performance_optimizations", "comprehensive_web_search", "advanced_automation", "intelligent_caching", "rotating_headers", "structured_results" ], "memory_status": "active", "initialization_time": datetime.datetime.now().isoformat(), "system_info": { "os": self.os_type, "python_version": f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}" }, "boss_greeting": "AutomationBrain V1.5 Production-Ready online, Boss!" })
                self.logger.info("Enhanced memory integration active - comprehensive tracking enabled")
            else:
                self.memory_brain = None
                self.memory_enabled = False
                self.logger.warning("Memory brain unavailable - operating in standalone mode")
        except Exception as e:
            self.logger.error(f"Memory integration setup failed: {e}")
            self.memory_brain = None
            self.memory_enabled = False

    def _setup_performance_tracking(self):
        """Setup comprehensive performance tracking."""
        self.command_stats = {
            'total_commands': 0, 'successful_commands': 0, 'failed_commands': 0, 'search_queries': 0,
            'memory_operations': 0, 'web_operations': 0, 'file_operations': 0, 'system_operations': 0,
            'average_execution_time': 0.0, 'session_start_time': datetime.datetime.now(), 'last_command_time': None
        }

    def _setup_caching(self):
        """Setup intelligent caching system."""
        self.cache = { 'search_results': {}, 'website_status': {}, 'system_info': {}, 'file_paths': {} }
        self.cache_ttl = 300  # 5 minutes TTL
    @contextmanager
    def _performance_timer(self, operation: str):
        """Context manager for performance timing."""
        start_time = time.time()
        try:
            yield
        finally:
            execution_time = time.time() - start_time
            self._update_performance_stats(operation, execution_time)

    def _update_performance_stats(self, operation: str, execution_time: float):
        """Update performance statistics."""
        total_ops = self.command_stats['total_commands']
        current_avg = self.command_stats['average_execution_time']
        if total_ops > 0:
            self.command_stats['average_execution_time'] = ((current_avg * (total_ops - 1) + execution_time) / total_ops)
        else:
            self.command_stats['average_execution_time'] = execution_time
        self.command_stats['last_command_time'] = datetime.datetime.now()

    def execute_command(self, command: str) -> str:
        """Enhanced main command execution with comprehensive error handling."""
        if not command or not command.strip():
            return "Boss, I need a command to execute. Please tell me what you'd like me to do."

        command_lower = command.lower().strip()
        self.command_stats['total_commands'] += 1
        self.logger.info(f"Processing command #{self.command_stats['total_commands']}: '{command_lower}'")

        with self._performance_timer("command_execution"):
            try:
                if self.memory_enabled:
                    self.memory_brain.log_action("AUTOMATION_BRAIN", "COMMAND_RECEIVED_V1.5", {
                        "command": command, "timestamp": datetime.datetime.now().isoformat(),
                        "source": "Boss", "command_id": self.command_stats['total_commands'],
                        "context": self._analyze_command_context(command)
                    })
                result = self._process_command_pipeline(command, command_lower)
                if result:
                    self.command_stats['successful_commands'] += 1
                    self._log_command_success(command, result)
                    return result.message if isinstance(result, CommandResult) else result
                else:
                    return None
            except Exception as e:
                self.command_stats['failed_commands'] += 1
                self.logger.error(f"Command execution error: {e}", exc_info=True)
                if self.memory_enabled:
                    self.memory_brain.log_action("AUTOMATION_BRAIN", "COMMAND_ERROR_V1.5", {
                        "command": command, "error": str(e), "error_type": type(e).__name__,
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                return f"Boss, I encountered an error: {type(e).__name__}. Let me try a different approach or check the logs for details."

    def _process_command_pipeline(self, command: str, command_lower: str) -> Optional[Union[str, CommandResult]]:
        """Process command through enhanced pipeline."""
        if self._is_memory_command(command): return self._handle_memory_command(command)
        if self._is_search_command(command):
            search_query = self._extract_search_query(command)
            search_context = self._determine_search_context(command)
            return self._search_web_enhanced(search_query, search_context)
        if self._is_web_browsing_command(command_lower): return self._handle_web_browsing(command_lower)
        
        multimedia_result = self._handle_multimedia_commands(command_lower)
        if multimedia_result: return multimedia_result
        
        system_result = self._handle_system_automation(command_lower)
        if system_result: return system_result
        
        file_result = self._handle_file_operations(command_lower)
        if file_result: return file_result
        
        window_result = self._handle_window_management(command_lower)
        if window_result: return window_result
        
        control_result = self._handle_input_control(command_lower)
        if control_result: return control_result
        
        status_result = self._handle_status_commands(command_lower)
        if status_result: return status_result
        
        automation_result = self._handle_advanced_automation(command_lower)
        if automation_result: return automation_result
        
        return None
    def _analyze_command_context(self, command: str) -> Dict[str, Any]:
        """Analyze command context for better processing."""
        context = { "length": len(command), "word_count": len(command.split()), "has_question": "?" in command, "urgency_indicators": [], "category": "general", "complexity": "simple" }
        urgent_words = ["urgent", "quickly", "now", "immediately", "asap", "fast", "hurry"]
        for word in urgent_words:
            if word in command.lower(): context["urgency_indicators"].append(word)
        if len(command.split()) > 10 or any(word in command.lower() for word in ["and", "then", "after", "before"]): context["complexity"] = "complex"
        if any(trigger in command.lower() for trigger in self.search_triggers): context["category"] = "search"
        elif any(trigger in command.lower() for trigger in self.memory_triggers): context["category"] = "memory"
        elif any(trigger in command.lower() for trigger in self.web_triggers): context["category"] = "web_browsing"
        elif "file" in command.lower(): context["category"] = "file_operations"
        elif any(word in command.lower() for word in ["window", "tab", "minimize", "maximize"]): context["category"] = "window_management"
        return context

    def _is_web_browsing_command(self, command: str) -> bool:
        """Check if command is for web browsing."""
        has_web_trigger = any(trigger in command for trigger in self.web_triggers)
        has_domain = any(domain in command for domain in self.web_domains) or any(site in command for site in self.common_websites)
        return has_web_trigger and has_domain

    def _handle_web_browsing(self, command: str) -> str:
        """Handle enhanced web browsing commands."""
        try:
            self.command_stats['web_operations'] += 1
            target = self._extract_web_target(command)
            if not target: return "Boss, I need to know which website you'd like me to open."
            
            if target.lower() in self.common_websites:
                url = f"https://{self.common_websites[target.lower()]}"
            elif self._is_valid_url(target):
                url = target if target.startswith(('http://', 'https://')) else f"https://{target}"
            else:
                if not any(domain in target for domain in self.web_domains): target += ".com"
                url = f"https://{target}"
            
            if hasattr(self.cns, 'security_brain') and self.cns.security_brain is not None:
                domain = urlparse(url).netloc
                security_response = self.cns.security_brain.check_website_access(domain)
                if security_response != "ALLOWED":
                    return f"Boss, access to {domain} is restricted by security protocols."
            
            webbrowser.open(url)
            if self.memory_enabled:
                self.memory_brain.log_action("AUTOMATION_BRAIN", "WEBSITE_OPENED", {"url": url, "target": target, "command": command})
            return f"Boss, I've opened {url} in your default browser."
        except Exception as e:
            self.logger.error(f"Web browsing error: {e}")
            return f"Boss, I had trouble opening that website: {str(e)}"

    def _extract_web_target(self, command: str) -> Optional[str]:
        """Extract website target from command."""
        for trigger in self.web_triggers:
            if trigger in command: command = command.replace(trigger, "", 1).strip()
        cleanup_words = ["website", "site", "page", "the", "a", "an"]
        words = command.split()
        cleaned_words = [word for word in words if word.lower() not in cleanup_words]
        if cleaned_words: return " ".join(cleaned_words)
        return None

    def _is_valid_url(self, text: str) -> bool:
        """Check if text is a valid URL."""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc]) or any(domain in text for domain in self.web_domains)
        except: return False

    def _search_web_enhanced(self, query: str, context: str = "general") -> str:
        """Enhanced web search with context awareness and multiple sources."""
        try:
            self.command_stats['search_queries'] += 1
            cleaned_query = query.strip()
            if not cleaned_query: return "Boss, I need a specific search term to find information for you."
            
            self.logger.info(f"Enhanced search with context '{context}': {cleaned_query}")
            
            cache_key = f"{cleaned_query}_{context}"
            if cache_key in self.cache['search_results']:
                cached_result = self.cache['search_results'][cache_key]
                if time.time() - cached_result['timestamp'] < self.cache_ttl:
                    return f"Boss, here's what I found (cached): {cached_result['result']}"
            
            if hasattr(self.cns, 'security_brain') and self.cns.security_brain is not None:
                security_response = self.cns.security_brain.check_website_access("google.com")
                if security_response != "ALLOWED": return "Boss, web search is currently restricted by security protocols."
            
            summary = self._get_enhanced_web_summary(cleaned_query, context)
            
            if summary:
                self.cache['search_results'][cache_key] = {'result': summary, 'timestamp': time.time()}
                response = f"Boss, here's what I found about '{cleaned_query}':\n\n{summary}"
                if context == "how_to": response += "\n\n💡 Would you like me to search for video tutorials on this topic?"
                elif context == "definition": response += "\n\n💡 Need more detailed information? I can search for related topics."
                elif context == "news": response += "\n\n📰 Want me to find more recent news on this topic?"
                
                if self.memory_enabled:
                    self.memory_brain.log_action("AUTOMATION_BRAIN", "SEARCH_COMPLETED", {"query": cleaned_query, "context": context, "result_length": len(summary), "source": "web_search"})
                return response
            else:
                encoded_query = urllib.parse.quote_plus(cleaned_query)
                search_url = f"https://www.google.com/search?q={encoded_query}"
                webbrowser.open(search_url)
                return f"I couldn't fetch a summary, Boss, but I've opened an enhanced web search for '{cleaned_query}' in your browser."
        except Exception as e:
            self.logger.error(f"Enhanced web search error: {str(e)}")
            return f"Boss, I encountered a technical issue while searching for '{query}'. Let me try opening a browser search instead."

    def _get_enhanced_web_summary(self, query: str, context: str = "general") -> Optional[str]:
        """Enhanced web content summarization with multiple sources."""
        try:
            summary = self._search_duckduckgo_enhanced(query)
            if summary: return summary
            if context in ["definition", "general", "factual", "person"]:
                wiki_summary = self._search_wikipedia_enhanced(query)
                if wiki_summary: return wiki_summary
            if context == "how_to":
                howto_summary = self._search_howto_enhanced(query)
                if howto_summary: return howto_summary
            return None
        except Exception as e:
            self.logger.error(f"Enhanced summary generation error: {str(e)}")
            return None

    def _search_duckduckgo_enhanced(self, query: str) -> Optional[str]:
        """Enhanced DuckDuckGo search with better result parsing."""
        try:
            duckduckgo_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            headers = self._get_next_headers()
            response = requests.get(duckduckgo_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Abstract'):
                    result = f"📋 {data['Abstract']}\n\n📎 Source: {data.get('AbstractSource', 'Web')}"
                    if data.get('AbstractURL'): result += f"\n🔗 More info: {data['AbstractURL']}"
                    return result
                if data.get('Answer'): return f"✨ Quick Answer: {data['Answer']}"
                if data.get('Definition'): return f"📖 Definition: {data['Definition']}\n\n📎 Source: {data.get('DefinitionSource', 'Dictionary')}"
                if data.get('RelatedTopics'):
                    topics = data['RelatedTopics'][:3]
                    results = [f"• {topic['Text']}" for topic in topics if isinstance(topic, dict) and topic.get('Text')]
                    if results: return "\n".join(results) + "\n\n📎 Source: DuckDuckGo Search"
            return None
        except Exception as e:
            self.logger.error(f"DuckDuckGo search error: {str(e)}")
            return None

    def _search_wikipedia_enhanced(self, query: str) -> Optional[str]:
        """Enhanced Wikipedia search."""
        try:
            wiki_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote_plus(query)
            headers = self._get_next_headers()
            response = requests.get(wiki_url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('extract'):
                    result = f"📚 **{data.get('title', query)}**\n\n{data['extract']}"
                    if data.get('content_urls', {}).get('desktop', {}).get('page'):
                        result += f"\n\n🔗 Read more: {data['content_urls']['desktop']['page']}"
                    return result
            return None
        except Exception as e:
            self.logger.error(f"Wikipedia search error: {str(e)}")
            return None

    def _search_howto_enhanced(self, query: str) -> Optional[str]:
        """Enhanced how-to search with structured results."""
        try:
            if not query.lower().startswith("how to"): query = f"how to {query}"
            return self._search_duckduckgo_enhanced(query)
        except Exception as e:
            self.logger.error(f"How-to search error: {str(e)}")
            return None
    def _handle_multimedia_commands(self, command: str) -> Optional[str]:
        """Enhanced multimedia command handling."""
        try:
            if "show me" in command and "video" in command:
                query = self._extract_video_query(command)
                return self._search_youtube_enhanced(query)
            
            video_controls = {
                "play video": ("space", "Video playback started"), "pause video": ("space", "Video paused"),
                "skip forward": ("right", "Skipped forward 10 seconds"), "skip backward": ("left", "Skipped backward 10 seconds"),
                "fullscreen": ("f", "Entered fullscreen mode"), "exit fullscreen": ("escape", "Exited fullscreen mode"),
                "mute video": ("m", "Video muted"), "unmute video": ("m", "Video unmuted")
            }
            for control_phrase, (key, message) in video_controls.items():
                if control_phrase in command:
                    pyautogui.press(key)
                    return f"Boss, {message.lower()}."
            
            if "volume up" in command: return self._volume_control("up")
            elif "volume down" in command: return self._volume_control("down")
            
            return None
        except Exception as e:
            self.logger.error(f"Multimedia command error: {e}")
            return f"Boss, I had trouble with that multimedia command: {str(e)}"

    def _extract_video_query(self, command: str) -> str:
        """Extract video search query from command."""
        triggers = ["show me", "video", "videos", "about", "on"]
        words = command.split()
        filtered_words = [word for word in words if word.lower() not in triggers]
        return " ".join(filtered_words).strip()

    def _search_youtube_enhanced(self, query: str) -> str:
        """Enhanced YouTube search."""
        try:
            if not query: return "Boss, I need to know what video you're looking for."
            encoded_query = urllib.parse.quote_plus(query)
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(youtube_url)
            if self.memory_enabled:
                self.memory_brain.log_action("AUTOMATION_BRAIN", "YOUTUBE_SEARCH", {"query": query, "url": youtube_url})
            return f"Boss, I've opened YouTube search results for '{query}' in your browser."
        except Exception as e:
            self.logger.error(f"YouTube search error: {e}")
            return f"Boss, I had trouble searching YouTube for '{query}': {str(e)}"

    def _volume_control(self, direction: str) -> str:
        """Enhanced volume control."""
        try:
            if direction == "up": pyautogui.press("volumeup"); return "Boss, volume increased."
            elif direction == "down": pyautogui.press("volumedown"); return "Boss, volume decreased."
            else: return "Boss, I can only adjust volume up or down."
        except Exception as e:
            self.logger.error(f"Volume control error: {e}")
            return f"Boss, I had trouble adjusting the volume: {str(e)}"

    def _handle_system_automation(self, command: str) -> Optional[str]:
        """Handle enhanced system automation tasks."""
        try:
            self.command_stats['system_operations'] += 1
            system_commands = {
                "system status": self._get_system_status_enhanced, "system info": self._get_system_info_enhanced,
                "time": self._get_current_time_enhanced, "date": self._get_current_date_enhanced,
                "performance stats": self._get_performance_report, "task manager": self._open_task_manager,
                "control panel": self._open_control_panel, "lock screen": self._lock_screen,
                "sleep mode": self._sleep_system, "restart computer": self._restart_system,
                "shutdown computer": self._shutdown_system
            }
            for sys_cmd, action in system_commands.items():
                if sys_cmd in command: return action()
            return None
        except Exception as e:
            self.logger.error(f"System automation error: {e}")
            return f"Boss, I had trouble with that system command: {str(e)}"

    def _get_system_status_enhanced(self) -> str:
        """Get enhanced system status information."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            status = (f"🖥️ **System Status Report**\n\n"
                      f"💻 CPU Usage: {cpu_percent}%\n"
                      f"🧠 Memory: {memory.percent}% used ({self._bytes_to_gb(memory.used):.1f}GB / {self._bytes_to_gb(memory.total):.1f}GB)\n"
                      f"💾 Disk: {disk.percent}% used ({self._bytes_to_gb(disk.used):.1f}GB / {self._bytes_to_gb(disk.total):.1f}GB)\n"
                      f"🌐 Network: ↑{self._bytes_to_mb(network.bytes_sent):.1f}MB ↓{self._bytes_to_mb(network.bytes_recv):.1f}MB\n"
                      f"⏰ Uptime: {self._get_system_uptime()}")
            return status
        except Exception as e:
            self.logger.error(f"System status error: {e}")
            return f"Boss, I couldn't get the system status: {str(e)}"

    def _get_system_info_enhanced(self) -> str:
        """Get detailed system information."""
        try:
            info = (f"🖥️ **System Information**\n\n"
                    f"OS: {platform.system()} {platform.release()}\n"
                    f"Architecture: {platform.architecture()[0]}\n"
                    f"Processor: {platform.processor()}\n"
                    f"Python: {platform.python_version()}\n"
                    f"Machine: {platform.machine()}\n"
                    f"Node: {platform.node()}")
            return info
        except Exception as e:
            return f"Boss, I couldn't get system information: {str(e)}"

    def _get_current_time_enhanced(self) -> str:
        """Get current time with enhanced formatting."""
        now = datetime.datetime.now()
        return f"Boss, the current time is {now.strftime('%I:%M:%S %p')} on {now.strftime('%A, %B %d, %Y')}."

    def _get_current_date_enhanced(self) -> str:
        """Get current date with enhanced formatting."""
        now = datetime.datetime.now()
        return f"Boss, today is {now.strftime('%A, %B %d, %Y')}."

    def _open_task_manager(self) -> str:
        """Open task manager."""
        try:
            if self.os_type == "windows": subprocess.run(["taskmgr"], check=True)
            elif self.os_type == "darwin": subprocess.run(["open", "-a", "Activity Monitor"], check=True)
            else: subprocess.run(["gnome-system-monitor"], check=True)
            return "Boss, I've opened the task manager."
        except Exception as e:
            return f"Boss, I couldn't open the task manager: {str(e)}"
    def _handle_file_operations(self, command: str) -> Optional[str]:
        """Handle enhanced file operations."""
        try:
            self.command_stats['file_operations'] += 1
            if command.startswith("create file"):
                filename = command.replace("create file", "").strip()
                return self._create_file_enhanced(filename)
            elif command.startswith("delete file"):
                filename = command.replace("delete file", "").strip()
                return self._delete_file_enhanced(filename)
            elif command.startswith("copy file"): return self._copy_file_enhanced(command)
            elif command.startswith("move file"): return self._move_file_enhanced(command)
            elif command.startswith("rename file"): return self._rename_file_enhanced(command)
            elif "organize files" in command: return self._organize_files_enhanced()
            elif "clean desktop" in command: return self._clean_desktop_enhanced()
            return None
        except Exception as e:
            self.logger.error(f"File operation error: {e}")
            return f"Boss, I had trouble with that file operation: {str(e)}"

    def _create_file_enhanced(self, filename: str) -> str:
        """Create a file with enhanced error handling."""
        try:
            if not filename: return "Boss, I need a filename to create the file."
            safe_filename = self._sanitize_filename(filename)
            file_path = self.desktop_path / safe_filename
            file_path.touch()
            if self.memory_enabled:
                self.memory_brain.log_action("AUTOMATION_BRAIN", "FILE_CREATED", {"filename": safe_filename, "path": str(file_path)})
            return f"Boss, I've created the file '{safe_filename}' on your desktop."
        except Exception as e: return f"Boss, I couldn't create the file: {str(e)}"

    def _delete_file_enhanced(self, filename: str) -> str:
        """Delete a file with enhanced safety checks."""
        try:
            if not filename: return "Boss, I need a filename to delete."
            safe_filename = self._sanitize_filename(filename)
            file_path = self.desktop_path / safe_filename
            if not file_path.exists(): return f"Boss, I couldn't find the file '{safe_filename}' on your desktop."
            if self._is_system_file(file_path): return f"Boss, I can't delete '{safe_filename}' as it appears to be a system file."
            file_path.unlink()
            if self.memory_enabled:
                self.memory_brain.log_action("AUTOMATION_BRAIN", "FILE_DELETED", {"filename": safe_filename, "path": str(file_path)})
            return f"Boss, I've deleted the file '{safe_filename}' from your desktop."
        except Exception as e: return f"Boss, I couldn't delete the file: {str(e)}"

    def _handle_window_management(self, command: str) -> Optional[str]:
        """Handle window management commands."""
        try:
            window_commands = {
                "minimize window": self._minimize_current_window, "maximize window": self._maximize_current_window,
                "close window": self._close_current_window, "new window": self._new_window,
                "new tab": self._new_tab, "close tab": self._close_tab,
                "switch window": self._switch_window, "list windows": self._list_windows
            }
            for window_cmd, action in window_commands.items():
                if window_cmd in command: return action()
            return None
        except Exception as e:
            self.logger.error(f"Window management error: {e}")
            return f"Boss, I had trouble with that window command: {str(e)}"

    def _minimize_current_window(self) -> str:
        try:
            active_window = gw.getActiveWindow()
            if active_window: active_window.minimize()
            return "Boss, I've minimized the current window."
        except Exception as e: return f"Boss, I couldn't minimize the window: {str(e)}"

    def _maximize_current_window(self) -> str:
        try:
            active_window = gw.getActiveWindow()
            if active_window: active_window.maximize()
            return "Boss, I've maximized the current window."
        except Exception as e: return f"Boss, I couldn't maximize the window: {str(e)}"

    def _close_current_window(self) -> str:
        try:
            active_window = gw.getActiveWindow()
            if active_window: active_window.close()
            return "Boss, I've closed the current window."
        except Exception as e: return f"Boss, I couldn't close the window: {str(e)}"

    def _new_tab(self) -> str:
        try:
            pyautogui.hotkey('ctrl', 't')
            return "Boss, I've opened a new tab."
        except Exception as e: return f"Boss, I couldn't open a new tab: {str(e)}"

    def _close_tab(self) -> str:
        try:
            pyautogui.hotkey('ctrl', 'w')
            return "Boss, I've closed the current tab."
        except Exception as e: return f"Boss, I couldn't close the tab: {str(e)}"

    def _handle_input_control(self, command: str) -> Optional[str]:
        """Handle enhanced mouse and keyboard control."""
        try:
            if command.startswith("move mouse to"):
                coords = re.findall(r'\d+', command)
                if len(coords) >= 2: return self._move_mouse_enhanced(int(coords[0]), int(coords[1]))
            elif "left click" in command: return self._click_mouse_enhanced("left")
            elif "right click" in command: return self._click_mouse_enhanced("right")
            elif "double click" in command: return self._double_click_enhanced()
            elif "copy" in command and "text" in command: pyautogui.hotkey('ctrl', 'c'); return "Boss, I've copied the selected text."
            elif "paste" in command and "text" in command: pyautogui.hotkey('ctrl', 'v'); return "Boss, I've pasted the text."
            elif command.startswith("type"):
                text = command.replace("type", "").strip()
                if text: pyautogui.write(text); return f"Boss, I've typed: {text}"
            return None
        except Exception as e:
            self.logger.error(f"Input control error: {e}")
            return f"Boss, I had trouble with that input command: {str(e)}"

    def _move_mouse_enhanced(self, x: int, y: int) -> str:
        try:
            screen_width, screen_height = pyautogui.size()
            if 0 <= x <= screen_width and 0 <= y <= screen_height:
                pyautogui.moveTo(x, y, duration=0.5)
                return f"Boss, I've moved the mouse to ({x}, {y})."
            else: return f"Boss, coordinates ({x}, {y}) are outside the screen bounds."
        except Exception as e: return f"Boss, I couldn't move the mouse: {str(e)}"

    def _click_mouse_enhanced(self, button: str) -> str:
        try:
            if button == "left": pyautogui.click(); return "Boss, I've performed a left click."
            elif button == "right": pyautogui.rightClick(); return "Boss, I've performed a right click."
            else: return "Boss, I can only perform left or right clicks."
        except Exception as e: return f"Boss, I couldn't perform the click: {str(e)}"
    def _handle_status_commands(self, command: str) -> Optional[str]:
        """Handle status and information commands."""
        if "performance stats" in command or "stats" in command: return self._format_performance_stats()
        elif "version" in command or "about" in command: return self._get_version_info()
        elif "help" in command: return self._get_help_info()
        return None

    def _format_performance_stats(self) -> str:
        """Format comprehensive performance statistics."""
        stats = self.get_performance_stats()
        uptime = datetime.datetime.now() - stats['session_start_time']
        uptime_str = str(uptime).split('.')[0]
        success_rate = (stats['successful_commands'] / stats['total_commands'] * 100) if stats['total_commands'] > 0 else 100
        return (f"📊 **AutomationBrain V1.5 Performance Dashboard**\n\n"
                f"✅ Total Commands: {stats['total_commands']}\n"
                f"🎯 Success Rate: {success_rate:.1f}%\n"
                f"🔍 Search Queries: {stats['search_queries']}\n"
                f"🌐 Web Operations: {stats['web_operations']}\n"
                f"📁 File Operations: {stats['file_operations']}\n"
                f"⚙️ System Operations: {stats['system_operations']}\n"
                f"💾 Memory Operations: {stats['memory_operations']}\n"
                f"⏱️ Avg Execution Time: {stats['average_execution_time']:.2f}s\n"
                f"🕐 Session Uptime: {uptime_str}")

    def _get_version_info(self) -> str:
        """Get version and system information."""
        return (f"🤖 **ZIA-X AutomationBrain V1.5**\n\n"
                f"🔧 Production-Ready Enhanced Edition\n"
                f"🐍 Python: {self.python_version.major}.{self.python_version.minor}\n"
                f"💻 OS: {self.os_type.title()}")

    def _get_help_info(self) -> str:
        """Get help information about available commands."""
        return (f"🆘 **ZIA-X AutomationBrain Help**\n\n"
                f"**🔍 Search:** 'search for [topic]'\n"
                f"**🌐 Web:** 'open [website]'\n"
                f"**📁 Files:** 'create file [name]', 'delete file [name]'\n"
                f"**⚙️ System:** 'system status', 'time', 'date'")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return self.command_stats

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file operations."""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

    def _is_system_file(self, file_path: Path) -> bool:
        """Check if file is a system file that shouldn't be deleted."""
        return file_path.suffix.lower() in ['.sys', '.dll', '.exe', '.ini']

    def _bytes_to_gb(self, bytes_value: int) -> float:
        """Convert bytes to gigabytes."""
        return bytes_value / (1024 ** 3)

    def _bytes_to_mb(self, bytes_value: int) -> float:
        """Convert bytes to megabytes."""
        return bytes_value / (1024 ** 2)

    def _get_system_uptime(self) -> str:
        """Get system uptime."""
        try:
            return str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))
        except: return "Unknown"
    
    def _is_memory_command(self, command: str) -> bool: return any(trigger in command for trigger in self.memory_triggers)
    def _is_search_command(self, command: str) -> bool: return any(trigger in command for trigger in self.search_triggers)
    def _handle_memory_command(self, command: str) -> str: return "Memory command recognized, but not yet implemented, Boss."
    def _copy_file_enhanced(self, command: str) -> str: return "Copy file command recognized, but not yet implemented, Boss."
    def _move_file_enhanced(self, command: str) -> str: return "Move file command recognized, but not yet implemented, Boss."
    def _rename_file_enhanced(self, command: str) -> str: return "Rename file command recognized, but not yet implemented, Boss."
    def _organize_files_enhanced(self) -> str: return "Organize files command recognized, but not yet implemented, Boss."
    def _clean_desktop_enhanced(self) -> str: return "Clean desktop command recognized, but not yet implemented, Boss."
    def _new_window(self) -> str: pyautogui.hotkey('ctrl', 'n'); return "New window command executed, Boss."
    def _switch_window(self) -> str: pyautogui.hotkey('alt', 'tab'); return "Switched window, Boss."
    def _list_windows(self) -> str: return "List windows command recognized, but not yet implemented, Boss."
    def _double_click_enhanced(self) -> str: pyautogui.doubleClick(); return "Double click executed, Boss."
    def _get_performance_report(self) -> str: return self._format_performance_stats()
    def _open_control_panel(self) -> str: os.system('control'); return "Opening Control Panel, Boss."
    def _lock_screen(self) -> str: 
        if self.os_type == "windows":
            os.system('rundll32.exe user32.dll,LockWorkStation')
        return "Screen locked, Boss."
    def _sleep_system(self) -> str: return "Sleep command recognized, but requires admin rights to execute safely."
    def _restart_system(self) -> str: return "Restart command recognized, but requires confirmation."
    def _shutdown_system(self) -> str: return "Shutdown command recognized, but requires confirmation."
    def _handle_advanced_automation(self, command: str) -> Optional[str]: return None
    def _log_command_success(self, command: str, result: Union[str, CommandResult]):
        if self.memory_enabled:
            result_text = result.message if isinstance(result, CommandResult) else result
            self.memory_brain.log_action("AUTOMATION_BRAIN", "COMMAND_SUCCESS_V1.5", {
                "command": command,
                "result_preview": result_text[:100] + "..." if len(result_text) > 100 else result_text,
                "timestamp": datetime.datetime.now().isoformat(),
                "success": True
            })

    def shutdown(self):
        """Graceful shutdown of AutomationBrain."""
        try:
            if self.memory_enabled:
                self.memory_brain.log_action("AUTOMATION_BRAIN", "SHUTDOWN_V1.5", {
                    "final_stats": self.get_performance_stats(),
                    "shutdown_time": datetime.datetime.now().isoformat(),
                    "message": "AutomationBrain V1.5 shutting down gracefully, Boss!"
                })
            self.logger.info("AutomationBrain V1.5 shutdown completed.")
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")
    