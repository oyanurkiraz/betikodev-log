# src/parser.py
import re
import os
from datetime import datetime
from src.models import LogRecord

LOG_FILE_PATH = os.path.join("data", "app.log")

# Regex Açıklaması:
# Tarih: \[(?P<timestamp>.*?)\] -> [2025-12-09 14:23:15] kısmını alır
# Seviye: (?P<level>\w+) -> INFO, WARNING vs alır
# UserID: \(user_id=(?P<user_id>\d+) -> user_id=12 kısmından 12'yi alır
# PostID: post_id=(?P<post_id>\d+)\) -> post_id=34 kısmından 34'ü alır
# Mesaj: : (?P<message>.*) -> geri kalan metni alır
LOG_PATTERN = re.compile(
    r"\[(?P<timestamp>.*?)\] (?P<level>\w+) \(user_id=(?P<user_id>\d+), post_id=(?P<post_id>\d+)\): (?P<message>.*)"
)

def parse_log_line(line: str) -> LogRecord | None:
    match = LOG_PATTERN.search(line)
    if not match:
        return None
    
    data = match.groupdict()
    
    try:
        dt = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        return LogRecord(
            timestamp=dt,
            level=data["level"],
            user_id=int(data["user_id"]),
            post_id=int(data["post_id"]),
            message=data["message"]
        )
    except Exception:
        return None

def load_logs() -> list[LogRecord]:
    if not os.path.exists(LOG_FILE_PATH):
        print("Log dosyası bulunamadı.")
        return []

    records = []
    with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            record = parse_log_line(line)
            if record:
                records.append(record)
    return records