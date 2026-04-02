from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class SQLSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            "SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "JOIN",
            "LEFT", "RIGHT", "INNER", "OUTER", "ON", "AND", "OR", "NOT",
            "ORDER", "BY", "GROUP", "HAVING", "LIMIT", "OFFSET", "AS",
            "DISTINCT", "COUNT", "SUM", "AVG", "MAX", "MIN", "IN", "EXISTS",
            "BETWEEN", "LIKE", "IS", "NULL", "CREATE", "ALTER", "DROP",
            "TABLE", "INDEX", "VIEW", "EXECUTE", "SET", "CASE", "WHEN", "THEN",
            "ELSE", "END", "UNION", "ALL", "ASC", "DESC"
        ]
        
        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b", QRegularExpression.PatternOption.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, keyword_format))
        
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((QRegularExpression("'[^']*'"), string_format))
        
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))
        self.highlighting_rules.append((QRegularExpression("\\b[0-9]+\\b"), number_format))
        
        parameter_format = QTextCharFormat()
        parameter_format.setForeground(QColor("#9CDCFE"))
        parameter_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression("\\$[0-9]+"), parameter_format))
        
        timestamp_format = QTextCharFormat()
        timestamp_format.setForeground(QColor("#808080"))
        self.highlighting_rules.append((QRegularExpression("^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\\.\\d{3}"), timestamp_format))
        
        log_type_format = QTextCharFormat()
        log_type_format.setForeground(QColor("#4EC9B0"))
        log_type_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression("\\b(LOG|DETAIL|ERROR|WARNING|INFO)\\b"), log_type_format))
        
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("#F44747"))
        error_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression("\\bERROR\\b"), error_format))
        
        detail_format = QTextCharFormat()
        detail_format.setForeground(QColor("#DCDCAA"))
        self.highlighting_rules.append((QRegularExpression("parameters:.*"), detail_format))
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
