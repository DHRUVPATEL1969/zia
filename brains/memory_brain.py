"""
ZIA-X Memory Brain Module
========================

This module implements ZIA's secure, encrypted memory system - the "Black Box" recorder
that maintains a complete log of all actions performed by the AI assistant.

Core Features:
- 100% offline privacy with military-grade encryption
- Persistent storage of all AI actions and decisions
- Secure key management with automatic generation
- Robust error handling and data integrity protection

Author: ZIA-X Development Team
License: Proprietary - All Rights Reserved
"""

import os
import json
import logging
import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError as e:
    raise ImportError(
        "The 'cryptography' library is required for the MemoryBrain module. "
        "Install it with: pip install cryptography"
    ) from e


class MemoryBrain:
    """
    ZIA's Secure Memory Brain - The Black Box Recorder
    
    This class manages encrypted storage and retrieval of all AI actions,
    ensuring complete privacy and security of all operations performed by ZIA.
    
    The memory system uses Fernet encryption (AES 128 in CBC mode) to protect
    all stored data, with automatic key generation and management.
    """
    
    def __init__(self, cns: Any, config: Any):
        """
        Initialize ZIA's Memory Brain with encryption capabilities.
        
        Args:
            cns: The Central Nervous System object (main CNS script)
            config: Configuration object containing system settings
        """
        self.cns = cns
        self.config = config
        
        # Setup logging for the memory brain itself
        self.logger = logging.getLogger(__name__)
        
        # Define secure storage paths with emojis as specified
        self.key_file_path = Path("config/memory.key")  # ⚙️ config/memory.key
        self.log_file_path = Path("database/memory_log.json.encrypted")  # 🗄️ database/memory_log.json.encrypted
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Initialize encryption system
        self.encryption_key = self._load_or_generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Log successful initialization
        self.logger.info("ZIA Memory Brain initialized successfully")
        
        # Record the brain activation in its own log
        self.log_action("MEMORY_BRAIN", "INITIALIZED", {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "operational",
            "encryption": "active",
            "boss_greeting": "Memory Brain online and ready to serve, Boss!"
        })
    
    def _ensure_directories(self) -> None:
        """
        Ensure that required directories exist for secure storage.
        Creates config and database directories if they don't exist.
        """
        try:
            self.key_file_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            self.logger.debug("Storage directories verified/created")
        except Exception as e:
            self.logger.error(f"Failed to create storage directories: {e}")
            raise
    
    def _load_or_generate_key(self) -> bytes:
        """
        Load existing encryption key or generate a new one.
        
        This method implements secure key management:
        - If a key file exists, it loads and validates the key
        - If no key exists, it generates a new cryptographically secure key
        - The key is stored with restricted file permissions for security
        
        Returns:
            bytes: The encryption key for use with Fernet cipher
            
        Raises:
            Exception: If key generation or loading fails
        """
        try:
            if self.key_file_path.exists():
                # Load existing key
                with open(self.key_file_path, 'rb') as key_file:
                    key = key_file.read()
                    # Validate key format by attempting to create Fernet instance
                    Fernet(key)  # This will raise an exception if key is invalid
                    self.logger.info("Encryption key loaded successfully from existing file")
                    return key
            else:
                # Generate new key
                key = Fernet.generate_key()
                
                # Save key with restricted permissions
                with open(self.key_file_path, 'wb') as key_file:
                    key_file.write(key)
                
                # Set file permissions (Unix/Linux systems) - read/write for owner only
                try:
                    os.chmod(self.key_file_path, 0o600)
                except (OSError, AttributeError):
                    # Windows or permission error - log warning but continue
                    self.logger.warning("Could not set restrictive permissions on key file (Windows/Permission issue)")
                
                self.logger.info("New encryption key generated and saved securely")
                return key
                
        except Exception as e:
            self.logger.error(f"Failed to load or generate encryption key: {e}")
            raise RuntimeError(f"Memory Brain key management failure: {e}") from e
    
    def log_action(self, brain: str, action: str, details: Dict[str, Any]) -> None:
        """
        Log an action to ZIA's encrypted memory with full security.
        
        This is the primary method for recording all of ZIA's activities.
        Every action is timestamped, encrypted, and stored securely.
        
        Args:
            brain (str): The brain module that performed the action (e.g., "AUTOMATION_BRAIN", "DECISION_BRAIN")
            action (str): The action identifier (e.g., "EXECUTED_COMMAND", "USER_INTERACTION")
            details (Dict[str, Any]): Dictionary containing detailed information about the action
            
        Example:
            memory_brain.log_action("AUTOMATION_BRAIN", "EXECUTED_COMMAND", {
                "command": "create_file",
                "file_path": "/home/user/document.txt",
                "success": True,
                "execution_time": 0.025
            })
        """
        try:
            # Create comprehensive log entry with all required fields
            log_entry = {
                "timestamp": datetime.datetime.now().isoformat(),
                "brain": brain,
                "action": action,
                "details": details,
                "session_id": getattr(self.config, 'session_id', 'unknown'),
                "zia_version": getattr(self.config, 'version', '1.0.0')
            }
            
            # Serialize to JSON with compact formatting
            json_data = json.dumps(log_entry, ensure_ascii=False, separators=(',', ':'))
            
            # Encrypt the JSON data using Fernet cipher
            encrypted_data = self.cipher_suite.encrypt(json_data.encode('utf-8'))
            
            # Append to encrypted log file (each entry on new line for easy parsing)
            with open(self.log_file_path, 'ab') as log_file:
                log_file.write(encrypted_data + b'\n')
            
            self.logger.debug(f"Action logged successfully: {brain}.{action}")
            
        except Exception as e:
            # Critical error - memory system failure
            self.logger.error(f"Failed to log action '{brain}.{action}': {e}")
            # Don't raise exception to avoid breaking main operations
            # But ensure Boss is informed of critical failure
            print(f"⚠️  ZIA MEMORY BRAIN CRITICAL ERROR: Unable to log action - {e}")
    
    def read_log(self) -> List[Dict[str, Any]]:
        """
        Read and decrypt all logged actions from ZIA's memory.
        
        This method decrypts and parses the entire memory log, returning
        a chronological list of all actions performed by ZIA.
        
        Returns:
            List[Dict[str, Any]]: List of decrypted log entry dictionaries
            
        Note:
            This method includes robust error handling for corrupted entries.
            Corrupted lines are logged but skipped to maintain system stability.
        """
        log_entries = []
        
        try:
            if not self.log_file_path.exists():
                self.logger.info("No memory log file found - returning empty log")
                return log_entries
            
            with open(self.log_file_path, 'rb') as log_file:
                line_number = 0
                for line in log_file:
                    line_number += 1
                    line = line.strip()
                    
                    if not line:  # Skip empty lines
                        continue
                    
                    try:
                        # Decrypt the line using Fernet cipher
                        decrypted_data = self.cipher_suite.decrypt(line)
                        
                        # Parse JSON back to dictionary
                        log_entry = json.loads(decrypted_data.decode('utf-8'))
                        log_entries.append(log_entry)
                        
                    except Exception as line_error:
                        # Log corrupted entry but continue processing other entries
                        self.logger.warning(
                            f"Corrupted log entry at line {line_number}: {line_error}"
                        )
                        # Optionally add a placeholder entry for corrupted data
                        log_entries.append({
                            "timestamp": "unknown",
                            "brain": "MEMORY_BRAIN",
                            "action": "CORRUPTED_ENTRY",
                            "details": {
                                "line_number": line_number,
                                "error": str(line_error),
                                "status": "data_corruption_detected"
                            }
                        })
            
            self.logger.info(f"Successfully read {len(log_entries)} log entries from encrypted storage")
            return log_entries
            
        except Exception as e:
            self.logger.error(f"Failed to read memory log: {e}")
            raise RuntimeError(f"Memory Brain log reading failure: {e}") from e
    
    def clear_log(self) -> bool:
        """
        Securely delete the entire log file (DANGEROUS OPERATION).
        
        This method completely erases all logged actions. Use with extreme caution.
        The Boss should be warned that this action is irreversible.
        
        Returns:
            bool: True if log was cleared successfully, False otherwise
            
        Note:
            This is a destructive operation that cannot be undone.
            All historical data will be permanently lost.
        """
        try:
            if self.log_file_path.exists():
                # Log the clearing action before deletion (for audit trail)
                self.log_action("MEMORY_BRAIN", "LOG_CLEAR_INITIATED", {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "authorized_by": "Boss",
                    "warning": "All historical memory data will be permanently deleted"
                })
                
                # Actually delete the file
                self.log_file_path.unlink()
                self.logger.warning("⚠️  ZIA memory log has been completely cleared by Boss request")
                
                # Create a new log entry documenting the clearing (will create new file)
                self.log_action("MEMORY_BRAIN", "LOG_CLEARED", {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status": "complete",
                    "authorized_by": "Boss",
                    "note": "Fresh memory log started after clearing"
                })
                
                return True
            else:
                self.logger.info("No log file exists to clear")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to clear memory log: {e}")
            return False
    
    def get_log_stats(self) -> Dict[str, Any]:
        """
        Get statistics about ZIA's memory log without decrypting all entries.
        
        This method provides useful information about the log file size,
        entry count, and other metadata for system monitoring.
        
        Returns:
            Dict[str, Any]: Statistics including entry count, file size, etc.
        """
        try:
            stats = {
                "total_entries": 0,
                "file_size_bytes": 0,
                "file_exists": False,
                "encryption_status": "active",
                "key_file_exists": self.key_file_path.exists()
            }
            
            if self.log_file_path.exists():
                stats["file_exists"] = True
                stats["file_size_bytes"] = self.log_file_path.stat().st_size
                
                # Count entries without full decryption (for performance)
                with open(self.log_file_path, 'rb') as f:
                    stats["total_entries"] = sum(1 for line in f if line.strip())
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get log stats: {e}")
            return {
                "error": str(e), 
                "encryption_status": "active",
                "file_exists": False,
                "total_entries": 0
            }
    
    def __del__(self):
        """
        Cleanup method called when MemoryBrain is destroyed.
        Logs the shutdown event for completeness and audit trail.
        """
        try:
            if hasattr(self, 'log_action') and hasattr(self, 'cipher_suite'):
                self.log_action("MEMORY_BRAIN", "SHUTDOWN", {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "status": "clean_shutdown",
                    "message": "Memory Brain going offline. All memories secured, Boss!"
                })
        except:
            # Ignore any errors during cleanup to prevent cascading failures
            pass


# Example usage and testing functionality
if __name__ == "__main__":
    """
    Test suite for MemoryBrain functionality.
    This section can be removed in production deployment.
    """
    
    # Mock objects for testing
    class MockConfig:
        session_id = "test_session_001"
        version = "1.0.0-dev"
    
    class MockCNS:
        def __init__(self):
            self.name = "Test CNS"
    
    print("🧠 Testing ZIA Memory Brain...")
    print("=" * 50)
    
    try:
        # Initialize memory brain with mock objects
        memory = MemoryBrain(MockCNS(), MockConfig())
        print("✅ Memory Brain initialized successfully")
        
        # Test action logging
        print("\n📝 Testing action logging...")
        memory.log_action("TEST_BRAIN", "INITIALIZATION_TEST", {
            "test_parameter": "test_value",
            "success": True,
            "notes": "Memory brain functionality test"
        })
        
        memory.log_action("AUTOMATION_BRAIN", "FILE_CREATED", {
            "filename": "test_document.txt",
            "path": "/home/user/documents/",
            "size_bytes": 1024,
            "success": True
        })
        
        print("✅ Action logging completed")
        
        # Test log reading
        print("\n📖 Testing log reading...")
        logs = memory.read_log()
        print(f"✅ Successfully read {len(logs)} log entries")
        
        # Display sample log entry
        if logs:
            print(f"📋 Sample log entry: {logs[-1]['brain']}.{logs[-1]['action']}")
        
        # Test statistics
        print("\n📊 Testing log statistics...")
        stats = memory.get_log_stats()
        print(f"✅ Log stats: {stats['total_entries']} entries, {stats['file_size_bytes']} bytes")
        
        print("\n🎉 ZIA Memory Brain test completed successfully!")
        print("🔒 All data encrypted and stored securely")
        
    except Exception as e:
        print(f"❌ Memory Brain test failed: {e}")
        import traceback
        traceback.print_exc()