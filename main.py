import sys
from PyQt6.QtWidgets import QApplication
from src.main_window_tabs import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("EchoDB")
    app.setOrganizationName("EchoDB")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
