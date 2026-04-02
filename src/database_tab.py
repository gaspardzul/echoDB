from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTextEdit, QLabel,
    QCheckBox, QGroupBox, QSplitter, QDialog, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFont
from src.log_reader import LogReader
from src.log_parser import LogParser
from src.syntax_highlighter import SQLSyntaxHighlighter
from src.tab_settings_dialog import TabSettingsDialog
from src.ai_chat_panel import AIChatPanel


class DatabaseTab(QWidget):
    name_changed = pyqtSignal(str)
    
    def __init__(self, connection_name: str, log_path: str = "", parent=None):
        super().__init__(parent)
        self.connection_name = connection_name
        self.log_reader = None
        self.log_parser = LogParser()
        self.filter_text = ""
        self.auto_scroll = True
        self.show_only_queries = False
        self.log_path = log_path
        self.font_size = 10
        self.db_filter = None
        self.detected_databases = set()
        
        self.init_ui()
        
        if log_path:
            self.path_input.setText(log_path)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        path_label = QLabel("Ruta del Log:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Ruta al archivo de log de PostgreSQL")
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input, 1)
        
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ Iniciar")
        self.start_btn.clicked.connect(self.start_monitoring)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        
        self.stop_btn = QPushButton("⏸ Detener")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            QPushButton:disabled {
                background-color: #9CA3AF;
            }
        """)
        
        clear_btn = QPushButton("🗑 Limpiar")
        clear_btn.clicked.connect(self.clear_log_display)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #F59E0B;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #D97706;
            }
        """)
        
        settings_btn = QPushButton("⚙️ Configuración")
        settings_btn.clicked.connect(self.open_settings)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        settings_btn.setToolTip("Editar configuración del tab")
        
        self.disable_logging_btn = QPushButton("🔴 Desactivar Logging BD")
        self.disable_logging_btn.clicked.connect(self.quick_disable_logging)
        self.disable_logging_btn.setStyleSheet("""
            QPushButton {
                background-color: #EC4899;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #DB2777;
            }
        """)
        self.disable_logging_btn.setToolTip("Desactivar rápidamente el logging de PostgreSQL para detener el crecimiento del log")
        
        ai_chat_btn = QPushButton("🤖 Chat de IA")
        ai_chat_btn.clicked.connect(self.open_ai_chat)
        ai_chat_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        ai_chat_btn.setToolTip("Pregunta a la IA sobre tus logs")
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(self.disable_logging_btn)
        button_layout.addWidget(ai_chat_btn)
        button_layout.addWidget(settings_btn)
        
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtro:")
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Buscar por nombre de tabla, palabra clave, etc.")
        self.filter_input.textChanged.connect(self.on_filter_changed)
        
        db_filter_label = QLabel("BD:")
        self.db_filter_combo = QComboBox()
        self.db_filter_combo.addItem("Todas las BDs")
        self.db_filter_combo.currentTextChanged.connect(self.on_db_filter_changed)
        self.db_filter_combo.setMinimumWidth(150)
        
        self.queries_only_checkbox = QCheckBox("Solo Queries")
        self.queries_only_checkbox.stateChanged.connect(self.on_queries_only_changed)
        
        self.auto_scroll_checkbox = QCheckBox("Auto-desplazar")
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.stateChanged.connect(self.on_auto_scroll_changed)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input, 1)
        filter_layout.addWidget(db_filter_label)
        filter_layout.addWidget(self.db_filter_combo)
        filter_layout.addWidget(self.queries_only_checkbox)
        filter_layout.addWidget(self.auto_scroll_checkbox)
        
        controls_layout.addLayout(path_layout)
        controls_layout.addLayout(button_layout)
        controls_layout.addLayout(filter_layout)
        controls_group.setLayout(controls_layout)
        
        layout.addWidget(controls_group)
        
        log_label = QLabel(f"Logs: {self.connection_name}")
        log_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(log_label)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Courier New", 10))
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 2px solid #3E3E3E;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        self.highlighter = SQLSyntaxHighlighter(self.log_display.document())
        
        layout.addWidget(self.log_display, 1)
        
        self.status_label = QLabel("Listo")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.status_label)
    
    def get_file_size(self, file_path: str) -> str:
        try:
            size_bytes = Path(file_path).stat().st_size
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.2f} KB"
            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
        except:
            return "N/A"
    
    def start_monitoring(self):
        log_path = self.path_input.text().strip()
        
        if not log_path:
            self.status_label.setText("Error: Por favor selecciona un archivo de log")
            self.status_label.setStyleSheet("color: #f44336; font-size: 11px;")
            return
            
        if not Path(log_path).exists():
            self.status_label.setText(f"Error: Archivo de log no encontrado")
            self.status_label.setStyleSheet("color: #f44336; font-size: 11px;")
            return
        
        if self.log_reader and self.log_reader.isRunning():
            self.log_reader.stop()
        
        self.log_reader = LogReader(log_path)
        self.log_reader.new_line.connect(self.on_new_log_line)
        self.log_reader.error_occurred.connect(self.on_reader_error)
        self.log_reader.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.path_input.setEnabled(False)
        
        file_size = self.get_file_size(log_path)
        self.status_label.setText(f"Monitoreando: {Path(log_path).name} | Tamaño: {file_size}")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
        
    def stop_monitoring(self):
        if self.log_reader:
            self.log_reader.stop()
            
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.path_input.setEnabled(True)
        self.status_label.setText("Monitoreo detenido")
        self.status_label.setStyleSheet("color: #FF9800; font-size: 11px;")
    
    @pyqtSlot(str)
    def on_new_log_line(self, line: str):
        entry = self.log_parser.parse_line(line)
        
        if not entry:
            return
        
        # Detectar y agregar nuevas bases de datos al combo
        if entry.database and entry.database not in self.detected_databases:
            self.detected_databases.add(entry.database)
            self.db_filter_combo.addItem(entry.database)
            
        if self.show_only_queries and not entry.is_query():
            return
        
        # Filtro por base de datos
        if self.db_filter and entry.database != self.db_filter:
            return
        
        if self.filter_text and self.filter_text.lower() not in entry.message.lower():
            return
        
        display_text = entry.raw_line
        if entry.parameters:
            display_text += f"\n    {entry.parameters}"
        
        self.log_display.append(display_text)
        
        if self.auto_scroll:
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    @pyqtSlot(str)
    def on_reader_error(self, error_message: str):
        self.status_label.setText(f"Error: {error_message}")
        self.status_label.setStyleSheet("color: #f44336; font-size: 11px;")
        self.log_display.append(f"\n[ERROR] {error_message}\n")
        self.stop_monitoring()
    
    def on_filter_changed(self, text: str):
        self.filter_text = text
    
    def on_queries_only_changed(self, state):
        self.show_only_queries = state == Qt.CheckState.Checked.value
    
    def on_auto_scroll_changed(self, state):
        self.auto_scroll = state == Qt.CheckState.Checked.value
    
    def on_db_filter_changed(self, db_name: str):
        if db_name == "Todas las BDs":
            self.db_filter = None
        else:
            self.db_filter = db_name
    
    def clear_log_display(self):
        self.log_display.clear()
        self.status_label.setText("Log display cleared")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")
    
    def cleanup(self):
        if self.log_reader and self.log_reader.isRunning():
            self.log_reader.stop()
    
    def is_monitoring(self) -> bool:
        return self.log_reader is not None and self.log_reader.isRunning()
    
    def open_settings(self):
        current_settings = {
            'name': self.connection_name,
            'log_path': self.path_input.text(),
            'auto_scroll': self.auto_scroll,
            'queries_only': self.show_only_queries,
            'font_size': self.font_size,
            'filter_text': self.filter_text
        }
        
        dialog = TabSettingsDialog(current_settings, self)
        dialog.settings_updated.connect(self.apply_settings)
        dialog.exec()
    
    @pyqtSlot(dict)
    def apply_settings(self, settings: dict):
        new_name = settings.get('name', self.connection_name)
        if new_name and new_name != self.connection_name:
            self.connection_name = new_name
            self.name_changed.emit(new_name)
        
        new_path = settings.get('log_path', '')
        if new_path != self.path_input.text():
            self.path_input.setText(new_path)
        
        self.auto_scroll = settings.get('auto_scroll', True)
        self.auto_scroll_checkbox.setChecked(self.auto_scroll)
        
        self.show_only_queries = settings.get('queries_only', False)
        self.queries_only_checkbox.setChecked(self.show_only_queries)
        
        new_font_size = settings.get('font_size', 10)
        if new_font_size != self.font_size:
            self.font_size = new_font_size
            font = self.log_display.font()
            font.setPointSize(new_font_size)
            self.log_display.setFont(font)
        
        new_filter = settings.get('filter_text', '')
        if new_filter != self.filter_text:
            self.filter_input.setText(new_filter)
        
        self.status_label.setText("Settings updated")
        self.status_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
    
    def get_settings(self) -> dict:
        return {
            'name': self.connection_name,
            'log_path': self.path_input.text(),
            'auto_scroll': self.auto_scroll,
            'queries_only': self.show_only_queries,
            'font_size': self.font_size,
            'filter_text': self.filter_text
        }
    
    def quick_disable_logging(self):
        from PyQt6.QtWidgets import QMessageBox, QInputDialog
        from src.db_connector import PostgreSQLConnector
        
        reply = QMessageBox.question(
            self,
            "Disable PostgreSQL Logging",
            "⚠️ This will disable logging in PostgreSQL to prevent log file growth.\n\n"
            "You'll need to provide database credentials.\n\n"
            "Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        host, ok = QInputDialog.getText(self, "Database Host", "Host:", text="localhost")
        if not ok:
            return
        
        port, ok = QInputDialog.getInt(self, "Database Port", "Port:", 5432, 1, 65535)
        if not ok:
            return
        
        database, ok = QInputDialog.getText(self, "Database Name", "Database:", text="postgres")
        if not ok:
            return
        
        user, ok = QInputDialog.getText(self, "Database User", "User:", text="postgres")
        if not ok:
            return
        
        from PyQt6.QtWidgets import QLineEdit
        password_dialog = QInputDialog(self)
        password_dialog.setWindowTitle("Database Password")
        password_dialog.setLabelText("Password:")
        password_dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        
        if not password_dialog.exec():
            return
        
        password = password_dialog.textValue()
        
        connector = PostgreSQLConnector()
        success, message = connector.connect(host, port, database, user, password)
        
        if not success:
            QMessageBox.critical(self, "Connection Failed", f"Failed to connect:\n{message}")
            return
        
        success, result = connector.disable_logging()
        connector.disconnect()
        
        if success:
            QMessageBox.information(
                self,
                "Logging Disabled",
                f"✅ PostgreSQL logging has been disabled successfully!\n\n{result}\n\n"
                "Log file will stop growing now."
            )
            self.status_label.setText("✅ DB Logging disabled")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 11px;")
        else:
            QMessageBox.critical(self, "Failed", f"Failed to disable logging:\n{result}")
    
    def open_ai_chat(self):
        log_content = self.log_display.toPlainText()
        
        if not log_content.strip():
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "No Logs",
                "No logs available yet. Start monitoring first to collect logs."
            )
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"AI Chat - {self.connection_name}")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(0, 0, 0, 0)
        
        ai_panel = AIChatPanel(log_content, dialog)
        layout.addWidget(ai_panel)
        
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("background-color: #757575; color: white; padding: 8px; margin: 10px;")
        layout.addWidget(close_btn)
        
        dialog.exec()
