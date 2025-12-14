# src/models.py
from datetime import datetime

class LogRecord:
    def __init__(self, timestamp: datetime, level: str, user_id: int, post_id: int, message: str):
        self.timestamp = timestamp
        self.level = level
        self.user_id = user_id
        self.post_id = post_id
        self.message = message

    @property
    def is_error(self) -> bool:
        """Log seviyesinin ERROR olup olmadığını döner."""
        return self.level == "ERROR"

    def __repr__(self):
        return f"<LogRecord level={self.level} user={self.user_id} msg='{self.message[:20]}...'>"

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message}"