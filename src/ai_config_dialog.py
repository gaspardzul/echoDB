from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QGroupBox, QComboBox,
    QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.database import EchoDatabase


class AIConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = EchoDatabase()
        self.init_ui()
        self.load_current_config()
        
    def init_ui(self):
        self.setWindowTitle("AI Configuration")
        self.setModal(True)
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(
            "🤖 Configure AI providers to analyze your PostgreSQL logs.\n"
            "Your API keys are stored securely in your local database."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                background-color: #1E293B;
                padding: 15px;
                border-radius: 8px;
                color: #E5E7EB;
            }
        """)
        layout.addWidget(info_label)
        
        provider_group = QGroupBox("AI Provider")
        provider_layout = QVBoxLayout()
        
        provider_select_layout = QHBoxLayout()
        provider_select_layout.addWidget(QLabel("Select Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "Claude (Anthropic)", "DeepSeek"])
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        provider_select_layout.addWidget(self.provider_combo)
        provider_layout.addLayout(provider_select_layout)
        
        provider_group.setLayout(provider_layout)
        layout.addWidget(provider_group)
        
        self.openai_group = QGroupBox("OpenAI Configuration")
        openai_layout = QVBoxLayout()
        
        openai_key_layout = QHBoxLayout()
        openai_key_layout.addWidget(QLabel("API Key:"))
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setPlaceholderText("sk-...")
        openai_key_layout.addWidget(self.openai_key_input)
        openai_layout.addLayout(openai_key_layout)
        
        openai_model_layout = QHBoxLayout()
        openai_model_layout.addWidget(QLabel("Model:"))
        self.openai_model_combo = QComboBox()
        self.openai_model_combo.addItems(["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"])
        openai_model_layout.addWidget(self.openai_model_combo)
        openai_layout.addLayout(openai_model_layout)
        
        openai_info = QLabel("Get your API key at: https://platform.openai.com/api-keys")
        openai_info.setStyleSheet("color: #666; font-size: 10px;")
        openai_layout.addWidget(openai_info)
        
        self.openai_group.setLayout(openai_layout)
        layout.addWidget(self.openai_group)
        
        self.claude_group = QGroupBox("Claude (Anthropic) Configuration")
        claude_layout = QVBoxLayout()
        
        claude_key_layout = QHBoxLayout()
        claude_key_layout.addWidget(QLabel("API Key:"))
        self.claude_key_input = QLineEdit()
        self.claude_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.claude_key_input.setPlaceholderText("sk-ant-...")
        claude_key_layout.addWidget(self.claude_key_input)
        claude_layout.addLayout(claude_key_layout)
        
        claude_model_layout = QHBoxLayout()
        claude_model_layout.addWidget(QLabel("Model:"))
        self.claude_model_combo = QComboBox()
        self.claude_model_combo.addItems(["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"])
        claude_model_layout.addWidget(self.claude_model_combo)
        claude_layout.addLayout(claude_model_layout)
        
        claude_info = QLabel("Get your API key at: https://console.anthropic.com/")
        claude_info.setStyleSheet("color: #666; font-size: 10px;")
        claude_layout.addWidget(claude_info)
        
        self.claude_group.setLayout(claude_layout)
        layout.addWidget(self.claude_group)
        
        self.deepseek_group = QGroupBox("DeepSeek Configuration")
        deepseek_layout = QVBoxLayout()
        
        deepseek_key_layout = QHBoxLayout()
        deepseek_key_layout.addWidget(QLabel("API Key:"))
        self.deepseek_key_input = QLineEdit()
        self.deepseek_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.deepseek_key_input.setPlaceholderText("sk-...")
        deepseek_key_layout.addWidget(self.deepseek_key_input)
        deepseek_layout.addLayout(deepseek_key_layout)
        
        deepseek_model_layout = QHBoxLayout()
        deepseek_model_layout.addWidget(QLabel("Model:"))
        self.deepseek_model_combo = QComboBox()
        self.deepseek_model_combo.addItems(["deepseek-chat", "deepseek-coder"])
        deepseek_model_layout.addWidget(self.deepseek_model_combo)
        deepseek_layout.addLayout(deepseek_model_layout)
        
        deepseek_info = QLabel("Get your API key at: https://platform.deepseek.com/")
        deepseek_info.setStyleSheet("color: #666; font-size: 10px;")
        deepseek_layout.addWidget(deepseek_info)
        
        self.deepseek_group.setLayout(deepseek_layout)
        layout.addWidget(self.deepseek_group)
        
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("🧪 Test Connection")
        test_btn.clicked.connect(self.test_connection)
        test_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        button_layout.addWidget(test_btn)
        
        save_btn = QPushButton("💾 Save Configuration")
        save_btn.clicked.connect(self.save_config)
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #757575; color: white; padding: 8px;")
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.on_provider_changed(self.provider_combo.currentText())
        
    def on_provider_changed(self, provider: str):
        self.openai_group.setVisible(provider == "OpenAI")
        self.claude_group.setVisible(provider == "Claude (Anthropic)")
        self.deepseek_group.setVisible(provider == "DeepSeek")
        
    def load_current_config(self):
        provider = self.db.get_app_setting('ai_provider', 'OpenAI')
        self.provider_combo.setCurrentText(provider)
        
        openai_key = self.db.get_app_setting('openai_api_key', '')
        openai_model = self.db.get_app_setting('openai_model', 'gpt-4o-mini')
        self.openai_key_input.setText(openai_key)
        self.openai_model_combo.setCurrentText(openai_model)
        
        claude_key = self.db.get_app_setting('claude_api_key', '')
        claude_model = self.db.get_app_setting('claude_model', 'claude-3-5-sonnet-20241022')
        self.claude_key_input.setText(claude_key)
        self.claude_model_combo.setCurrentText(claude_model)
        
        deepseek_key = self.db.get_app_setting('deepseek_api_key', '')
        deepseek_model = self.db.get_app_setting('deepseek_model', 'deepseek-chat')
        self.deepseek_key_input.setText(deepseek_key)
        self.deepseek_model_combo.setCurrentText(deepseek_model)
        
    def save_config(self):
        provider = self.provider_combo.currentText()
        self.db.save_app_setting('ai_provider', provider)
        
        self.db.save_app_setting('openai_api_key', self.openai_key_input.text())
        self.db.save_app_setting('openai_model', self.openai_model_combo.currentText())
        
        self.db.save_app_setting('claude_api_key', self.claude_key_input.text())
        self.db.save_app_setting('claude_model', self.claude_model_combo.currentText())
        
        self.db.save_app_setting('deepseek_api_key', self.deepseek_key_input.text())
        self.db.save_app_setting('deepseek_model', self.deepseek_model_combo.currentText())
        
        QMessageBox.information(
            self,
            "Configuration Saved",
            f"✅ AI configuration saved successfully!\n\nProvider: {provider}"
        )
        
        self.accept()
        
    def test_connection(self):
        provider = self.provider_combo.currentText()
        
        if provider == "OpenAI":
            api_key = self.openai_key_input.text()
            model = self.openai_model_combo.currentText()
        elif provider == "Claude (Anthropic)":
            api_key = self.claude_key_input.text()
            model = self.claude_model_combo.currentText()
        else:
            api_key = self.deepseek_key_input.text()
            model = self.deepseek_model_combo.currentText()
        
        if not api_key:
            QMessageBox.warning(self, "No API Key", "Please enter an API key first.")
            return
        
        QMessageBox.information(
            self,
            "Test Connection",
            f"🧪 Testing connection to {provider}...\n\n"
            f"Model: {model}\n\n"
            "Note: Full API testing will be implemented in the AI chat panel."
        )
