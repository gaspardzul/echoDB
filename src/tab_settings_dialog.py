from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QGroupBox, QFileDialog,
    QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from pathlib import Path


class TabSettingsDialog(QDialog):
    settings_updated = pyqtSignal(dict)
    
    def __init__(self, current_settings: dict, parent=None):
        super().__init__(parent)
        self.current_settings = current_settings
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        self.setWindowTitle("Tab Settings")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Tab Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Connection name")
        name_layout.addWidget(self.name_input)
        general_layout.addLayout(name_layout)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Log Path:"))
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Path to PostgreSQL log file")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_log_file)
        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(browse_btn)
        general_layout.addLayout(path_layout)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        display_group = QGroupBox("Display Options")
        display_layout = QVBoxLayout()
        
        self.auto_scroll_check = QCheckBox("Auto-scroll to bottom")
        self.auto_scroll_check.setChecked(True)
        display_layout.addWidget(self.auto_scroll_check)
        
        self.queries_only_check = QCheckBox("Show queries only (hide other logs)")
        display_layout.addWidget(self.queries_only_check)
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 16)
        self.font_size_spin.setValue(10)
        self.font_size_spin.setSuffix(" pt")
        font_layout.addWidget(self.font_size_spin)
        font_layout.addStretch()
        display_layout.addLayout(font_layout)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        filter_group = QGroupBox("Default Filter")
        filter_layout = QVBoxLayout()
        
        filter_input_layout = QHBoxLayout()
        filter_input_layout.addWidget(QLabel("Filter Text:"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("e.g., table name, SELECT, ERROR")
        filter_input_layout.addWidget(self.filter_input)
        filter_layout.addLayout(filter_input_layout)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        info_label = QLabel(
            "💡 Tip: These settings will be applied to this tab only.\n"
            "You can change them anytime by clicking the ⚙️ button."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                background-color: #E3F2FD;
                padding: 10px;
                border-radius: 5px;
                color: #1976D2;
            }
        """)
        layout.addWidget(info_label)
        
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #757575; color: white; padding: 8px;")
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def load_settings(self):
        self.name_input.setText(self.current_settings.get('name', ''))
        self.path_input.setText(self.current_settings.get('log_path', ''))
        self.auto_scroll_check.setChecked(self.current_settings.get('auto_scroll', True))
        self.queries_only_check.setChecked(self.current_settings.get('queries_only', False))
        self.font_size_spin.setValue(self.current_settings.get('font_size', 10))
        self.filter_input.setText(self.current_settings.get('filter_text', ''))
        
    def browse_log_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PostgreSQL Log File",
            str(Path.home()),
            "Log Files (*.log);;All Files (*)"
        )
        if file_path:
            self.path_input.setText(file_path)
    
    def save_settings(self):
        settings = {
            'name': self.name_input.text().strip(),
            'log_path': self.path_input.text().strip(),
            'auto_scroll': self.auto_scroll_check.isChecked(),
            'queries_only': self.queries_only_check.isChecked(),
            'font_size': self.font_size_spin.value(),
            'filter_text': self.filter_input.text().strip()
        }
        
        self.settings_updated.emit(settings)
        self.accept()
