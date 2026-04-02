from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QGroupBox, QGridLayout, QHeaderView,
    QWidget, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from src.db_connector import PostgreSQLConnector


class DBMonitorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connector = None
        self.auto_refresh = True
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Database Monitor")
        self.setModal(False)
        self.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("🔍 PostgreSQL Monitor")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2196F3; padding: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.status_label = QLabel("⚪ Not Connected")
        self.status_label.setStyleSheet("color: #9CA3AF; padding: 10px;")
        header_layout.addWidget(self.status_label)
        
        connect_btn = QPushButton("🔌 Connect")
        connect_btn.clicked.connect(self.connect_to_db)
        connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        header_layout.addWidget(connect_btn)
        
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3E3E3E;
                border-radius: 4px;
                background-color: #1E1E1E;
            }
            QTabBar::tab {
                background-color: #2C2C2C;
                color: #E0E0E0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3B82F6;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #374151;
            }
        """)
        
        # Tab 1: Overview
        self.overview_tab = self.create_overview_tab()
        self.tabs.addTab(self.overview_tab, "📊 Overview")
        
        # Tab 2: Active Queries
        self.queries_tab = self.create_queries_tab()
        self.tabs.addTab(self.queries_tab, "⚡ Active Queries")
        
        # Tab 3: Database Stats
        self.stats_tab = self.create_stats_tab()
        self.tabs.addTab(self.stats_tab, "📈 Database Stats")
        
        layout.addWidget(self.tabs)
        
        # Footer
        footer_layout = QHBoxLayout()
        
        self.auto_refresh_btn = QPushButton("🔄 Auto-Refresh: ON")
        self.auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
        self.auto_refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        footer_layout.addWidget(self.auto_refresh_btn)
        
        refresh_btn = QPushButton("🔃 Refresh Now")
        refresh_btn.clicked.connect(self.refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        footer_layout.addWidget(refresh_btn)
        
        footer_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
    def create_overview_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)
        
        # Connections Group
        conn_group = QGroupBox("🔗 Connections")
        conn_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3B82F6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                color: #E0E0E0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        conn_layout = QGridLayout()
        
        conn_layout.addWidget(QLabel("Active:"), 0, 0)
        self.active_conn_label = QLabel("0")
        self.active_conn_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.active_conn_label.setStyleSheet("color: #10B981;")
        conn_layout.addWidget(self.active_conn_label, 0, 1)
        
        conn_layout.addWidget(QLabel("Max:"), 0, 2)
        self.max_conn_label = QLabel("100")
        self.max_conn_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.max_conn_label.setStyleSheet("color: #9CA3AF;")
        conn_layout.addWidget(self.max_conn_label, 0, 3)
        
        self.conn_progress = QProgressBar()
        self.conn_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3E3E3E;
                border-radius: 5px;
                text-align: center;
                background-color: #2C2C2C;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #10B981;
                border-radius: 3px;
            }
        """)
        conn_layout.addWidget(self.conn_progress, 1, 0, 1, 4)
        
        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)
        
        # Performance Metrics
        perf_group = QGroupBox("⚡ Performance")
        perf_group.setStyleSheet(conn_group.styleSheet().replace("#3B82F6", "#10B981"))
        perf_layout = QGridLayout()
        
        perf_layout.addWidget(QLabel("TPS:"), 0, 0)
        self.tps_label = QLabel("0")
        self.tps_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.tps_label.setStyleSheet("color: #60A5FA;")
        perf_layout.addWidget(self.tps_label, 0, 1)
        
        perf_layout.addWidget(QLabel("Cache Hit Ratio:"), 0, 2)
        self.cache_label = QLabel("0%")
        self.cache_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.cache_label.setStyleSheet("color: #F59E0B;")
        perf_layout.addWidget(self.cache_label, 0, 3)
        
        perf_layout.addWidget(QLabel("Active Queries:"), 1, 0)
        self.active_queries_label = QLabel("0")
        self.active_queries_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.active_queries_label.setStyleSheet("color: #8B5CF6;")
        perf_layout.addWidget(self.active_queries_label, 1, 1)
        
        perf_layout.addWidget(QLabel("Locks:"), 1, 2)
        self.locks_label = QLabel("0")
        self.locks_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.locks_label.setStyleSheet("color: #EF4444;")
        perf_layout.addWidget(self.locks_label, 1, 3)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Database Size
        size_group = QGroupBox("💾 Database Size")
        size_group.setStyleSheet(conn_group.styleSheet().replace("#3B82F6", "#F59E0B"))
        size_layout = QVBoxLayout()
        
        self.db_size_label = QLabel("Total: 0 MB")
        self.db_size_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.db_size_label.setStyleSheet("color: #E0E0E0; padding: 10px;")
        size_layout.addWidget(self.db_size_label)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        layout.addStretch()
        
        return widget
        
    def create_queries_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Active queries running on the database:")
        info_label.setStyleSheet("color: #9CA3AF; padding: 10px;")
        layout.addWidget(info_label)
        
        self.queries_table = QTableWidget()
        self.queries_table.setColumnCount(6)
        self.queries_table.setHorizontalHeaderLabels([
            "PID", "User", "Database", "State", "Duration", "Query"
        ])
        self.queries_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.queries_table.setStyleSheet("""
            QTableWidget {
                background-color: #1E1E1E;
                color: #E0E0E0;
                gridline-color: #3E3E3E;
                border: 1px solid #3E3E3E;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #3B82F6;
            }
            QHeaderView::section {
                background-color: #2C2C2C;
                color: #E0E0E0;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.queries_table)
        
        btn_layout = QHBoxLayout()
        
        kill_btn = QPushButton("❌ Kill Selected Query")
        kill_btn.clicked.connect(self.kill_query)
        kill_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
        """)
        btn_layout.addWidget(kill_btn)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        return widget
        
    def create_stats_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Database statistics and information:")
        info_label.setStyleSheet("color: #9CA3AF; padding: 10px;")
        layout.addWidget(info_label)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(4)
        self.stats_table.setHorizontalHeaderLabels([
            "Database", "Size", "Tables", "Connections"
        ])
        self.stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stats_table.setStyleSheet(self.queries_table.styleSheet())
        layout.addWidget(self.stats_table)
        
        return widget
        
    def connect_to_db(self):
        from PyQt6.QtWidgets import QInputDialog, QLineEdit, QMessageBox
        
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
        
        password_dialog = QInputDialog(self)
        password_dialog.setWindowTitle("Database Password")
        password_dialog.setLabelText("Password:")
        password_dialog.setTextEchoMode(QLineEdit.EchoMode.Password)
        
        if not password_dialog.exec():
            return
        
        password = password_dialog.textValue()
        
        self.connector = PostgreSQLConnector()
        success, message = self.connector.connect(host, port, database, user, password)
        
        if success:
            self.status_label.setText("🟢 Connected")
            self.status_label.setStyleSheet("color: #10B981; padding: 10px;")
            self.refresh_data()
            if self.auto_refresh:
                self.refresh_timer.start(5000)  # Refresh every 5 seconds
        else:
            QMessageBox.critical(self, "Connection Failed", f"Failed to connect:\n{message}")
            
    def refresh_data(self):
        if not self.connector or not self.connector.connection:
            return
        
        try:
            cursor = self.connector.connection.cursor()
            
            # Get connections info
            cursor.execute("""
                SELECT count(*) as active, 
                       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max
                FROM pg_stat_activity 
                WHERE state != 'idle'
            """)
            row = cursor.fetchone()
            if row:
                active, max_conn = row
                self.active_conn_label.setText(str(active))
                self.max_conn_label.setText(str(max_conn))
                self.conn_progress.setMaximum(max_conn)
                self.conn_progress.setValue(active)
            
            # Get TPS (transactions per second)
            cursor.execute("""
                SELECT sum(xact_commit + xact_rollback) / 
                       GREATEST(EXTRACT(EPOCH FROM (now() - stats_reset)), 1) as tps
                FROM pg_stat_database
            """)
            row = cursor.fetchone()
            if row and row[0]:
                self.tps_label.setText(f"{int(row[0])}")
            
            # Get cache hit ratio
            cursor.execute("""
                SELECT round(100.0 * sum(blks_hit) / NULLIF(sum(blks_hit + blks_read), 0), 2) as cache_hit_ratio
                FROM pg_stat_database
            """)
            row = cursor.fetchone()
            if row and row[0]:
                self.cache_label.setText(f"{row[0]}%")
            
            # Get active queries count
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'")
            row = cursor.fetchone()
            if row:
                self.active_queries_label.setText(str(row[0]))
            
            # Get locks count
            cursor.execute("SELECT count(*) FROM pg_locks WHERE NOT granted")
            row = cursor.fetchone()
            if row:
                self.locks_label.setText(str(row[0]))
            
            # Get total database size
            cursor.execute("SELECT pg_size_pretty(sum(pg_database_size(datname))::bigint) FROM pg_database")
            row = cursor.fetchone()
            if row:
                self.db_size_label.setText(f"Total: {row[0]}")
            
            # Update active queries table
            self.update_queries_table(cursor)
            
            # Update stats table
            self.update_stats_table(cursor)
            
            cursor.close()
            
        except Exception as e:
            print(f"Error refreshing data: {e}")
            
    def update_queries_table(self, cursor):
        cursor.execute("""
            SELECT pid, usename, datname, state, 
                   EXTRACT(EPOCH FROM (now() - query_start))::int as duration,
                   LEFT(query, 100) as query
            FROM pg_stat_activity 
            WHERE state != 'idle' AND pid != pg_backend_pid()
            ORDER BY query_start
        """)
        
        rows = cursor.fetchall()
        self.queries_table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                if j == 4:  # Duration
                    value = f"{value}s"
                item = QTableWidgetItem(str(value) if value else "")
                self.queries_table.setItem(i, j, item)
                
    def update_stats_table(self, cursor):
        cursor.execute("""
            SELECT datname,
                   pg_size_pretty(pg_database_size(datname)) as size,
                   (SELECT count(*) FROM pg_tables WHERE schemaname = 'public') as tables,
                   numbackends
            FROM pg_stat_database
            WHERE datname NOT IN ('template0', 'template1')
            ORDER BY pg_database_size(datname) DESC
        """)
        
        rows = cursor.fetchall()
        self.stats_table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value else "0")
                self.stats_table.setItem(i, j, item)
                
    def toggle_auto_refresh(self):
        self.auto_refresh = not self.auto_refresh
        if self.auto_refresh:
            self.auto_refresh_btn.setText("🔄 Auto-Refresh: ON")
            self.auto_refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: #10B981;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #059669;
                }
            """)
            self.refresh_timer.start(5000)
        else:
            self.auto_refresh_btn.setText("🔄 Auto-Refresh: OFF")
            self.auto_refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6B7280;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #4B5563;
                }
            """)
            self.refresh_timer.stop()
            
    def kill_query(self):
        from PyQt6.QtWidgets import QMessageBox
        
        selected = self.queries_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a query to kill.")
            return
        
        row = selected[0].row()
        pid = self.queries_table.item(row, 0).text()
        
        reply = QMessageBox.question(
            self,
            "Kill Query",
            f"Are you sure you want to kill query with PID {pid}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connector.connection.cursor()
                cursor.execute(f"SELECT pg_terminate_backend({pid})")
                cursor.close()
                self.connector.connection.commit()
                QMessageBox.information(self, "Success", f"Query {pid} terminated.")
                self.refresh_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to kill query:\n{str(e)}")
                
    def closeEvent(self, event):
        self.refresh_timer.stop()
        if self.connector:
            self.connector.disconnect()
        event.accept()
