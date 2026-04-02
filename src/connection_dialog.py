from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QGroupBox, QTextEdit,
    QSpinBox, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from src.db_connector import PostgreSQLConnector


class ConnectionDialog(QDialog):
    connection_established = pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = PostgreSQLConnector()
        self.log_path = None
        self.connection_name = ""
        self.init_ui()
        self.load_default_values()
        
    def init_ui(self):
        self.setWindowTitle("PostgreSQL Connection Setup")
        self.setModal(True)
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(
            "EchoDB se conectará a PostgreSQL para configurar automáticamente el logging.\n"
            "Necesitas credenciales con permisos de superusuario."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background-color: #1E293B; color: #E5E7EB; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)
        
        conn_group = QGroupBox("Database Connection")
        conn_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Connection Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Production, Development, Local")
        name_layout.addWidget(self.name_input)
        conn_layout.addLayout(name_layout)
        
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
        
        options_group = QGroupBox("Auto-Configuration Options")
        options_layout = QVBoxLayout()
        
        self.configure_logging_check = QCheckBox("Configure logging parameters (log_statement, log_min_duration, etc.)")
        self.configure_logging_check.setChecked(True)
        options_layout.addWidget(self.configure_logging_check)
        
        self.enable_pg_stat_check = QCheckBox("Enable pg_stat_statements extension (optional)")
        self.enable_pg_stat_check.setChecked(False)
        options_layout.addWidget(self.enable_pg_stat_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
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
        
        test_btn = QPushButton("Test Connection")
        test_btn.clicked.connect(self.test_connection)
        test_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        button_layout.addWidget(test_btn)
        
        connect_btn = QPushButton("Connect & Configure")
        connect_btn.clicked.connect(self.connect_and_configure)
        connect_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(connect_btn)
        
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
    
    def test_connection(self):
        self.status_text.clear()
        self.status_text.append("🔍 Testing connection...")
        
        params = self.get_connection_params()
        success, message = self.connector.connect(**params)
        
        if success:
            self.status_text.append("✅ " + message)
            
            is_superuser = self.connector.test_superuser_access()
            if is_superuser:
                self.status_text.append("✅ User has superuser privileges")
            else:
                self.status_text.append("⚠️  Warning: User does not have superuser privileges. Some configurations may fail.")
            
            settings = self.connector.get_current_log_settings()
            self.status_text.append("\n📋 Current logging settings:")
            for key, value in settings.items():
                self.status_text.append(f"  • {key}: {value}")
            
            self.connector.disconnect()
        else:
            self.status_text.append("❌ " + message)
    
    def connect_and_configure(self):
        self.status_text.clear()
        self.status_text.append("🚀 Starting connection and configuration...\n")
        
        params = self.get_connection_params()
        success, message = self.connector.connect(**params)
        
        if not success:
            self.status_text.append("❌ " + message)
            QMessageBox.critical(self, "Connection Failed", message)
            return
        
        self.status_text.append("✅ Connected to PostgreSQL\n")
        
        if self.configure_logging_check.isChecked():
            self.status_text.append("⚙️  Configuring logging parameters...")
            success, message = self.connector.configure_logging()
            self.status_text.append(message + "\n")
            
            if not success:
                QMessageBox.warning(self, "Configuration Warning", message)
        
        if self.enable_pg_stat_check.isChecked():
            self.status_text.append("⚙️  Enabling pg_stat_statements...")
            success, message = self.connector.enable_pg_stat_statements()
            self.status_text.append(message + "\n")
            
            if not success:
                QMessageBox.warning(self, "Extension Warning", message)
        
        log_dir = self.connector.get_log_directory()
        data_dir = self.connector.get_data_directory()
        
        if log_dir:
            self.status_text.append(f"📁 Log directory: {log_dir}")
            
            possible_log_files = [
                log_dir / "postgresql.log",
                log_dir / "postgresql-*.log",
            ]
            
            for log_file in possible_log_files:
                if '*' not in str(log_file):
                    if log_file.exists():
                        self.log_path = str(log_file)
                        self.status_text.append(f"✅ Found log file: {self.log_path}")
                        break
            
            if not self.log_path and data_dir:
                fallback_log = data_dir / "postgresql.log"
                if fallback_log.exists():
                    self.log_path = str(fallback_log)
                    self.status_text.append(f"✅ Found log file: {self.log_path}")
        
        if not self.log_path:
            self.status_text.append("\n⚠️  Could not automatically locate log file.")
            self.status_text.append("You may need to specify it manually after closing this dialog.")
            
            reply = QMessageBox.question(
                self,
                "Log File Not Found",
                "Could not automatically locate the PostgreSQL log file.\n\n"
                "Do you want to continue anyway? You can specify the log file path manually.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                self.connector.disconnect()
                return
        
        self.status_text.append("\n✅ Configuration complete!")
        
        connection_name = self.name_input.text().strip()
        if not connection_name:
            db_name = self.database_input.text().strip() or "postgres"
            host = self.host_input.text().strip() or "localhost"
            connection_name = f"{db_name}@{host}"
        
        self.connection_name = connection_name
        
        QMessageBox.information(
            self,
            "Success",
            "PostgreSQL has been configured for logging.\n\n"
            "You can now start monitoring logs in real-time."
        )
        
        self.connection_established.emit(connection_name, self.log_path or "")
        self.accept()
    
    def closeEvent(self, event):
        if self.connector and self.connector.is_connected():
            self.connector.disconnect()
        event.accept()
