"""
security_brain.py - ZIA's Security Guardian Module

This module implements ZIA's conscience for internet access control.
It acts as a "VIP Bouncer" ensuring all web access is safe and authorized by Boss.

Core Principles:
- 100% offline privacy (no external validation)
- Explicit user permission for new sites
- Modular brain architecture compatible with CNS
"""

import re
import logging
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional


class SecurityBrain:
    """
    ZIA's Security Brain - Acts as a guardian for all internet access.
    
    This brain implements a "VIP Bouncer" system that categorizes websites into:
    - Trusted sites (VIP list): Always allowed
    - Blocked sites (Never list): Always denied  
    - One-time sessions: Temporary access granted
    - Unknown sites: Require Boss's explicit permission
    """
    
    def __init__(self, cns, config):
        """
        Initialize the Security Brain with CNS and configuration.
        
        Args:
            cns: Central Nervous System object for communication with other brains
            config: Configuration object containing security lists and settings
        """
        self.cns = cns
        self.config = config
        self.logger = logging.getLogger(f"ZIA.{self.__class__.__name__}")
        
        # Load security lists from configuration
        self.trusted_sites = set(config.get('trusted_sites', []))
        self.blocked_sites = set(config.get('blocked_sites', []))
        self.one_time_sessions = set(config.get('one_time_sessions', []))
        
        # Track session state for one-time access cleanup
        self.session_usage = {}
        
        self.logger.info("Security Brain initialized - Guardian mode active")
        self.logger.info(f"Loaded {len(self.trusted_sites)} trusted sites")
        self.logger.info(f"Loaded {len(self.blocked_sites)} blocked sites")
        self.logger.info(f"Loaded {len(self.one_time_sessions)} one-time sessions")
    
    def extract_domain(self, url: str) -> str:
        """
        Extract the domain from a URL for security list comparison.
        
        Args:
            url (str): The full URL to extract domain from
            
        Returns:
            str: Clean domain name (e.g., 'example.com')
        """
        try:
            # Handle URLs without protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove 'www.' prefix for consistency
            if domain.startswith('www.'):
                domain = domain[4:]
                
            return domain
        except Exception as e:
            self.logger.warning(f"Failed to parse URL '{url}': {e}")
            return url.lower()  # Fallback to original URL
    
    def is_valid_domain(self, domain: str) -> bool:
        """
        Validate if a domain name is properly formatted.
        
        Args:
            domain (str): Domain to validate
            
        Returns:
            bool: True if domain is valid
        """
        # Basic domain validation regex
        domain_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
            r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        )
        return bool(domain_pattern.match(domain)) if domain else False
    
    def check_website_access(self, url: str) -> str:
        """
        Main security checkpoint - determines if Boss can access a website.
        
        Implements the "VIP Bouncer" logic:
        1. Check if site is blocked (immediate denial)
        2. Check if site is trusted (immediate approval)
        3. Check if site has one-time session (temporary approval)
        4. Ask Boss for permission on unknown sites
        
        Args:
            url (str): The URL that needs access permission
            
        Returns:
            str: One of:
                - "DENIED" - Access blocked
                - "ALLOWED" - Access granted
                - "ASK_USER:..." - Permission request for Boss
        """
        if not url or not url.strip():
            self.logger.warning("Empty URL provided to security check")
            return "DENIED"
        
        domain = self.extract_domain(url.strip())
        
        if not self.is_valid_domain(domain):
            self.logger.warning(f"Invalid domain format: {domain}")
            return "DENIED"
        
        self.logger.info(f"Security check requested for: {domain}")
        
        # STEP 1: Check blocklist (highest priority)
        if domain in self.blocked_sites:
            self.logger.info(f"Access DENIED - {domain} is on blocklist")
            return "DENIED"
        
        # STEP 2: Check VIP/trusted list
        if domain in self.trusted_sites:
            self.logger.info(f"Access ALLOWED - {domain} is on trusted list")
            return "ALLOWED"
        
        # STEP 3: Check one-time sessions
        if domain in self.one_time_sessions:
            self.logger.info(f"Access ALLOWED - {domain} has one-time session")
            # Mark as used (could implement auto-removal logic here)
            self.session_usage[domain] = self.session_usage.get(domain, 0) + 1
            return "ALLOWED"
        
        # STEP 4: Unknown site - ask Boss for permission
        self.logger.info(f"Unknown site detected: {domain} - requesting Boss permission")
        return f"ASK_USER:This is a new site ('{domain}'). How should I proceed? (Options: Yes, No, This time only)"
    
    def add_to_trusted(self, domain: str) -> bool:
        """
        Add a domain to the trusted sites list.
        
        Args:
            domain (str): Domain to add to trusted list
            
        Returns:
            bool: True if successfully added
        """
        try:
            clean_domain = self.extract_domain(domain)
            if not self.is_valid_domain(clean_domain):
                self.logger.error(f"Cannot add invalid domain to trusted list: {clean_domain}")
                return False
            
            # Remove from other lists if present
            self.blocked_sites.discard(clean_domain)
            self.one_time_sessions.discard(clean_domain)
            
            self.trusted_sites.add(clean_domain)
            self.logger.info(f"Added {clean_domain} to trusted sites")
            
            # Update config if needed
            self._update_config_lists()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add {domain} to trusted sites: {e}")
            return False
    
    def add_to_blocked(self, domain: str) -> bool:
        """
        Add a domain to the blocked sites list.
        
        Args:
            domain (str): Domain to add to blocked list
            
        Returns:
            bool: True if successfully added
        """
        try:
            clean_domain = self.extract_domain(domain)
            if not self.is_valid_domain(clean_domain):
                self.logger.error(f"Cannot add invalid domain to blocked list: {clean_domain}")
                return False
            
            # Remove from other lists if present
            self.trusted_sites.discard(clean_domain)
            self.one_time_sessions.discard(clean_domain)
            
            self.blocked_sites.add(clean_domain)
            self.logger.info(f"Added {clean_domain} to blocked sites")
            
            # Update config if needed
            self._update_config_lists()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add {domain} to blocked sites: {e}")
            return False
    
    def add_to_one_time(self, domain: str) -> bool:
        """
        Add a domain to the one-time sessions list.
        
        Args:
            domain (str): Domain to add to one-time list
            
        Returns:
            bool: True if successfully added
        """
        try:
            clean_domain = self.extract_domain(domain)
            if not self.is_valid_domain(clean_domain):
                self.logger.error(f"Cannot add invalid domain to one-time list: {clean_domain}")
                return False
            
            # Don't remove from blocked/trusted - one-time is temporary
            self.one_time_sessions.add(clean_domain)
            self.logger.info(f"Added {clean_domain} to one-time sessions")
            
            # Update config if needed
            self._update_config_lists()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add {domain} to one-time sessions: {e}")
            return False
    
    def remove_from_trusted(self, domain: str) -> bool:
        """Remove a domain from trusted sites list."""
        clean_domain = self.extract_domain(domain)
        if clean_domain in self.trusted_sites:
            self.trusted_sites.remove(clean_domain)
            self.logger.info(f"Removed {clean_domain} from trusted sites")
            self._update_config_lists()
            return True
        return False
    
    def remove_from_blocked(self, domain: str) -> bool:
        """Remove a domain from blocked sites list."""
        clean_domain = self.extract_domain(domain)
        if clean_domain in self.blocked_sites:
            self.blocked_sites.remove(clean_domain)
            self.logger.info(f"Removed {clean_domain} from blocked sites")
            self._update_config_lists()
            return True
        return False
    
    def clear_one_time_sessions(self) -> int:
        """
        Clear all one-time sessions (useful for session cleanup).
        
        Returns:
            int: Number of sessions cleared
        """
        count = len(self.one_time_sessions)
        self.one_time_sessions.clear()
        self.session_usage.clear()
        self.logger.info(f"Cleared {count} one-time sessions")
        self._update_config_lists()
        return count
    
    def get_security_status(self) -> Dict[str, Any]:
        """
        Get current security status and statistics.
        
        Returns:
            dict: Security brain status information
        """
        return {
            "trusted_sites_count": len(self.trusted_sites),
            "blocked_sites_count": len(self.blocked_sites),
            "one_time_sessions_count": len(self.one_time_sessions),
            "session_usage": dict(self.session_usage),
            "trusted_sites": list(self.trusted_sites),
            "blocked_sites": list(self.blocked_sites),
            "one_time_sessions": list(self.one_time_sessions)
        }
    
    def _update_config_lists(self):
        """
        Update the configuration with current security lists.
        This ensures persistence across sessions.
        """
        try:
            if hasattr(self.config, 'update'):
                self.config.update({
                    'trusted_sites': list(self.trusted_sites),
                    'blocked_sites': list(self.blocked_sites),
                    'one_time_sessions': list(self.one_time_sessions)
                })
            self.logger.debug("Updated configuration with current security lists")
        except Exception as e:
            self.logger.warning(f"Failed to update config lists: {e}")
    
    def __str__(self) -> str:
        """String representation of Security Brain status."""
        return (f"SecurityBrain(trusted={len(self.trusted_sites)}, "
                f"blocked={len(self.blocked_sites)}, "
                f"one_time={len(self.one_time_sessions)})")


# Example usage and testing (can be removed in production)
if __name__ == "__main__":
    # Mock objects for testing
    class MockCNS:
        pass
    
    class MockConfig:
        def __init__(self):
            self.data = {
                'trusted_sites': ['github.com', 'stackoverflow.com'],
                'blocked_sites': ['malicious-site.com'],
                'one_time_sessions': ['temp-site.com']
            }
        
        def get(self, key, default=None):
            return self.data.get(key, default)
        
        def update(self, updates):
            self.data.update(updates)
    
    # Test the SecurityBrain
    logging.basicConfig(level=logging.INFO)
    
    cns = MockCNS()
    config = MockConfig()
    brain = SecurityBrain(cns, config)
    
    # Test cases
    test_urls = [
        "https://github.com/user/repo",  # Should be allowed (trusted)
        "https://malicious-site.com/bad",  # Should be denied (blocked)
        "https://temp-site.com/page",  # Should be allowed (one-time)
        "https://unknown-site.com"  # Should ask user
    ]
    
    for url in test_urls:
        result = brain.check_website_access(url)
        print(f"URL: {url}")
        print(f"Result: {result}")
        print("-" * 50)