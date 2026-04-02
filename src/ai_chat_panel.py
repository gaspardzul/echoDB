from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QScrollArea, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextOption
from src.database import EchoDatabase
import markdown
import html as html_module


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
        
        title_label = QLabel("🤖 Analizador de Logs con IA")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2196F3; padding: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.provider_label = QLabel("Proveedor: No configurado")
        self.provider_label.setStyleSheet("color: #9CA3AF; padding: 10px;")
        header_layout.addWidget(self.provider_label)
        
        config_btn = QPushButton("⚙️ Configurar IA")
        config_btn.clicked.connect(self.open_ai_config)
        config_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        header_layout.addWidget(config_btn)
        
        layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #0D1117;
            }
            QScrollBar:vertical {
                background-color: #161B22;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #30363D;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #484F58;
            }
        """)
        
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: #0D1117;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(12, 12, 12, 12)
        
        scroll_area.setWidget(self.chat_container)
        self.scroll_area = scroll_area
        layout.addWidget(scroll_area)
        
        suggestions_layout = QHBoxLayout()
        suggestions_label = QLabel("💡 Preguntas rápidas:")
        suggestions_label.setStyleSheet("color: #9CA3AF; font-size: 11px; font-weight: 500;")
        suggestions_layout.addWidget(suggestions_label)
        
        suggestions = [
            "Resumir errores",
            "Encontrar queries lentas",
            "Analizar patrones"
        ]
        
        for suggestion in suggestions:
            btn = QPushButton(suggestion)
            btn.clicked.connect(lambda checked, s=suggestion: self.use_suggestion(s))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #374151;
                    color: #60A5FA;
                    border: 1px solid #3B82F6;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #4B5563;
                    border-color: #60A5FA;
                }
            """)
            suggestions_layout.addWidget(btn)
        
        suggestions_layout.addStretch()
        layout.addLayout(suggestions_layout)
        
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Pregunta cualquier cosa sobre tus logs...")
        self.input_field.setFont(QFont("Arial", 12))
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #3B82F6;
                border-radius: 10px;
                background-color: #374151;
                color: #E5E7EB;
                font-size: 12px;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
            }
            QLineEdit:focus {
                border-color: #60A5FA;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Enviar")
        self.send_btn.clicked.connect(self.send_message)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 10px;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:disabled {
                background-color: #6B7280;
            }
        """)
        input_layout.addWidget(self.send_btn)
        
        clear_btn = QPushButton("Limpiar")
        clear_btn.clicked.connect(self.clear_chat)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                padding: 12px 20px;
                border-radius: 10px;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4B5563;
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
        
        self.provider_label.setText(f"Proveedor: {provider} • {model}")
        
    def add_welcome_message(self):
        welcome = """👋 **¡Bienvenido al Analizador de Logs con IA!**

Puedo ayudarte a analizar tus logs de PostgreSQL. Pregúntame cosas como:

• ¿Qué errores ocurrieron en la última hora?
• ¿Qué queries están tardando más?
• ¿Hay patrones inusuales?
• Resume los problemas principales

Configura tu proveedor de IA en la configuración para comenzar."""
        
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
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(4)
        
        if role == 'user':
            prefix = '> '
            color = '#60A5FA'
            bg_color = '#1E293B'
        elif role == 'assistant':
            prefix = '$ '
            color = '#10B981'
            bg_color = '#0F1419'
        elif role == 'system':
            prefix = '# '
            color = '#F59E0B'
            bg_color = '#1E1E1E'
        else:
            prefix = '! '
            color = '#EF4444'
            bg_color = '#1E1E1E'
        
        header_label = QLabel(f"{prefix}{role.upper()}")
        header_label.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        header_label.setStyleSheet(f"color: {color}; padding: 8px 12px 4px 12px;")
        
        content_html = markdown.markdown(
            content,
            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']
        )
        
        content_label = QLabel()
        content_label.setTextFormat(Qt.TextFormat.RichText)
        content_label.setWordWrap(True)
        content_label.setText(f"""
            <div style='font-family: "Courier New", Monaco, monospace; font-size: 13px; color: #F1F5F9; line-height: 1.6;'>
                {content_html}
            </div>
        """)
        content_label.setStyleSheet("padding: 4px 12px 8px 32px;")
        
        message_frame = QFrame()
        message_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-left: 4px solid {color};
                border-radius: 6px;
                margin: 4px 0px;
            }}
        """)
        
        frame_layout = QVBoxLayout(message_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        frame_layout.addWidget(header_label)
        frame_layout.addWidget(content_label)
        
        container_layout.addWidget(message_frame)
        
        if show_actions and role == 'assistant':
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            copy_btn = QPushButton("📋 Copiar")
            copy_btn.clicked.connect(lambda: self.copy_message(content))
            copy_btn.setStyleSheet("""
                QPushButton {
                    background-color: #374151;
                    color: #9CA3AF;
                    border: 1px solid #4B5563;
                    border-radius: 4px;
                    padding: 4px 10px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #4B5563;
                    color: #E5E7EB;
                }
            """)
            actions_layout.addWidget(copy_btn)
            actions_layout.addStretch()
            
            container_layout.addLayout(actions_layout)
        
        self.chat_layout.addWidget(container)
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def copy_message(self, content: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(content)
        
    def scroll_to_bottom(self):
        if hasattr(self, 'scroll_area'):
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
    
    def send_message(self):
        user_message = self.input_field.text().strip()
        if not user_message:
            return
        
        provider = self.db.get_app_setting('ai_provider')
        if not provider or provider == "Not configured":
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "IA No Configurada",
                "Por favor configura tu proveedor de IA primero haciendo clic en '⚙️ Configurar IA'."
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
        
        if not api_key:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Sin API Key",
                f"Por favor configura tu API key de {provider} primero."
            )
            return
        
        self.add_message('user', user_message)
        self.input_field.clear()
        self.send_btn.setEnabled(False)
        self.input_field.setEnabled(False)
        
        if not self.conversation_history:
            system_message = {
                "role": "system",
                "content": f"Eres un administrador experto de bases de datos PostgreSQL analizando archivos de log. Aquí están los logs recientes:\n\n{self.log_content[:8000]}\n\nAyuda al usuario a entender y analizar estos logs. También conoces sobre AWS, Huawei Cloud y Microsoft Azure. Formatea tus respuestas usando Markdown para mejor legibilidad. Usa bloques de código para queries SQL, viñetas para listas, y negritas para términos importantes. IMPORTANTE: Responde siempre en español."
            }
            self.conversation_history.append(system_message)
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        self.add_message('system', '🤔 Pensando...')
        
        self.ai_worker = AIWorker(provider, api_key, model, self.conversation_history)
        self.ai_worker.response_ready.connect(self.on_response_ready)
        self.ai_worker.error_occurred.connect(self.on_error)
        self.ai_worker.start()
        
    def on_response_ready(self, response: str):
        if self.chat_layout.count() > 0:
            last_widget = self.chat_layout.itemAt(self.chat_layout.count() - 1).widget()
            if last_widget:
                last_widget.deleteLater()
        
        self.add_message('assistant', response, show_actions=True)
        
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        self.send_btn.setEnabled(True)
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        
    def on_error(self, error: str):
        if self.chat_layout.count() > 0:
            last_widget = self.chat_layout.itemAt(self.chat_layout.count() - 1).widget()
            if last_widget:
                last_widget.deleteLater()
        
        self.add_message('error', f"**Error:** {error}")
        
        self.send_btn.setEnabled(True)
        self.input_field.setEnabled(True)
        
    def clear_chat(self):
        while self.chat_layout.count():
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.conversation_history = []
        self.add_welcome_message()
        
    def update_log_content(self, log_content: str):
        self.log_content = log_content
        self.conversation_history = []
