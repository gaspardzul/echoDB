from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTextEdit, QLabel,
    QFileDialog, QStatusBar, QCheckBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QAction
from src.log_reader import LogReader
from src.log_parser import LogParser
from src.syntax_highlighter import SQLSyntaxHighlighter
from src.connection_dialog import ConnectionDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_reader = None
        self.log_parser = LogParser()
        self.filter_text = ""
        self.auto_scroll = True
        self.show_only_queries = False
        
        self.init_ui()
        self.load_default_log_path()
        
    def init_ui(self):
        self.setWindowTitle("EchoDB - PostgreSQL Real-time Logger")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        path_label = QLabel("Log Path:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("/Users/gaspardzul/Library/Application Support/Postgres/var-16/postgresql.log")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_log_file)
        
        setup_btn = QPushButton("🔧 Auto-Setup")
        setup_btn.clicked.connect(self.open_connection_dialog)
        setup_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; padding: 8px;")
        setup_btn.setToolTip("Connect to PostgreSQL and auto-configure logging")
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(browse_btn)
        path_layout.addWidget(setup_btn)
        
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start Monitoring")
        self.start_btn.clicked.connect(self.start_monitoring)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        
        self.stop_btn = QPushButton("⏸ Stop Monitoring")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 8px;")
        
        clear_btn = QPushButton("🗑 Clear")
        clear_btn.clicked.connect(self.clear_log_display)
        clear_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 8px;")
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(clear_btn)
        
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter:")
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Search by table name, keyword, etc. (e.g., 'timerecord', 'SELECT')")
        self.filter_input.textChanged.connect(self.on_filter_changed)
        
        self.queries_only_checkbox = QCheckBox("Show Queries Only")
        self.queries_only_checkbox.stateChanged.connect(self.on_queries_only_changed)
        
        self.auto_scroll_checkbox = QCheckBox("Auto-scroll")
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.stateChanged.connect(self.on_auto_scroll_changed)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input, 1)
        filter_layout.addWidget(self.queries_only_checkbox)
        filter_layout.addWidget(self.auto_scroll_checkbox)
        
        controls_layout.addLayout(path_layout)
        controls_layout.addLayout(button_layout)
        controls_layout.addLayout(filter_layout)
        controls_group.setLayout(controls_layout)
        
        main_layout.addWidget(controls_group)
        
        log_label = QLabel("PostgreSQL Logs (Real-time):")
        log_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(log_label)
        
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
        
        main_layout.addWidget(self.log_display, 1)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Select a log file and click 'Start Monitoring'")
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open Log File", self)
        open_action.triggered.connect(self.browse_log_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        database_menu = menubar.addMenu("Database")
        
        setup_action = QAction("Auto-Setup PostgreSQL Logging", self)
        setup_action.triggered.connect(self.open_connection_dialog)
        database_menu.addAction(setup_action)
        
    def load_default_log_path(self):
        default_path = Path.home() / "Library" / "Application Support" / "Postgres" / "var-16" / "postgresql.log"
        if default_path.exists():
            self.path_input.setText(str(default_path))
        
    def browse_log_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PostgreSQL Log File",
            str(Path.home()),
            "Log Files (*.log);;All Files (*)"
        )
        if file_path:
            self.path_input.setText(file_path)
    
    def open_connection_dialog(self):
        dialog = ConnectionDialog(self)
        dialog.connection_established.connect(self.on_connection_established)
        dialog.exec()
    
    @pyqtSlot(object, str)
    def on_connection_established(self, connector, log_path):
        if log_path:
            self.path_input.setText(log_path)
            self.status_bar.showMessage("PostgreSQL configured successfully! Log path updated.", 5000)
        else:
            self.status_bar.showMessage("PostgreSQL configured. Please select log file manually.", 5000)
    
    def start_monitoring(self):
        log_path = self.path_input.text().strip()
        
        if not log_path:
            self.status_bar.showMessage("Error: Please select a log file", 5000)
            return
            
        if not Path(log_path).exists():
            self.status_bar.showMessage(f"Error: Log file not found: {log_path}", 5000)
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
        self.status_bar.showMessage(f"Monitoring: {log_path}")
        
    def stop_monitoring(self):
        if self.log_reader:
            self.log_reader.stop()
            
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.path_input.setEnabled(True)
        self.status_bar.showMessage("Monitoring stopped")
    
    @pyqtSlot(str)
    def on_new_log_line(self, line: str):
        entry = self.log_parser.parse_line(line)
        
        if not entry:
            return
            
        if self.show_only_queries and not entry.is_query():
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
        self.status_bar.showMessage(f"Error: {error_message}", 10000)
        self.log_display.append(f"\n[ERROR] {error_message}\n")
        self.stop_monitoring()
    
    def on_filter_changed(self, text: str):
        self.filter_text = text
    
    def on_queries_only_changed(self, state):
        self.show_only_queries = state == Qt.CheckState.Checked.value
    
    def on_auto_scroll_changed(self, state):
        self.auto_scroll = state == Qt.CheckState.Checked.value
    
    def clear_log_display(self):
        self.log_display.clear()
        self.status_bar.showMessage("Log display cleared", 3000)
    
    def closeEvent(self, event):
        if self.log_reader and self.log_reader.isRunning():
            self.log_reader.stop()
        event.accept()
