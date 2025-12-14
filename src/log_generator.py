# src/log_generator.py
import json #json dosyasından postları okumak için
import random #Log seviyesini rastgele seçmek için (INFO, WARNING, ERROR)
import os #Dosya yolu kontrolü, dosya var mı, path oluşturma
from datetime import datetime #Log satırına timestamp eklemek için

RAW_DATA_PATH = os.path.join("data", "raw_posts.json") #Fetcher'ın ürettiği ham post verileri
LOG_FILE_PATH = os.path.join("data", "app.log") #oluşturulacak log sayısı
LOG_LEVELS = ["INFO", "WARNING", "ERROR"] #gerçek uygulamalardaki klasik log seviyeleri

def generate_log_line(post: dict) -> str:
    """
    Bir post sözlüğünü alır ve formatlı log satırı döndürür.
    Format: [YYYY-MM-DD HH:MM:SS] LEVEL (user_id=X, post_id=Y): message
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(LOG_LEVELS)#INFO / WARNING / ERROR arasından rastgele Log’lar tekdüze olmasın diye 
    user_id = post.get("userId")
    post_id = post.get("id")
    # Title veya body mesaj olarak kullanılır, satır sonlarını temizleyelim
    message = post.get("title", "").replace("\n", " ")
    
    return f"[{timestamp}] {level} (user_id={user_id}, post_id={post_id}): {message}"

def create_logs(): #Her post için log üretir
    try:
        if not os.path.exists(RAW_DATA_PATH): #Dosya var mı kontrolü
            print(f"Hata: {RAW_DATA_PATH} bulunamadı. Önce --fetch komutunu çalıştırın.")
            return

        with open(RAW_DATA_PATH, "r", encoding="utf-8") as f: #JSON dosyasını okuma
            posts = json.load(f)
        
        logs = [] #Log üretme döngüsü
        for post in posts:
            logs.append(generate_log_line(post))
            
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f: #Log dosyasına yazma
            f.write("\n".join(logs))
            
        print(f"Başarılı! {len(logs)} adet log satırı {LOG_FILE_PATH} dosyasına yazıldı.")

    except Exception as e:
        print(f"Log oluşturulurken hata: {e}")