from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QComboBox, QSplitter,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCursor
from src.database import EchoDatabase
import json
import markdown
import html


class AIWorker(QThread):
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, provider: str, api_key: str, model: str, messages: list):
        super().__init__()
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.messages = messages
        
    def run(self):
        try:
            if self.provider == "OpenAI":
                response = self.call_openai()
            elif self.provider == "Claude (Anthropic)":
                response = self.call_claude()
            elif self.provider == "DeepSeek":
                response = self.call_deepseek()
            else:
                response = "Unknown provider"
            
            self.response_ready.emit(response)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def call_openai(self):
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": self.messages,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except ImportError:
            return "Error: 'requests' library not installed. Run: pip install requests"
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"
    
    def call_claude(self):
        try:
            import requests
            
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            
            system_message = ""
            user_messages = []
            
            for msg in self.messages:
                if msg['role'] == 'system':
                    system_message = msg['content']
                else:
                    user_messages.append(msg)
            
            data = {
                "model": self.model,
                "max_tokens": 4096,
                "messages": user_messages
            }
            
            if system_message:
                data["system"] = system_message
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except ImportError:
            return "Error: 'requests' library not installed. Run: pip install requests"
        except Exception as e:
            return f"Error calling Claude: {str(e)}"
    
    def call_deepseek(self):
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": self.messages,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except ImportError:
            return "Error: 'requests' library not installed. Run: pip install requests"
        except Exception as e:
            return f"Error calling DeepSeek: {str(e)}"


class AIChatPanel(QWidget):
    def __init__(self, log_content: str = "", parent=None):
        super().__init__(parent)
        self.log_content = log_content
        self.db = EchoDatabase()
        self.conversation_history = []
        self.ai_worker = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🤖 AI Log Analyzer")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2196F3; padding: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.provider_label = QLabel("Provider: Not configured")
        self.provider_label.setStyleSheet("color: #666; padding: 10px;")
        header_layout.addWidget(self.provider_label)
        
        config_btn = QPushButton("⚙️ Configure AI")
        config_btn.clicked.connect(self.open_ai_config)
        config_btn.setStyleSheet("background-color: #607D8B; color: white; padding: 8px;")
        header_layout.addWidget(config_btn)
        
        layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1E1E1E;
            }
        """)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(12)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll_area.setWidget(self.chat_container)
        layout.addWidget(scroll_area)
        
        suggestions_layout = QHBoxLayout()
        suggestions_label = QLabel("💡 Quick questions:")
        suggestions_label.setStyleSheet("color: #9CA3AF; font-size: 10px;")
        suggestions_layout.addWidget(suggestions_label)
        
        self.suggestion_btns = []
        suggestions = [
            "Summarize errors",
            "Find slow queries",
            "Analyze patterns"
        ]
        
        for suggestion in suggestions:
            btn = QPushButton(suggestion)
            btn.clicked.connect(lambda checked, s=suggestion: self.use_suggestion(s))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #374151;
                    color: #60A5FA;
                    border: 1px solid #3B82F6;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #4B5563;
                }
            """)
            suggestions_layout.addWidget(btn)
            self.suggestion_btns.append(btn)
        
        suggestions_layout.addStretch()
        layout.addLayout(suggestions_layout)
        
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask anything about your logs...")
        self.input_field.setFont(QFont("Arial", 11))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #3B82F6;
                border-radius: 8px;
                background-color: #374151;
                color: #E5E7EB;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        input_layout.addWidget(self.send_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_chat)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        input_layout.addWidget(clear_btn)
        
        layout.addLayout(input_layout)
        
        self.update_provider_label()
        self.add_welcome_message()
        
    def update_provider_label(self):
        provider = self.db.get_app_setting('ai_provider', 'Not configured')
        if provider == "OpenAI":
            model = self.db.get_app_setting('openai_model', 'gpt-4o-mini')
        elif provider == "Claude (Anthropic)":
            model = self.db.get_app_setting('claude_model', 'claude-3-5-sonnet-20241022')
        elif provider == "DeepSeek":
            model = self.db.get_app_setting('deepseek_model', 'deepseek-chat')
        else:
            model = "N/A"
        
        self.provider_label.setText(f"Provider: {provider} ({model})")
        
    def add_welcome_message(self):
        welcome = (
            "👋 **Welcome to AI Log Analyzer!**\n\n"
            "I can help you analyze your PostgreSQL logs. Ask me questions like:\n\n"
            "• What errors occurred in the last hour?\n"
            "• Which queries are taking the longest?\n"
            "• Are there any unusual patterns?\n"
            "• Summarize the main issues\n\n"
            "Configure your AI provider in the settings to get started."
        )
        self.add_message('system', welcome)
        
    def open_ai_config(self):
        from src.ai_config_dialog import AIConfigDialog
        dialog = AIConfigDialog(self)
        if dialog.exec():
            self.update_provider_label()
            
    def use_suggestion(self, suggestion: str):
        self.input_field.setText(suggestion)
        self.send_message()
    
    def add_message(self, role: str, content: str, show_actions: bool = False):
        message_frame = QFrame()
        message_frame.setStyleSheet(\"\"\"\n            QFrame {\n                background-color: transparent;\n                border: none;\n            }\n        \"\"\")\n        message_layout = QVBoxLayout(message_frame)\n        message_layout.setContentsMargins(0, 0, 0, 0)\n        message_layout.setSpacing(5)\n        \n        if role == 'user':\n            bubble_color = '#3B82F6'\n            text_color = 'white'\n            icon = '👤'\n            align = Qt.AlignmentFlag.AlignRight\n        elif role == 'assistant':\n            bubble_color = '#10B981'\n            text_color = 'white'\n            icon = '🤖'\n            align = Qt.AlignmentFlag.AlignLeft\n        elif role == 'system':\n            bubble_color = '#2C3E50'\n            text_color = '#ECF0F1'\n            icon = '💡'\n            align = Qt.AlignmentFlag.AlignLeft\n        else:\n            bubble_color = '#EF4444'\n            text_color = 'white'\n            icon = '❌'\n            align = Qt.AlignmentFlag.AlignLeft\n        \n        content_html = markdown.markdown(\n            content,\n            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']\n        )\n        \n        bubble = QTextEdit()\n        bubble.setReadOnly(True)\n        bubble.setHtml(f\"\"\"\n            <div style='font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, sans-serif;'>\n                <div style='margin-bottom: 8px;'>\n                    <span style='font-weight: bold; color: {text_color};'>{icon} {role.title()}</span>\n                </div>\n                <div style='color: {text_color}; line-height: 1.6;'>\n                    {content_html}\n                </div>\n            </div>\n        \"\"\")\n        bubble.setStyleSheet(f\"\"\"\n            QTextEdit {{\n                background-color: {bubble_color};\n                border: none;\n                border-radius: 12px;\n                padding: 12px 16px;\n                max-width: 80%;\n            }}\n        \"\"\")\n        bubble.setMaximumWidth(int(self.width() * 0.8))\n        bubble.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)\n        bubble.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)\n        \n        doc_height = bubble.document().size().height()\n        bubble.setFixedHeight(int(doc_height) + 20)\n        \n        bubble_container = QHBoxLayout()\n        if align == Qt.AlignmentFlag.AlignRight:\n            bubble_container.addStretch()\n        bubble_container.addWidget(bubble)\n        if align == Qt.AlignmentFlag.AlignLeft:\n            bubble_container.addStretch()\n        \n        message_layout.addLayout(bubble_container)\n        \n        if show_actions and role == 'assistant':\n            actions_layout = QHBoxLayout()\n            if align == Qt.AlignmentFlag.AlignLeft:\n                actions_layout.addSpacing(20)\n            else:\n                actions_layout.addStretch()\n            \n            copy_btn = QPushButton(\"📋 Copy\")\n            copy_btn.clicked.connect(lambda: self.copy_message(content))\n            copy_btn.setStyleSheet(\"\"\"\n                QPushButton {\n                    background-color: transparent;\n                    color: #9CA3AF;\n                    border: 1px solid #4B5563;\n                    border-radius: 4px;\n                    padding: 4px 8px;\n                    font-size: 10px;\n                }\n                QPushButton:hover {\n                    background-color: #374151;\n                    color: #E5E7EB;\n                }\n            \"\"\")\n            actions_layout.addWidget(copy_btn)\n            \n            if align == Qt.AlignmentFlag.AlignRight:\n                actions_layout.addSpacing(20)\n            else:\n                actions_layout.addStretch()\n            \n            message_layout.addLayout(actions_layout)\n        \n        self.chat_layout.addWidget(message_frame)\n        \n        QTimer.singleShot(100, self.scroll_to_bottom)\n    \n    def copy_message(self, content: str):\n        from PyQt6.QtWidgets import QApplication\n        clipboard = QApplication.clipboard()\n        clipboard.setText(content)\n        \n    def scroll_to_bottom(self):\n        scroll_area = self.chat_container.parent().parent()\n        if isinstance(scroll_area, QScrollArea):\n            scroll_area.verticalScrollBar().setValue(\n                scroll_area.verticalScrollBar().maximum()\n            )
        
    def send_message(self):
        user_message = self.input_field.text().strip()
        if not user_message:
            return
        
        provider = self.db.get_app_setting('ai_provider')
        if not provider or provider == "Not configured":
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "AI Not Configured",
                "Please configure your AI provider first by clicking '⚙️ Configure AI'."
            )
            return
        
        if provider == "OpenAI":
            api_key = self.db.get_app_setting('openai_api_key')
            model = self.db.get_app_setting('openai_model', 'gpt-4o-mini')
        elif provider == "Claude (Anthropic)":
            api_key = self.db.get_app_setting('claude_api_key')
            model = self.db.get_app_setting('claude_model', 'claude-3-5-sonnet-20241022')
        else:
            api_key = self.db.get_app_setting('deepseek_api_key')
            model = self.db.get_app_setting('deepseek_model', 'deepseek-chat')
    def update_log_content(self, log_content: str):
        self.log_content = log_content
        self.conversation_history = []
