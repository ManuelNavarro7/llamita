#!/usr/bin/env python3
"""
Simple analytics tracking for Llamita
Optional - can be disabled for privacy
"""

import json
import os
import requests
from datetime import datetime

class Analytics:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.analytics_file = "llamita_analytics.json"
        
    def track_app_start(self):
        """Track when the app starts"""
        if not self.enabled:
            return
            
        data = {
            "event": "app_start",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        self._save_event(data)
        
    def track_message_sent(self, message_length):
        """Track when a message is sent"""
        if not self.enabled:
            return
            
        data = {
            "event": "message_sent",
            "timestamp": datetime.now().isoformat(),
            "message_length": message_length
        }
        self._save_event(data)
        
    def track_response_received(self, response_length):
        """Track when a response is received"""
        if not self.enabled:
            return
            
        data = {
            "event": "response_received",
            "timestamp": datetime.now().isoformat(),
            "response_length": response_length
        }
        self._save_event(data)
        
    def _save_event(self, data):
        """Save event to local file"""
        try:
            events = []
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    events = json.load(f)
            
            events.append(data)
            
            with open(self.analytics_file, 'w') as f:
                json.dump(events, f, indent=2)
                
        except Exception as e:
            print(f"Analytics error: {e}")
            
    def get_usage_stats(self):
        """Get usage statistics"""
        if not os.path.exists(self.analytics_file):
            return {"total_events": 0, "app_starts": 0, "messages": 0}
            
        try:
            with open(self.analytics_file, 'r') as f:
                events = json.load(f)
                
            stats = {
                "total_events": len(events),
                "app_starts": len([e for e in events if e.get("event") == "app_start"]),
                "messages": len([e for e in events if e.get("event") == "message_sent"]),
                "responses": len([e for e in events if e.get("event") == "response_received"])
            }
            return stats
            
        except Exception as e:
            print(f"Error reading analytics: {e}")
            return {"total_events": 0, "app_starts": 0, "messages": 0}
