# src/report.py
import csv
import json
import os
from collections import Counter, defaultdict
from src.parser import load_logs

REPORT_DIR = "reports"
CSV_PATH = os.path.join(REPORT_DIR, "summary.csv")
JSON_PATH = os.path.join(REPORT_DIR, "summary.json")

def analyze_logs():
    records = load_logs()
    if not records:
        print("Analiz edilecek log kaydı yok.")
        return

    # 1. İstatistikleri Hesapla
    total_logs = len(records)
    level_counts = Counter(r.level for r in records)
    
    # Kullanıcı bazlı istatistikler
    user_stats = defaultdict(lambda: {"total": 0, "errors": 0})
    error_messages = []

    for r in records:
        user_stats[str(r.user_id)]["total"] += 1
        if r.is_error:
            user_stats[str(r.user_id)]["errors"] += 1
            error_messages.append(r.message)

    # En uzun 5 hata mesajı
    top_error_messages = sorted(error_messages, key=len, reverse=True)[:5]

    # Klasörü oluştur
    os.makedirs(REPORT_DIR, exist_ok=True)

    # --- CSV OLUŞTURMA ---
    try:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["level", "count"])
            for level, count in level_counts.items():
                writer.writerow([level, count])
        print(f"CSV Raporu oluşturuldu: {CSV_PATH}")
    except Exception as e:
        print(f"CSV yazma hatası: {e}")

    # --- JSON OLUŞTURMA ---
    report_data = {
        "total_logs": total_logs,
        "by_level": dict(level_counts),
        "by_user": dict(user_stats),
        "top_error_messages": top_error_messages
    }

    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        print(f"JSON Raporu oluşturuldu: {JSON_PATH}")
    except Exception as e:
        print(f"JSON yazma hatası: {e}")