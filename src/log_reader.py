import time
from pathlib import Path
from typing import Optional, Callable
from PyQt6.QtCore import QThread, pyqtSignal


class LogReader(QThread):
    new_line = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, log_path: str):
        super().__init__()
        self.log_path = Path(log_path)
        self.running = False
        self.file_position = 0
        
    def run(self):
        self.running = True
        
        if not self.log_path.exists():
            self.error_occurred.emit(f"Log file not found: {self.log_path}")
            return
            
        try:
            with open(self.log_path, 'r', encoding='utf-8', errors='replace') as file:
                file.seek(0, 2)
                self.file_position = file.tell()
                
                while self.running:
                    current_position = file.tell()
                    line = file.readline()
                    
                    if line:
                        self.new_line.emit(line.rstrip('\n'))
                    else:
                        file.seek(current_position)
                        time.sleep(0.1)
                        
                        if self.log_path.stat().st_size < current_position:
                            file.seek(0)
                            self.file_position = 0
                            
        except Exception as e:
            self.error_occurred.emit(f"Error reading log file: {str(e)}")
            
    def stop(self):
        self.running = False
        self.wait()
