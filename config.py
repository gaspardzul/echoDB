from pathlib import Path


DEFAULT_LOG_PATH = Path.home() / "Library" / "Application Support" / "Postgres" / "var-16" / "postgresql.log"

WINDOW_TITLE = "EchoDB - PostgreSQL Real-time Logger"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

THEME = {
    "background": "#1E1E1E",
    "foreground": "#D4D4D4",
    "border": "#3E3E3E",
    "keyword": "#569CD6",
    "string": "#CE9178",
    "number": "#B5CEA8",
    "parameter": "#9CDCFE",
    "timestamp": "#808080",
    "log_type": "#4EC9B0",
    "error": "#F44747",
    "detail": "#DCDCAA"
}

FONT_FAMILY = "Courier New"
FONT_SIZE = 10

LOG_REFRESH_INTERVAL = 0.1
