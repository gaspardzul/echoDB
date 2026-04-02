from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class WelcomeWidget(QWidget):
    add_connection_clicked = pyqtSignal()
    auto_setup_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel("👋 Bienvenido a EchoDB")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2196F3; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        subtitle_label = QLabel("PostgreSQL Real-time Logger")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #9CA3AF; margin-bottom: 30px;")
        layout.addWidget(subtitle_label)
        
        info_label = QLabel(
            "No tienes conexiones configuradas aún.\n\n"
            "Para comenzar a monitorear logs de PostgreSQL,\n"
            "necesitas agregar tu primera conexión."
        )
        info_label.setFont(QFont("Arial", 12))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                color: #E5E7EB;
                background-color: #1E293B;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 50px;
            }
        """)
        layout.addWidget(info_label)
        
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        auto_setup_btn = QPushButton("🔧 Auto-Setup (Recomendado)")
        auto_setup_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        auto_setup_btn.setMinimumWidth(300)
        auto_setup_btn.setMinimumHeight(50)
        auto_setup_btn.clicked.connect(self.auto_setup_clicked.emit)
        auto_setup_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        auto_setup_btn.setToolTip("Conecta a PostgreSQL y configura automáticamente el logging")
        buttons_layout.addWidget(auto_setup_btn)
        
        auto_setup_desc = QLabel("Configura automáticamente PostgreSQL y crea tu primera conexión")
        auto_setup_desc.setFont(QFont("Arial", 10))
        auto_setup_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        auto_setup_desc.setStyleSheet("color: #666; margin-bottom: 20px;")
        buttons_layout.addWidget(auto_setup_desc)
        
        manual_btn = QPushButton("➕ Agregar Conexión Manual")
        manual_btn.setFont(QFont("Arial", 12))
        manual_btn.setMinimumWidth(300)
        manual_btn.setMinimumHeight(50)
        manual_btn.clicked.connect(self.add_connection_clicked.emit)
        manual_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        manual_btn.setToolTip("Agrega una conexión especificando la ruta del log manualmente")
        buttons_layout.addWidget(manual_btn)
        
        manual_desc = QLabel("Especifica manualmente la ruta del archivo de log")
        manual_desc.setFont(QFont("Arial", 10))
        manual_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        manual_desc.setStyleSheet("color: #666;")
        buttons_layout.addWidget(manual_desc)
        
        layout.addLayout(buttons_layout)
        
        layout.addStretch()
        
        tips_label = QLabel(
            "💡 Tip: Puedes agregar múltiples conexiones para monitorear\n"
            "diferentes bases de datos simultáneamente usando tabs."
        )
        tips_label.setFont(QFont("Arial", 10))
        tips_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tips_label.setStyleSheet("""
            QLabel {
                color: #666;
                background-color: #E3F2FD;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 100px;
            }
        """)
        layout.addWidget(tips_label)
