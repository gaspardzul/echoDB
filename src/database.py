import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
import json


class EchoDatabase:
    def __init__(self, db_path: str = None):
        if db_path is None:
            config_dir = Path.home() / ".echodb"
            config_dir.mkdir(exist_ok=True)
            db_path = config_dir / "echodb.db"
        
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def init_database(self):
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                log_path TEXT,
                auto_scroll INTEGER DEFAULT 1,
                queries_only INTEGER DEFAULT 0,
                font_size INTEGER DEFAULT 10,
                filter_text TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                connection_id INTEGER,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (connection_id) REFERENCES connections(id)
            )
        """)
        
        conn.commit()
        self.close()
    
    def save_connection(self, connection_data: Dict) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO connections (name, log_path, auto_scroll, queries_only, font_size, filter_text)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    log_path = excluded.log_path,
                    auto_scroll = excluded.auto_scroll,
                    queries_only = excluded.queries_only,
                    font_size = excluded.font_size,
                    filter_text = excluded.filter_text,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                connection_data.get('name'),
                connection_data.get('log_path', ''),
                1 if connection_data.get('auto_scroll', True) else 0,
                1 if connection_data.get('queries_only', False) else 0,
                connection_data.get('font_size', 10),
                connection_data.get('filter_text', '')
            ))
            
            connection_id = cursor.lastrowid
            conn.commit()
            
            return connection_id
            
        except sqlite3.Error as e:
            print(f"Error saving connection: {e}")
            conn.rollback()
            return -1
        finally:
            self.close()
    
    def get_all_connections(self) -> List[Dict]:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, log_path, auto_scroll, queries_only, font_size, filter_text, created_at, updated_at
                FROM connections
                ORDER BY updated_at DESC
            """)
            
            rows = cursor.fetchall()
            connections = []
            
            for row in rows:
                connections.append({
                    'id': row['id'],
                    'name': row['name'],
                    'log_path': row['log_path'],
                    'auto_scroll': bool(row['auto_scroll']),
                    'queries_only': bool(row['queries_only']),
                    'font_size': row['font_size'],
                    'filter_text': row['filter_text'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                })
            
            return connections
            
        except sqlite3.Error as e:
            print(f"Error getting connections: {e}")
            return []
        finally:
            self.close()
    
    def get_connection_by_name(self, name: str) -> Optional[Dict]:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, log_path, auto_scroll, queries_only, font_size, filter_text
                FROM connections
                WHERE name = ?
            """, (name,))
            
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row['id'],
                    'name': row['name'],
                    'log_path': row['log_path'],
                    'auto_scroll': bool(row['auto_scroll']),
                    'queries_only': bool(row['queries_only']),
                    'font_size': row['font_size'],
                    'filter_text': row['filter_text']
                }
            
            return None
            
        except sqlite3.Error as e:
            print(f"Error getting connection: {e}")
            return None
        finally:
            self.close()
    
    def delete_connection(self, name: str) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM connections WHERE name = ?", (name,))
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error deleting connection: {e}")
            conn.rollback()
            return False
        finally:
            self.close()
    
    def update_connection(self, name: str, connection_data: Dict) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE connections
                SET log_path = ?,
                    auto_scroll = ?,
                    queries_only = ?,
                    font_size = ?,
                    filter_text = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
            """, (
                connection_data.get('log_path', ''),
                1 if connection_data.get('auto_scroll', True) else 0,
                1 if connection_data.get('queries_only', False) else 0,
                connection_data.get('font_size', 10),
                connection_data.get('filter_text', ''),
                name
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error updating connection: {e}")
            conn.rollback()
            return False
        finally:
            self.close()
    
    def save_app_setting(self, key: str, value: str) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO app_settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, value))
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error saving app setting: {e}")
            conn.rollback()
            return False
        finally:
            self.close()
    
    def get_app_setting(self, key: str, default: str = None) -> Optional[str]:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            
            if row:
                return row['value']
            return default
            
        except sqlite3.Error as e:
            print(f"Error getting app setting: {e}")
            return default
        finally:
            self.close()
    
    def migrate_from_json(self, json_file: Path) -> int:
        if not json_file.exists():
            return 0
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            tabs = config.get('tabs', [])
            migrated = 0
            
            for tab in tabs:
                if self.save_connection(tab) > 0:
                    migrated += 1
            
            return migrated
            
        except Exception as e:
            print(f"Error migrating from JSON: {e}")
            return 0
