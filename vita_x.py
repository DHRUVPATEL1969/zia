#!/usr/bin/env python3
"""
ZIA-X Central Nervous System (CNS) - Enhanced Edition
====================================================

This is the master CNS with enhanced brain integration, improved error handling,
and advanced coordination between all brain modules.

Author: ZIA-X Development Team
Version: 1.0.0 - Production Ready Enhanced
Python: 3.10+
"""

import re
import threading
import logging
import json
import time
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from urllib.parse import urlparse

# Import enhanced brain modules
from brains.automation_brain import AutomationBrain, CommandResult as AutomationCommandResult
from brains.response_brain import ResponseBrain
from brains.security_brain import SecurityBrain
from brains.decision_brain import DecisionBrain, DecisionResult
from brains.memory_brain import MemoryBrain

@dataclass
class CommandResult:
    """Structured result for command processing."""
    success: bool
    response: str
    source_brain: str
    execution_time: float = 0.0
    requires_clarification: bool = False
    clarification_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class VitaCNS:
    """
    Enhanced Central Nervous System for ZIA-X AI with advanced brain coordination.
    """

    def __init__(self):
        print("🧠 ZIA-X Enhanced CNS initializing...")

        # Core components
        self._threads = []
        self._shutdown_event = threading.Event()
        self.pending_security_question = None
        self.pending_clarification = None
        self.pending_decision_clarification = None
        self.last_command = None
        
        # Performance tracking
        self.session_stats = {
            'commands_processed': 0,
            'successful_commands': 0,
            'failed_commands': 0,
            'clarifications_requested': 0,
            'security_checks': 0,
            'session_start': datetime.datetime.now(),
            'brain_usage': {
                'decision_brain': 0,
                'automation_brain': 0,
                'response_brain': 0,
                'security_brain': 0,
                'memory_brain': 0
            }
        }

        # Setup logging & config
        self._setup_enhanced_logging()
        logging.info("ZIA-X Enhanced Central Nervous System starting up...")
        self.config = self._load_configuration()

        # Initialize brain module attributes
        self.automation_brain = None
        self.response_brain = None
        self.security_brain = None
        self.decision_brain = None
        self.memory_brain = None

        # Enhanced initialization
        self._initialize_enhanced_brains()
        self._setup_brain_communication()
        
        logging.info("ZIA-X Enhanced CNS initialization complete.")
        print("✅ All enhanced brain modules loaded and connected!")

    def _setup_enhanced_logging(self):
        """Setup enhanced logging with better formatting and rotation."""
        log_dir = Path("📝 logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"zia_x_enhanced_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Enhanced logging initialized - Log file: {log_file}")

    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration with enhanced error handling and defaults."""
        config_file = Path("⚙️ config") / "settings.json"
        
        default_config = {
            "response_brain": {"enabled": True},
            "security_brain": {"enabled": True},
            "automation_brain": {"enabled": True},
            "decision_brain": { "enabled": True, "confidence_threshold": 0.7, "max_alternatives": 3, "learning_enabled": True, "context_window": 5 },
            "memory_brain": {"enabled": True},
            "cns": { "max_retries": 3, "command_timeout": 30, "enable_performance_tracking": True }
        }
        
        try:
            if config_file.exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    for key, value in default_config.items():
                        if key not in loaded_config: loaded_config[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in loaded_config[key]: loaded_config[key][subkey] = subvalue
                    return loaded_config
            else:
                self.logger.warning(f"Config file not found, creating default: {config_file}")
                config_file.parent.mkdir(exist_ok=True)
                with open(config_file, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2)
                return default_config
                
        except Exception as e:
            self.logger.error(f"Error loading config, using defaults: {e}")
            return default_config

    def _initialize_enhanced_brains(self):
        """Initialize all brain modules with enhanced error handling."""
        logging.info("Initializing enhanced brain modules...")
        
        self._load_memory_brain()
        self._load_security_brain()
        self._load_decision_brain()
        self._load_automation_brain()
        self._load_response_brain()
        
        logging.info("All enhanced brain modules initialized successfully.")

    def _load_memory_brain(self):
        """Initialize the enhanced MemoryBrain."""
        if self.config.get("memory_brain", {}).get("enabled", True):
            try:
                self.memory_brain = MemoryBrain(cns=self, config=self.config)
                logging.info("💾 Enhanced Memory Brain (Black Box) module loaded.")
                if self.memory_brain:
                    self.memory_brain.log_action("CNS", "ENHANCED_INITIALIZATION", { "version": "1.0.0", "timestamp": datetime.datetime.now().isoformat(), "features": ["enhanced_brain_coordination", "performance_tracking", "advanced_error_handling"], "message": "Enhanced CNS initialized successfully, Boss!" })
            except Exception as e:
                logging.error(f"Failed to load Enhanced Memory Brain: {e}", exc_info=True)
                self.memory_brain = None

    def _load_security_brain(self):
        """Initialize the SecurityBrain."""
        security_config = self.config.get("security_brain", {})
        if security_config.get("enabled", False):
            try:
                self.security_brain = SecurityBrain(cns=self, config=security_config)
                logging.info("🛡️ Security Brain module loaded.")
            except Exception as e:
                logging.error(f"Failed to load Security Brain: {e}", exc_info=True)
                self.security_brain = None

    def _load_decision_brain(self):
        """Initialize the enhanced DecisionBrain V2.0."""
        decision_config = self.config.get("decision_brain", {})
        if decision_config.get("enabled", True):
            try:
                self.decision_brain = DecisionBrain(cns=self, config=decision_config)
                logging.info("🧠 Enhanced Decision Brain V2.0 (Mastermind) module loaded.")
                if self.memory_brain and self.decision_brain:
                    capabilities = self.decision_brain.get_capabilities()
                    self.memory_brain.log_action("CNS", "DECISION_BRAIN_LOADED", { "version": capabilities["version"], "supported_intents": len(capabilities["supported_intents"]), "features": capabilities["features"] })
            except Exception as e:
                logging.error(f"Failed to load Enhanced Decision Brain: {e}", exc_info=True)
                self.decision_brain = None

    def _load_automation_brain(self):
        """Initialize the enhanced AutomationBrain V1.5."""
        if self.config.get("automation_brain", {}).get("enabled", False):
            try:
                self.automation_brain = AutomationBrain(cns=self, config=self.config)
                logging.info("🤖 Enhanced Automation Brain V1.5 module loaded.")
                if self.memory_brain and self.automation_brain:
                    stats = self.automation_brain.get_performance_stats()
                    self.memory_brain.log_action("CNS", "AUTOMATION_BRAIN_LOADED", { "version": "1.5", "memory_status": stats["memory_status"], "features": ["enhanced_web_search", "advanced_automation", "performance_tracking"] })
            except Exception as e:
                logging.error(f"Failed to load Enhanced Automation Brain: {e}", exc_info=True)
                self.automation_brain = None

    def _load_response_brain(self):
        """Initialize the ResponseBrain."""
        if self.config.get("response_brain", {}).get("enabled", False):
            try:
                self.response_brain = ResponseBrain(cns=self, config=self.config)
                logging.info("💬 Response Brain module loaded.")
            except Exception as e:
                logging.error(f"Failed to load Response Brain: {e}", exc_info=True)
                self.response_brain = None

    def _setup_brain_communication(self):
        """Setup enhanced communication channels between brains."""
        try:
            connected_brains = [brain for brain, active in { "MemoryBrain": self.memory_brain, "DecisionBrain V2.0": self.decision_brain, "AutomationBrain V1.5": self.automation_brain, "SecurityBrain": self.security_brain, "ResponseBrain": self.response_brain }.items() if active]
            self.logger.info(f"Brain communication established: {', '.join(connected_brains)}")
            if self.memory_brain:
                self.memory_brain.log_action("CNS", "BRAIN_NETWORK_ESTABLISHED", { "connected_brains": connected_brains, "total_brains": len(connected_brains), "communication_status": "active" })
        except Exception as e:
            self.logger.error(f"Error setting up brain communication: {e}")
    def handle_command(self, command: str, source: str = "text") -> CommandResult:
        """
        Enhanced command handling with improved brain coordination.
        """
        start_time = time.time()
        self.session_stats['commands_processed'] += 1
        self.last_command = command
        
        self.logger.info(f"Enhanced CNS received {source} command: '{command}'")
        print(f">>> You: {command}")

        try:
            if self.pending_security_question:
                result_response = self._handle_security_response(command)
                execution_time = time.time() - start_time
                command_result = CommandResult(success=True, response=result_response, source_brain="SecurityBrain", execution_time=execution_time)
            elif self.pending_decision_clarification:
                command_result = self._handle_decision_clarification(command)
            else:
                command_result = self._process_command_enhanced(command, source)
            
            execution_time = time.time() - start_time
            command_result.execution_time = execution_time
            
            if command_result.success: self.session_stats['successful_commands'] += 1
            else: self.session_stats['failed_commands'] += 1
            if command_result.requires_clarification: self.session_stats['clarifications_requested'] += 1
            
            if self.memory_brain:
                self.memory_brain.log_action("CNS", "COMMAND_PROCESSED_ENHANCED", { 'command': command, 'source': source, 'success': command_result.success, 'source_brain': command_result.source_brain, 'execution_time': execution_time, 'requires_clarification': command_result.requires_clarification })
            
            if command_result.requires_clarification:
                print(f"🤖 ZIA: {command_result.clarification_message}")
            else:
                print(f"🤖 ZIA: {command_result.response}")
            
            self.logger.info(f"Enhanced CNS processed command in {execution_time:.2f}s via {command_result.source_brain}")
            return command_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Error in enhanced command handling: {e}", exc_info=True)
            self.session_stats['failed_commands'] += 1
            error_response = f"Boss, I encountered an unexpected error: {type(e).__name__}. Please try again."
            print(f"🤖 ZIA: {error_response}")
            return CommandResult(success=False, response=error_response, source_brain="CNS_Error_Handler", execution_time=execution_time, metadata={"error": str(e), "error_type": type(e).__name__})

    def _process_command_enhanced(self, command: str, source: str) -> CommandResult:
        """Enhanced command processing with intelligent brain coordination."""
        if self.decision_brain:
            self.session_stats['brain_usage']['decision_brain'] += 1
            try:
                decision_result = self.decision_brain.make_decision(command)
                if isinstance(decision_result, DecisionResult):
                    if decision_result.success and decision_result.automation_command:
                        if self.automation_brain:
                            self.session_stats['brain_usage']['automation_brain'] += 1
                            automation_response = self.automation_brain.execute_command(decision_result.automation_command)
                            if automation_response and automation_response.startswith("ASK_USER:"):
                                return self._handle_security_question(automation_response, command)
                            return CommandResult(success=True, response=automation_response, source_brain="DecisionBrain->AutomationBrain", metadata={"intent": decision_result.intent, "confidence": decision_result.confidence, "action": decision_result.action, "parameters": decision_result.parameters})
                    elif decision_result.clarification_needed:
                        self.pending_decision_clarification = {'original_command': command, 'decision_result': decision_result}
                        return CommandResult(success=False, response="", source_brain="DecisionBrain", requires_clarification=True, clarification_message=decision_result.clarification_message, metadata={"intent": decision_result.intent, "confidence": decision_result.confidence, "alternatives": decision_result.alternatives})
            except Exception as e: self.logger.error(f"Error in DecisionBrain processing: {e}")

        if self.response_brain:
            self.session_stats['brain_usage']['response_brain'] += 1
            try:
                response = self.response_brain.process_command(command)
                if response: return CommandResult(success=True, response=response, source_brain="ResponseBrain")
            except Exception as e: self.logger.error(f"Error in ResponseBrain processing: {e}")

        if self.automation_brain:
            self.session_stats['brain_usage']['automation_brain'] += 1
            try:
                automation_response = self.automation_brain.execute_command(command)
                if automation_response:
                    if automation_response.startswith("ASK_USER:"): return self._handle_security_question(automation_response, command)
                    return CommandResult(success=True, response=automation_response, source_brain="AutomationBrain")
            except Exception as e: self.logger.error(f"Error in AutomationBrain processing: {e}")

        return CommandResult(success=False, response="I'm not sure how to help with that, Boss. Could you try rephrasing your request?", source_brain="CNS_Fallback")
    def _handle_security_question(self, security_response: str, original_command: str) -> CommandResult:
        """Handle security questions from AutomationBrain."""
        url = self._extract_url_from_original_command(original_command)
        self.pending_security_question = { 'question': security_response, 'url': url, 'original_command': original_command }
        self.session_stats['security_checks'] += 1
        clean_question = security_response.replace('ASK_USER:', '').strip()
        return CommandResult(success=False, response="", source_brain="SecurityBrain", requires_clarification=True, clarification_message=clean_question, metadata={"security_check": True, "url": url})

    def _handle_decision_clarification(self, user_response: str) -> CommandResult:
        """Handle clarification responses for DecisionBrain."""
        try:
            clarification_context = self.pending_decision_clarification
            original_command = clarification_context['original_command']
            self.pending_decision_clarification = None
            
            if self.decision_brain and 'decision_result' in clarification_context:
                result = self.decision_brain.handle_clarification_response(original_command, user_response)
                if isinstance(result, DecisionResult) and result.success:
                    if self.automation_brain and result.automation_command:
                        automation_response = self.automation_brain.execute_command(result.automation_command)
                        if automation_response:
                            return CommandResult(success=True, response=automation_response, source_brain="DecisionBrain->AutomationBrain", metadata={"clarification_resolved": True, "intent": result.intent, "action": result.action})
                elif isinstance(result, DecisionResult) and result.clarification_needed:
                    self.pending_decision_clarification = {'original_command': original_command, 'decision_result': result}
                    return CommandResult(success=False, response="", source_brain="DecisionBrain", requires_clarification=True, clarification_message=result.clarification_message)
            
            return self._process_command_enhanced(f"{original_command} {user_response}", "clarification")
        except Exception as e:
            self.logger.error(f"Error handling decision clarification: {e}")
            return CommandResult(success=False, response="I had trouble understanding your clarification, Boss. Let's start over.", source_brain="CNS_Error_Handler")

    def _handle_security_response(self, user_answer: str) -> str:
        """Enhanced security response handling."""
        try:
            answer = user_answer.lower().strip()
            security_context = self.pending_security_question
            url = security_context['url']
            domain = self.security_brain.extract_domain(url) if self.security_brain else urlparse(f'https://{url}').netloc
            
            final_response = "Request cancelled, Boss."

            if answer in ['yes', 'y', 'allow', 'allow permanently', 'permanently']:
                if self.security_brain: self.security_brain.add_to_trusted(domain)
                final_response = f"Understood, Boss. I've added '{domain}' to the VIP list. Opening it now."
                if self.automation_brain: self.automation_brain._open_website(url)
            elif answer in ['no', 'n', 'block', 'deny', 'never']:
                if self.security_brain: self.security_brain.add_to_blocked(domain)
                final_response = f"Got it, Boss. I've added '{domain}' to the blocklist. Access will be denied in the future."
            elif answer in ['this time only', 'once', 'just once', 'temporary', 'temp']:
                if self.security_brain: self.security_brain.add_to_one_time(domain)
                final_response = f"Okay, Boss. Granting one-time access to '{domain}'."
                if self.automation_brain: self.automation_brain._open_website(url)
            else:
                return f"I didn't understand that, Boss. Please answer with 'yes', 'no', or 'this time only'."

            if self.memory_brain:
                self.memory_brain.log_action("CNS", "SECURITY_DECISION", {'url': url, 'domain': domain, 'user_decision': answer, 'action_taken': final_response})

            self.pending_security_question = None
            return final_response
        except Exception as e:
            self.logger.error(f"Error handling security response: {e}")
            self.pending_security_question = None
            return f"Boss, I had trouble processing your security decision: {str(e)}"

    def _extract_url_from_original_command(self, command: str) -> str:
        """Enhanced URL extraction from command."""
        url_patterns = [r'https?://[^\s]+', r'www\.[^\s]+', r'[a-zA-Z0-9-]+\.[a-zA-Z]{2,}[^\s]*']
        for pattern in url_patterns:
            match = re.search(pattern, command)
            if match: return match.group(0)
        words = command.split()
        for word in words:
            if any(ext in word for ext in ['.com', '.org', '.net', '.io', '.in', '.edu', '.gov']): return word
        return command
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        uptime = datetime.datetime.now() - self.session_stats['session_start']
        brain_status = { 'memory_brain': self.memory_brain is not None, 'decision_brain': self.decision_brain is not None, 'automation_brain': self.automation_brain is not None, 'security_brain': self.security_brain is not None, 'response_brain': self.response_brain is not None }
        performance_stats = {}
        if self.decision_brain: performance_stats['decision_brain'] = self.decision_brain.get_performance_stats()
        if self.automation_brain: performance_stats['automation_brain'] = self.automation_brain.get_performance_stats()
        return { 'cns_version': '1.0.0', 'uptime': str(uptime).split('.')[0], 'session_stats': self.session_stats, 'brain_status': brain_status, 'brain_performance': performance_stats, 'active_brains': sum(brain_status.values()), 'total_brains': len(brain_status), 'system_health': 'Excellent' if sum(brain_status.values()) >= 4 else 'Good' if sum(brain_status.values()) >= 2 else 'Limited' }

    def _text_command_loop(self):
        """Enhanced loop to handle typed user commands."""
        time.sleep(1)
        print("\n🎯 Enhanced ZIA-X is ready! Type 'help' for commands or 'status' for system info.")
        
        while not self._shutdown_event.is_set():
            try:
                if self.pending_security_question: prompt = ">>> Your security decision (Yes/No/This time only): "
                elif self.pending_decision_clarification: prompt = ">>> Your choice: "
                else: prompt = ">>> You: "
                command = input(prompt)
                
                if command:
                    if command.lower() in ['exit', 'quit', 'bye', 'goodbye']: print("🤖 ZIA: Goodbye, Boss! It was a pleasure serving you."); break
                    elif command.lower() == 'status': self._display_system_status(); continue
                    elif command.lower() == 'help': self._display_help(); continue
                    elif command.lower() == 'stats': self._display_performance_stats(); continue
                    
                    result = self.handle_command(command, source="text")
                    if not result.success and not result.requires_clarification:
                        print("💡 Tip: Try being more specific or type 'help' for available commands.")
            except (EOFError, KeyboardInterrupt): print("\n🤖 ZIA: Received shutdown signal. Goodbye, Boss!"); break
            except Exception as e:
                self.logger.error(f"Error in command loop: {e}")
                print(f"🤖 ZIA: I encountered an error: {str(e)}. Please try again.")

        self.shutdown()

    def _display_system_status(self):
        """Display comprehensive system status."""
        status = self.get_system_status()
        print("\n📊 ZIA-X Enhanced System Status" + "\n" + "=" * 40)
        print(f"🔧 CNS Version: {status['cns_version']}\n⏰ Uptime: {status['uptime']}\n🏥 System Health: {status['system_health']}\n🧠 Active Brains: {status['active_brains']}/{status['total_brains']}")
        print("\n🧠 Brain Status:")
        for brain, active in status['brain_status'].items(): print(f"  {'✅' if active else '❌'} {brain.replace('_', ' ').title()}")
        print(f"\n📈 Session Statistics:")
        print(f"  📝 Commands Processed: {status['session_stats']['commands_processed']}\n  ✅ Successful: {status['session_stats']['successful_commands']}\n  ❌ Failed: {status['session_stats']['failed_commands']}\n  ❓ Clarifications: {status['session_stats']['clarifications_requested']}\n  🛡️ Security Checks: {status['session_stats']['security_checks']}")
        if status['session_stats']['commands_processed'] > 0:
            success_rate = (status['session_stats']['successful_commands'] / status['session_stats']['commands_processed']) * 100
            print(f"  📊 Success Rate: {success_rate:.1f}%")

    def _display_help(self):
        """Display help information."""
        print("\n🆘 ZIA-X Enhanced Help" + "\n" + "=" * 30)
        print("🔍 Search Commands:\n  • 'search for [topic]'\n  • 'what is [topic]'\n  • 'how to [task]'")
        print("\n🌐 Web Commands:\n  • 'open [website]'\n  • 'go to [url]'")
        print("\n📁 File Commands:\n  • 'create file [name]'\n  • 'open file explorer'")
        print("\n🎵 Media Commands:\n  • 'play music'\n  • 'show me videos about [topic]'")
        print("\n⚙️ System Commands:\n  • 'system status'\n  • 'performance stats'\n  • 'time'\n  • 'date'")
        print("\n🎮 Special Commands:\n  • 'status'\n  • 'stats'\n  • 'help'\n  • 'exit'")

    def _display_performance_stats(self):
        """Display detailed performance statistics."""
        print("\n📊 ZIA-X Enhanced Performance Statistics" + "\n" + "=" * 45)
        status = self.get_system_status()
        session_stats = status['session_stats']
        print("🎯 CNS Performance:")
        print(f"  📝 Total Commands: {session_stats['commands_processed']}\n  ✅ Success Rate: {(session_stats['successful_commands'] / max(session_stats['commands_processed'], 1)) * 100:.1f}%")
        print(f"  ⚡ Brain Usage Distribution:")
        total_usage = sum(session_stats['brain_usage'].values())
        if total_usage > 0:
            for brain, usage in session_stats['brain_usage'].items():
                print(f"    • {brain.replace('_', ' ').title()}: {usage} ({(usage / total_usage) * 100:.1f}%)")
        
        if self.decision_brain:
            print("\n🧠 Decision Brain V2.0:")
            decision_stats = self.decision_brain.get_performance_stats()
            print(f"  🎯 Success Rate: {decision_stats['success_rate_percent']}%\n  🤔 Clarification Rate: {decision_stats.get('clarification_rate_percent', 0)}%\n  ⚡ Avg Confidence: {decision_stats['average_confidence']:.2f}")
        
        if self.automation_brain:
            print("\n🤖 Automation Brain V1.5:")
            auto_stats = self.automation_brain.get_performance_stats()
            print(f"  🎯 Success Rate: {(auto_stats['successful_commands'] / max(auto_stats['total_commands'], 1)) * 100:.1f}%\n  🔍 Search Queries: {auto_stats['search_queries']}")

    def run(self):
        """Enhanced main execution loop for ZIA-X CNS."""
        try:
            if self.memory_brain:
                self.memory_brain.log_action("CNS", "SESSION_STARTED", { "version": "1.0.0", "timestamp": datetime.datetime.now().isoformat(), "active_brains": [b for b, a in self.get_system_status()['brain_status'].items() if a]})
            
            text_thread = threading.Thread(target=self._text_command_loop, name="EnhancedTextInputThread")
            text_thread.daemon = True
            text_thread.start()
            
            print("🚀 ZIA-X Enhanced CNS is now running with all brain modules!")
            print("💡 Enhanced features: Advanced decision-making, intelligent automation, learning capabilities")
            
            text_thread.join()
        except Exception as e:
            self.logger.critical(f"Critical error in main execution loop: {e}", exc_info=True)
            print(f"💥 Critical error occurred: {e}")
        finally:
            self.shutdown()

    def shutdown(self):
        """Enhanced graceful shutdown procedure."""
        if self._shutdown_event.is_set(): return
        print("\n🔄 ZIA-X Enhanced CNS shutting down...")
        self._shutdown_event.set()
        
        try:
            final_stats = self.get_system_status()
            shutdown_order = [('Decision Brain V2.0', self.decision_brain), ('Automation Brain V1.5', self.automation_brain), ('Security Brain', self.security_brain), ('Response Brain', self.response_brain), ('Memory Brain', self.memory_brain)]
            
            for brain_name, brain_instance in shutdown_order:
                if brain_instance and hasattr(brain_instance, 'shutdown'):
                    try: brain_instance.shutdown(); print(f"✅ {brain_name} shutdown complete")
                    except Exception as e: self.logger.error(f"Error shutting down {brain_name}: {e}")
            
            if self.memory_brain:
                try:
                    self.memory_brain.log_action("CNS", "SESSION_ENDED", { "session_duration": str(datetime.datetime.now() - self.session_stats['session_start']).split('.')[0], "final_stats": final_stats['session_stats'], "commands_processed": self.session_stats['commands_processed'], "success_rate": (self.session_stats['successful_commands'] / max(self.session_stats['commands_processed'], 1)) * 100, "shutdown_time": datetime.datetime.now().isoformat(), "message": "Enhanced CNS session completed successfully, Boss!" })
                except Exception as e: self.logger.error(f"Error logging final session data: {e}")
            
            print(f"\n📊 Session Summary:\n⏰ Duration: {str(datetime.datetime.now() - self.session_stats['session_start']).split('.')[0]}\n📝 Commands Processed: {self.session_stats['commands_processed']}\n✅ Success Rate: {(self.session_stats['successful_commands'] / max(self.session_stats['commands_processed'], 1)) * 100:.1f}%")
            print("✅ ZIA-X Enhanced CNS shutdown complete.\n👋 Thank you for using ZIA-X Enhanced Edition, Boss!")
        except Exception as e:
            self.logger.error(f"Error during enhanced shutdown: {e}")
            print(f"⚠️ Shutdown completed with warnings: {e}")

def main():
    """Enhanced main function with better error handling."""
    try:
        print("🚀 Starting ZIA-X Enhanced Edition...\n" + "-" * 60)
        cns = VitaCNS()
        cns.run()
    except KeyboardInterrupt: print("\n🛑 Keyboard interrupt received")
    except SystemExit: print("\n🚪 System exit requested")
    except Exception as e:
        logging.critical(f"Fatal error in main: {e}", exc_info=True)
        print(f"\n💥 Fatal error occurred: {e}\n📝 Check logs for detailed error information")
    finally:
        print("\n👋 ZIA-X Enhanced Edition terminated")

if __name__ == "__main__":
    main()
