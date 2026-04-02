import re
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class LogEntry:
    timestamp: Optional[datetime]
    log_type: str
    message: str
    raw_line: str
    parameters: Optional[str] = None
    database: Optional[str] = None
    user: Optional[str] = None
    
    def is_query(self) -> bool:
        return 'execute' in self.message.lower() or 'select' in self.message.lower() or \
               'insert' in self.message.lower() or 'update' in self.message.lower() or \
               'delete' in self.message.lower()
    
    def is_detail(self) -> bool:
        return self.log_type == 'DETAIL'


class LogParser:
    TIMESTAMP_PATTERN = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})'
    LOG_TYPE_PATTERN = r'\[(.*?)\]\s+(LOG|DETAIL|ERROR|WARNING|INFO|STATEMENT):\s+'
    # Patrón para extraer usuario y BD del formato: [usuario]@[basedatos]
    DB_USER_PATTERN_1 = r'\[(\w+)\]@\[(\w+)\]'
    # Patrón alternativo para connection: database=X user=Y
    DB_USER_PATTERN_2 = r'database=(\w+)\s+user=(\w+)'
    # Patrón para connection received
    CONNECTION_PATTERN = r'connection received:.*database=(\w+)\s+user=(\w+)'
    
    def __init__(self):
        self.last_entry: Optional[LogEntry] = None
        self.current_database: Optional[str] = None
        self.current_user: Optional[str] = None
        
    def parse_line(self, line: str) -> Optional[LogEntry]:
        if not line.strip():
            return None
            
        timestamp = self._extract_timestamp(line)
        log_type = self._extract_log_type(line)
        message = self._extract_message(line)
        database, user = self._extract_db_and_user(line)
        
        entry = LogEntry(
            timestamp=timestamp,
            log_type=log_type,
            message=message,
            raw_line=line,
            database=database,
            user=user
        )
        
        if entry.is_detail() and self.last_entry and self.last_entry.is_query():
            self.last_entry.parameters = message
            return None
        
        self.last_entry = entry
        return entry
    
    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        match = re.search(self.TIMESTAMP_PATTERN, line)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                return None
        return None
    
    def _extract_log_type(self, line: str) -> str:
        match = re.search(self.LOG_TYPE_PATTERN, line)
        if match:
            return match.group(2)
        return 'UNKNOWN'
    
    def _extract_message(self, line: str) -> str:
        match = re.search(self.LOG_TYPE_PATTERN, line)
        if match:
            return line[match.end():].strip()
        return line.strip()
    
    def _extract_db_and_user(self, line: str) -> tuple[Optional[str], Optional[str]]:
        # Intentar patrón 1: [usuario]@[basedatos]
        match = re.search(self.DB_USER_PATTERN_1, line)
        if match:
            user = match.group(1)
            database = match.group(2)
            self.current_database = database
            self.current_user = user
            return database, user
        
        # Intentar patrón 2: database=X user=Y
        match = re.search(self.DB_USER_PATTERN_2, line)
        if match:
            database = match.group(1)
            user = match.group(2)
            self.current_database = database
            self.current_user = user
            return database, user
        
        # Intentar patrón 3: connection received
        match = re.search(self.CONNECTION_PATTERN, line)
        if match:
            database = match.group(1)
            user = match.group(2)
            self.current_database = database
            self.current_user = user
            return database, user
        
        # Si no encontramos en esta línea, usar el último conocido
        return self.current_database, self.current_user
