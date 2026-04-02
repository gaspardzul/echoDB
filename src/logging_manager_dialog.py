from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QGroupBox, QTextEdit,
    QSpinBox, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.db_connector import PostgreSQLConnector


class LoggingManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = PostgreSQLConnector()
        self.init_ui()
        self.load_default_values()
        
    def init_ui(self):
        self.setWindowTitle("PostgreSQL Logging Manager")
        self.setModal(True)
        self.setMinimumWidth(650)
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(
            "⚙️ Gestiona la configuración de logging de PostgreSQL.\n"
            "Puedes activar, desactivar o restaurar los valores por defecto."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background-color: #1E293B; color: #E5E7EB; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)
        
        conn_group = QGroupBox("Database Connection")
        conn_layout = QVBoxLayout()
        
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("localhost")
        host_layout.addWidget(self.host_input)
        conn_layout.addLayout(host_layout)
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(5432)
        port_layout.addWidget(self.port_input)
        conn_layout.addLayout(port_layout)
        
        db_layout = QHBoxLayout()
        db_layout.addWidget(QLabel("Database:"))
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText("postgres")
        db_layout.addWidget(self.database_input)
        conn_layout.addLayout(db_layout)
        
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("User:"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("postgres")
        user_layout.addWidget(self.user_input)
        conn_layout.addLayout(user_layout)
        
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password")
        pass_layout.addWidget(self.password_input)
        conn_layout.addLayout(pass_layout)
        
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)
        
        action_group = QGroupBox("Logging Action")
        action_layout = QVBoxLayout()
        
        self.action_button_group = QButtonGroup()
        
        self.enable_radio = QRadioButton("✅ Enable Full Logging")
        self.enable_radio.setToolTip("Configura PostgreSQL para registrar todas las queries y sus parámetros")
        self.action_button_group.addButton(self.enable_radio, 1)
        action_layout.addWidget(self.enable_radio)
        
        enable_desc = QLabel("   • log_min_duration_statement = 0\n   • log_statement = 'all'\n   • log_duration = 'on'")
        enable_desc.setStyleSheet("color: #666; font-size: 11px; margin-left: 20px;")
        action_layout.addWidget(enable_desc)
        
        self.disable_radio = QRadioButton("❌ Disable Logging")
        self.disable_radio.setToolTip("Desactiva el logging de queries en PostgreSQL")
        self.action_button_group.addButton(self.disable_radio, 2)
        action_layout.addWidget(self.disable_radio)
        
        disable_desc = QLabel("   • log_min_duration_statement = -1\n   • log_statement = 'none'\n   • log_duration = 'off'")
        disable_desc.setStyleSheet("color: #666; font-size: 11px; margin-left: 20px;")
        action_layout.addWidget(disable_desc)
        
        self.reset_radio = QRadioButton("🔄 Reset to Defaults")
        self.reset_radio.setToolTip("Restaura la configuración de logging a los valores por defecto de PostgreSQL")
        self.action_button_group.addButton(self.reset_radio, 3)
        action_layout.addWidget(self.reset_radio)
        
        reset_desc = QLabel("   • Restaura todos los parámetros de logging a sus valores por defecto")
        reset_desc.setStyleSheet("color: #666; font-size: 11px; margin-left: 20px;")
        action_layout.addWidget(reset_desc)
        
        self.enable_radio.setChecked(True)
        
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        current_group = QGroupBox("Current Settings")
        current_layout = QVBoxLayout()
        
        self.current_settings_text = QTextEdit()
        self.current_settings_text.setReadOnly(True)
        self.current_settings_text.setMaximumHeight(100)
        self.current_settings_text.setFont(QFont("Courier New", 9))
        self.current_settings_text.setStyleSheet("""
            QTextEdit {
                background-color: #2B2B2B;
                color: #E0E0E0;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        self.current_settings_text.setPlaceholderText("Connect to see current settings...")
        current_layout.addWidget(self.current_settings_text)
        
        current_group.setLayout(current_layout)
        layout.addWidget(current_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(120)
        self.status_text.setFont(QFont("Courier New", 9))
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #2B2B2B;
                color: #E0E0E0;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_text)
        
        button_layout = QHBoxLayout()
        
        check_btn = QPushButton("🔍 Check Current Settings")
        check_btn.clicked.connect(self.check_current_settings)
        check_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        button_layout.addWidget(check_btn)
        
        apply_btn = QPushButton("✅ Apply Changes")
        apply_btn.clicked.connect(self.apply_changes)
        apply_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(apply_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #757575; color: white; padding: 8px;")
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def load_default_values(self):
        self.host_input.setText("localhost")
        self.port_input.setValue(5432)
        self.database_input.setText("postgres")
        self.user_input.setText("postgres")
        
    def get_connection_params(self):
        return {
            'host': self.host_input.text().strip() or 'localhost',
            'port': self.port_input.value(),
            'database': self.database_input.text().strip() or 'postgres',
            'user': self.user_input.text().strip() or 'postgres',
            'password': self.password_input.text()
        }
    
    def check_current_settings(self):
        self.status_text.clear()
        self.current_settings_text.clear()
        self.status_text.append("🔍 Checking current settings...")
        
        params = self.get_connection_params()
        success, message = self.connector.connect(**params)
        
        if not success:
            self.status_text.append("❌ " + message)
            return
        
        self.status_text.append("✅ Connected to PostgreSQL\n")
        
        settings = self.connector.get_current_log_settings()
        
        if 'error' in settings:
            self.status_text.append(f"❌ Error: {settings['error']}")
        else:
            self.current_settings_text.clear()
            for key, value in settings.items():
                self.current_settings_text.append(f"{key}: {value}")
            
            self.status_text.append("✅ Current settings loaded successfully")
        
        self.connector.disconnect()
    
    def apply_changes(self):
        self.status_text.clear()
        self.status_text.append("🚀 Applying changes...\n")
        
        params = self.get_connection_params()
        success, message = self.connector.connect(**params)
        
        if not success:
            self.status_text.append("❌ " + message)
            QMessageBox.critical(self, "Connection Failed", message)
            return
        
        self.status_text.append("✅ Connected to PostgreSQL\n")
        
        is_superuser = self.connector.test_superuser_access()
        if not is_superuser:
            self.status_text.append("⚠️  Warning: User does not have superuser privileges")
            reply = QMessageBox.question(
                self,
                "Insufficient Privileges",
                "The user does not have superuser privileges.\nSome operations may fail.\n\nContinue anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                self.connector.disconnect()
                return
        
        selected_action = self.action_button_group.checkedId()
        
        if selected_action == 1:
            self.status_text.append("⚙️  Enabling full logging...")
            success, result_message = self.connector.configure_logging()
        elif selected_action == 2:
            self.status_text.append("⚙️  Disabling logging...")
            success, result_message = self.connector.disable_logging()
        elif selected_action == 3:
            self.status_text.append("⚙️  Resetting to defaults...")
            success, result_message = self.connector.reset_logging_to_defaults()
        else:
            success = False
            result_message = "No action selected"
        
        self.status_text.append(result_message + "\n")
        
        if success:
            self.status_text.append("✅ Changes applied successfully!")
            QMessageBox.information(
                self,
                "Success",
                "Logging configuration updated successfully.\n\n"
                "The changes have been applied to PostgreSQL."
            )
            
            self.check_current_settings()
        else:
            QMessageBox.critical(self, "Error", result_message)
        
        self.connector.disconnect()
    
    def closeEvent(self, event):
        if self.connector and self.connector.is_connected():
            self.connector.disconnect()
        event.accept()
