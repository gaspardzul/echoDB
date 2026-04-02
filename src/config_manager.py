import json
from pathlib import Path
from typing import List, Dict, Optional
from src.database import EchoDatabase


class ConfigManager:
    def __init__(self, config_file: str = "echodb_config.json"):
        self.config_dir = Path.home() / ".echodb"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / config_file
        self.db = EchoDatabase()
        
        self.migrate_from_json_if_needed()
        
    def migrate_from_json_if_needed(self):
        if self.config_file.exists():
            migrated = self.db.migrate_from_json(self.config_file)
            if migrated > 0:
                print(f"Migrated {migrated} connections from JSON to SQLite")
                backup_file = self.config_file.with_suffix('.json.backup')
                self.config_file.rename(backup_file)
                print(f"JSON config backed up to {backup_file}")
        
    def save_tabs_config(self, tabs_settings: List[Dict]) -> bool:
        try:
            for tab_config in tabs_settings:
                self.db.save_connection(tab_config)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_tabs_config(self) -> List[Dict]:
        try:
            return self.db.get_all_connections()
        except Exception as e:
            print(f"Error loading config: {e}")
            return []
    
    def save_connection(self, connection_data: Dict) -> bool:
        try:
            return self.db.save_connection(connection_data) > 0
        except Exception as e:
            print(f"Error saving connection: {e}")
            return False
    
    def delete_connection(self, name: str) -> bool:
        try:
            return self.db.delete_connection(name)
        except Exception as e:
            print(f"Error deleting connection: {e}")
            return False
    
    def get_connection_count(self) -> int:
        try:
            connections = self.db.get_all_connections()
            return len(connections)
        except Exception as e:
            print(f"Error getting connection count: {e}")
            return 0
    
    def clear_config(self) -> bool:
        try:
            connections = self.db.get_all_connections()
            for conn in connections:
                self.db.delete_connection(conn['name'])
            return True
        except Exception as e:
            print(f"Error clearing config: {e}")
            return False
