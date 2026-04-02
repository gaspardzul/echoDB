import psycopg2
from psycopg2 import sql, extensions
from typing import Optional, Dict, Tuple
from pathlib import Path


class PostgreSQLConnector:
    def __init__(self):
        self.connection: Optional[extensions.connection] = None
        self.connection_params: Optional[Dict] = None
        
    def connect(self, host: str, port: int, database: str, user: str, password: str) -> Tuple[bool, str]:
        try:
            self.connection_params = {
                'host': host,
                'port': port,
                'database': database,
                'user': user,
                'password': password
            }
            
            self.connection = psycopg2.connect(**self.connection_params)
            self.connection.autocommit = True
            
            return True, "Connection successful"
            
        except psycopg2.Error as e:
            return False, f"Connection failed: {str(e)}"
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def is_connected(self) -> bool:
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except:
            return False
    
    def get_postgresql_conf_path(self) -> Optional[Path]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW config_file;")
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return Path(result[0])
            return None
        except psycopg2.Error:
            return None
    
    def get_data_directory(self) -> Optional[Path]:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW data_directory;")
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return Path(result[0])
            return None
        except psycopg2.Error:
            return None
    
    def get_log_directory(self) -> Optional[Path]:
        try:
            data_dir = self.get_data_directory()
            if not data_dir:
                return None
            
            cursor = self.connection.cursor()
            cursor.execute("SHOW log_directory;")
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                log_dir = result[0]
                if log_dir.startswith('/'):
                    return Path(log_dir)
                else:
                    return data_dir / log_dir
            return None
        except psycopg2.Error:
            return None
    
    def get_current_log_settings(self) -> Dict[str, str]:
        settings = {}
        params = [
            'logging_collector',
            'log_destination',
            'log_directory',
            'log_filename',
            'log_statement',
            'log_min_duration_statement',
            'log_line_prefix',
            'log_duration'
        ]
        
        try:
            cursor = self.connection.cursor()
            for param in params:
                cursor.execute(f"SHOW {param};")
                result = cursor.fetchone()
                if result:
                    settings[param] = result[0]
            cursor.close()
        except psycopg2.Error as e:
            settings['error'] = str(e)
        
        return settings
    
    def configure_logging(self) -> Tuple[bool, str]:
        try:
            cursor = self.connection.cursor()
            
            changes_made = []
            
            cursor.execute("ALTER SYSTEM SET log_min_duration_statement = 0;")
            changes_made.append("log_min_duration_statement = 0")
            
            cursor.execute("ALTER SYSTEM SET log_statement = 'all';")
            changes_made.append("log_statement = 'all'")
            
            cursor.execute("ALTER SYSTEM SET log_duration = 'on';")
            changes_made.append("log_duration = 'on'")
            
            cursor.execute("ALTER SYSTEM SET log_line_prefix = '%t [%p] ';")
            changes_made.append("log_line_prefix = '%t [%p] '")
            
            cursor.execute("SELECT pg_reload_conf();")
            
            cursor.close()
            
            message = "Logging configured successfully. Changes:\n" + "\n".join(f"  • {c}" for c in changes_made)
            message += "\n\nNote: Some changes may require a PostgreSQL restart to take full effect."
            
            return True, message
            
        except psycopg2.Error as e:
            return False, f"Failed to configure logging: {str(e)}"
    
    def disable_logging(self) -> Tuple[bool, str]:
        try:
            cursor = self.connection.cursor()
            
            changes_made = []
            
            cursor.execute("ALTER SYSTEM SET log_min_duration_statement = -1;")
            changes_made.append("log_min_duration_statement = -1 (disabled)")
            
            cursor.execute("ALTER SYSTEM SET log_statement = 'none';")
            changes_made.append("log_statement = 'none'")
            
            cursor.execute("ALTER SYSTEM SET log_duration = 'off';")
            changes_made.append("log_duration = 'off'")
            
            cursor.execute("SELECT pg_reload_conf();")
            
            cursor.close()
            
            message = "Logging disabled successfully. Changes:\n" + "\n".join(f"  • {c}" for c in changes_made)
            message += "\n\nNote: Logs will no longer be generated for queries."
            
            return True, message
            
        except psycopg2.Error as e:
            return False, f"Failed to disable logging: {str(e)}"
    
    def reset_logging_to_defaults(self) -> Tuple[bool, str]:
        try:
            cursor = self.connection.cursor()
            
            changes_made = []
            
            cursor.execute("ALTER SYSTEM RESET log_min_duration_statement;")
            changes_made.append("log_min_duration_statement (reset to default)")
            
            cursor.execute("ALTER SYSTEM RESET log_statement;")
            changes_made.append("log_statement (reset to default)")
            
            cursor.execute("ALTER SYSTEM RESET log_duration;")
            changes_made.append("log_duration (reset to default)")
            
            cursor.execute("ALTER SYSTEM RESET log_line_prefix;")
            changes_made.append("log_line_prefix (reset to default)")
            
            cursor.execute("SELECT pg_reload_conf();")
            
            cursor.close()
            
            message = "Logging settings reset to defaults. Changes:\n" + "\n".join(f"  • {c}" for c in changes_made)
            
            return True, message
            
        except psycopg2.Error as e:
            return False, f"Failed to reset logging: {str(e)}"
    
    def enable_pg_stat_statements(self) -> Tuple[bool, str]:
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT * FROM pg_extension WHERE extname = 'pg_stat_statements';")
            if cursor.fetchone():
                cursor.close()
                return True, "pg_stat_statements is already enabled"
            
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_stat_statements;")
            cursor.close()
            
            return True, "pg_stat_statements extension enabled successfully"
            
        except psycopg2.Error as e:
            error_msg = str(e)
            if "shared_preload_libraries" in error_msg:
                return False, (
                    "pg_stat_statements requires configuration in postgresql.conf:\n"
                    "Add 'pg_stat_statements' to shared_preload_libraries and restart PostgreSQL"
                )
            return False, f"Failed to enable pg_stat_statements: {error_msg}"
    
    def get_recent_queries(self, limit: int = 50) -> list:
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT 
                    query,
                    calls,
                    total_exec_time,
                    mean_exec_time,
                    max_exec_time
                FROM pg_stat_statements
                ORDER BY last_exec_time DESC
                LIMIT %s;
            """, (limit,))
            
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except psycopg2.Error:
            return []
    
    def test_superuser_access(self) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT current_setting('is_superuser');")
            result = cursor.fetchone()
            cursor.close()
            return result and result[0] == 'on'
        except:
            return False
