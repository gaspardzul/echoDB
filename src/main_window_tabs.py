from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTabWidget, QFileDialog, QStatusBar,
    QMessageBox, QInputDialog, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QAction
from src.database_tab import DatabaseTab
from src.connection_dialog import ConnectionDialog
from src.config_manager import ConfigManager
from src.logging_manager_dialog import LoggingManagerDialog
from src.welcome_widget import WelcomeWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = []
        self.config_manager = ConfigManager()
        self.init_ui()
        self.load_saved_tabs()
        
    def init_ui(self):
        self.setWindowTitle("EchoDB - Monitor de PostgreSQL en Tiempo Real")
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        add_tab_btn = QPushButton("➕ New Connection")
        add_tab_btn.clicked.connect(self.add_new_connection)
        add_tab_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B5CF6;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7C3AED;
            }
        """)
        add_tab_btn.setToolTip("Add a new database connection")
        
        auto_setup_btn = QPushButton("🔧 Auto-Setup")
        auto_setup_btn.clicked.connect(self.open_connection_dialog)
        auto_setup_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        auto_setup_btn.setToolTip("Connect to PostgreSQL and auto-configure logging")
        
        toolbar_layout.addWidget(add_tab_btn)
        toolbar_layout.addWidget(auto_setup_btn)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)
        
        self.stacked_widget = QStackedWidget()
        
        self.welcome_widget = WelcomeWidget()
        self.welcome_widget.add_connection_clicked.connect(self.add_new_connection)
        self.welcome_widget.auto_setup_clicked.connect(self.open_connection_dialog)
        self.stacked_widget.addWidget(self.welcome_widget)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3E3E3E;
                background: #2B2B2B;
            }
            QTabBar::tab {
                background: #3E3E3E;
                color: #D4D4D4;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2B2B2B;
                color: #FFFFFF;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #4E4E4E;
            }
        """)
        
        self.stacked_widget.addWidget(self.tab_widget)
        
        main_layout.addWidget(self.stacked_widget)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Add a new connection or use Auto-Setup")
        
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Archivo")
        
        new_tab_action = QAction("Nueva Pestaña de Conexión", self)
        new_tab_action.setShortcut("Ctrl+T")
        new_tab_action.triggered.connect(self.add_new_connection)
        file_menu.addAction(new_tab_action)
        
        open_action = QAction("Abrir Archivo de Log en Nueva Pestaña", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_log_file_in_new_tab)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        save_config_action = QAction("Guardar Configuración de Pestañas", self)
        save_config_action.setShortcut("Ctrl+S")
        save_config_action.triggered.connect(self.save_tabs_configuration)
        file_menu.addAction(save_config_action)
        
        file_menu.addSeparator()
        
        close_tab_action = QAction("Cerrar Pestaña Actual", self)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(self.close_current_tab)
        file_menu.addAction(close_tab_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Salir", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        database_menu = menubar.addMenu("Base de Datos")
        
        setup_action = QAction("Auto-Configurar Logging de PostgreSQL", self)
        setup_action.triggered.connect(self.open_connection_dialog)
        database_menu.addAction(setup_action)
        
        database_menu.addSeparator()
        
        monitor_action = QAction("🔍 Monitor de Base de Datos", self)
        monitor_action.triggered.connect(self.open_db_monitor)
        database_menu.addAction(monitor_action)
        
        manage_logging_action = QAction("Gestionar Logging de PostgreSQL", self)
        manage_logging_action.triggered.connect(self.open_logging_manager)
        database_menu.addAction(manage_logging_action)
        
        ai_menu = menubar.addMenu("AI")
        
        ai_config_action = QAction("Configurar Proveedores de IA", self)
        ai_config_action.triggered.connect(self.open_ai_config)
        ai_menu.addAction(ai_config_action)
        
        view_menu = menubar.addMenu("Ver")
        
        next_tab_action = QAction("Siguiente Pestaña", self)
        next_tab_action.setShortcut("Ctrl+Tab")
        next_tab_action.triggered.connect(self.next_tab)
        view_menu.addAction(next_tab_action)
        
        prev_tab_action = QAction("Pestaña Anterior", self)
        prev_tab_action.setShortcut("Ctrl+Shift+Tab")
        prev_tab_action.triggered.connect(self.previous_tab)
        view_menu.addAction(prev_tab_action)
        
    def load_saved_tabs(self):
        saved_tabs = self.config_manager.load_tabs_config()
        
        if saved_tabs:
            for tab_config in saved_tabs:
                self.create_tab_from_config(tab_config)
            self.stacked_widget.setCurrentWidget(self.tab_widget)
            self.status_bar.showMessage(f"Loaded {len(saved_tabs)} saved tab(s)", 3000)
        else:
            self.stacked_widget.setCurrentWidget(self.welcome_widget)
            self.status_bar.showMessage("Welcome! Add your first connection to get started")
    
    def add_default_tab(self):
        default_path = Path.home() / "Library" / "Application Support" / "Postgres" / "var-16" / "postgresql.log"
        log_path = str(default_path) if default_path.exists() else ""
        
        tab = DatabaseTab("Default Connection", log_path)
        tab.name_changed.connect(lambda name: self.update_tab_name(tab, name))
        self.tabs.append(tab)
        self.tab_widget.addTab(tab, "Default Connection")
    
    def create_tab_from_config(self, config: dict):
        name = config.get('name', 'Unnamed')
        log_path = config.get('log_path', '')
        
        tab = DatabaseTab(name, log_path)
        tab.name_changed.connect(lambda new_name: self.update_tab_name(tab, new_name))
        
        tab.auto_scroll = config.get('auto_scroll', True)
        tab.auto_scroll_checkbox.setChecked(tab.auto_scroll)
        
        tab.show_only_queries = config.get('queries_only', False)
        tab.queries_only_checkbox.setChecked(tab.show_only_queries)
        
        font_size = config.get('font_size', 10)
        tab.font_size = font_size
        font = tab.log_display.font()
        font.setPointSize(font_size)
        tab.log_display.setFont(font)
        
        filter_text = config.get('filter_text', '')
        if filter_text:
            tab.filter_input.setText(filter_text)
        
        self.tabs.append(tab)
        self.tab_widget.addTab(tab, name)
    
    def save_tabs_configuration(self):
        tabs_settings = []
        for tab in self.tabs:
            if isinstance(tab, DatabaseTab):
                tabs_settings.append(tab.get_settings())
        
        if self.config_manager.save_tabs_config(tabs_settings):
            self.status_bar.showMessage(f"Saved {len(tabs_settings)} tab(s) configuration", 3000)
            QMessageBox.information(
                self,
                "Configuration Saved",
                f"Successfully saved configuration for {len(tabs_settings)} tab(s).\n\n"
                f"Location: {self.config_manager.config_file}"
            )
        else:
            QMessageBox.warning(
                self,
                "Save Failed",
                "Failed to save tabs configuration."
            )
        
    def add_new_connection(self):
        name, ok = QInputDialog.getText(
            self,
            "New Connection",
            "Enter connection name:",
            text=f"Connection {len(self.tabs) + 1}"
        )
        
        if ok and name:
            tab = DatabaseTab(name)
            tab.name_changed.connect(lambda new_name: self.update_tab_name(tab, new_name))
            self.tabs.append(tab)
            index = self.tab_widget.addTab(tab, name)
            self.tab_widget.setCurrentIndex(index)
            
            if self.stacked_widget.currentWidget() == self.welcome_widget:
                self.stacked_widget.setCurrentWidget(self.tab_widget)
            
            self.status_bar.showMessage(f"Added new connection: {name}", 3000)
    
    def open_log_file_in_new_tab(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PostgreSQL Log File",
            str(Path.home()),
            "Log Files (*.log);;All Files (*)"
        )
        
        if file_path:
            name = Path(file_path).stem
            tab = DatabaseTab(name, file_path)
            tab.name_changed.connect(lambda new_name: self.update_tab_name(tab, new_name))
            self.tabs.append(tab)
            index = self.tab_widget.addTab(tab, name)
            self.tab_widget.setCurrentIndex(index)
            self.status_bar.showMessage(f"Opened log file: {name}", 3000)
    
    def open_connection_dialog(self):
        dialog = ConnectionDialog(self)
        dialog.connection_established.connect(self.on_connection_established)
        dialog.exec()
    
    def open_logging_manager(self):
        dialog = LoggingManagerDialog(self)
        dialog.exec()
    
    def open_ai_config(self):
        from src.ai_config_dialog import AIConfigDialog
        dialog = AIConfigDialog(self)
        dialog.exec()
    
    def open_db_monitor(self):
        from src.db_monitor_dialog import DBMonitorDialog
        dialog = DBMonitorDialog(self)
        dialog.show()
    
    @pyqtSlot(str, str)
    def on_connection_established(self, connection_name: str, log_path: str):
        tab = DatabaseTab(connection_name, log_path)
        tab.name_changed.connect(lambda name: self.update_tab_name(tab, name))
        self.tabs.append(tab)
        index = self.tab_widget.addTab(tab, connection_name)
        self.tab_widget.setCurrentIndex(index)
        
        if self.stacked_widget.currentWidget() == self.welcome_widget:
            self.stacked_widget.setCurrentWidget(self.tab_widget)
        
        self.status_bar.showMessage(f"Connected: {connection_name}", 5000)
    
    def close_tab(self, index: int):
        if self.tab_widget.count() <= 1:
            reply = QMessageBox.question(
                self,
                "Close Last Tab",
                "This is the last tab. Do you want to close it?\n\n"
                "You can add a new connection anytime.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                return
        
        tab = self.tab_widget.widget(index)
        if tab and isinstance(tab, DatabaseTab):
            if tab.is_monitoring():
                reply = QMessageBox.question(
                    self,
                    "Close Tab",
                    f"Tab '{tab.connection_name}' is currently monitoring.\n\nDo you want to close it?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    return
            
            tab.cleanup()
            self.tabs.remove(tab)
        
        self.tab_widget.removeTab(index)
        
        if self.tab_widget.count() == 0:
            self.stacked_widget.setCurrentWidget(self.welcome_widget)
            self.status_bar.showMessage("No connections. Add your first connection to get started")
        else:
            self.status_bar.showMessage("Tab closed", 2000)
    
    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)
    
    def next_tab(self):
        current = self.tab_widget.currentIndex()
        next_index = (current + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(next_index)
    
    def previous_tab(self):
        current = self.tab_widget.currentIndex()
        prev_index = (current - 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(prev_index)
    
    def update_tab_name(self, tab: DatabaseTab, new_name: str):
        index = self.tab_widget.indexOf(tab)
        if index >= 0:
            self.tab_widget.setTabText(index, new_name)
            self.status_bar.showMessage(f"Tab renamed to: {new_name}", 3000)
    
    def closeEvent(self, event):
        active_tabs = [tab for tab in self.tabs if tab.is_monitoring()]
        
        if active_tabs:
            reply = QMessageBox.question(
                self,
                "Exit Application",
                f"{len(active_tabs)} tab(s) are currently monitoring.\n\nDo you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        tabs_settings = []
        for tab in self.tabs:
            if isinstance(tab, DatabaseTab):
                tabs_settings.append(tab.get_settings())
        
        self.config_manager.save_tabs_config(tabs_settings)
        
        for tab in self.tabs:
            tab.cleanup()
        
        event.accept()
