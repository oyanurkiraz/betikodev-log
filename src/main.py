# src/main.py
import argparse #Komut satırından gelen argümanları okumak için
import sys #Programdan kontrollü çıkmak için (sys.exit)
from src.fetcher import fetch_posts
from src.log_generator import create_logs
from src.report import analyze_logs

def main():
    parser = argparse.ArgumentParser(description="Log Analiz Aracı CLI")
    
    parser.add_argument("--fetch", action="store_true", help="API'den postları çek ve raw_posts.json'a kaydet.")
    #action="store_true" -> flag mantığı
    parser.add_argument("--generate", action="store_true", help="raw_posts.json'dan sentetik log üret.")
    parser.add_argument("--analyze", action="store_true", help="Logları analiz et ve raporları oluştur (CSV/JSON).")

    args = parser.parse_args() #Komut satırından gelenleri oku

    # Eğer hiç argüman verilmediyse help göster
    if not (args.fetch or args.generate or args.analyze):
        parser.print_help()
        sys.exit(1)

    if args.fetch:
        print("--- Veri Çekme İşlemi Başlıyor ---")
        fetch_posts()
        print("-" * 30)

    if args.generate:
        print("--- Log Üretme İşlemi Başlıyor ---")
        create_logs()
        print("-" * 30)

    if args.analyze:
        print("--- Analiz İşlemi Başlıyor ---")
        analyze_logs()
        print("-" * 30)

if __name__ == "__main__":
    main()