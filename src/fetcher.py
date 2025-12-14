# src/fetcher.py
import requests #http istekleri get post için kullanılır(buradan API ye get isteği atıcaz)
import json #python objelerini json a çevirmek ve json dosyasını yazma/okuma yapar
import os # dosya ve klasör işlemleri

RAW_DATA_PATH = os.path.join("data", "raw_posts.json") #kaydedilecek dosyanın yolu
API_URL = "https://jsonplaceholder.typicode.com/posts" # veri çekeceğim API endpointi

def fetch_posts(limit: int = 100) -> list[dict]: #API den post çekme(varsayılan 100 kayıt)
    #list[dict] → fonksiyon dictionary listesi döndürür
    """
    API'den post verilerini çeker ve JSON dosyasına kaydeder.
    """
    try:
        print(f"İstek gönderiliyor: {API_URL}")
        response = requests.get(API_URL, timeout=10) #API ye get isteği yollandı(10 saniye içinde cevap gelmezse iptal eder)
        
        # HTTP hatası kontrolü (404, 500 vb. hata varsa exception fırlatır)
        response.raise_for_status()
        
        data = response.json() #API’den gelen JSON → Python list/dict(JSON cevabı Python’a çevirme)
        
        # İlk 'limit' kadar kaydı al(orn: limit=10 ->ilk 10 post)
        limited_data = data[:limit]
        
        # Klasör yoksa oluştur (Garanti olsun)
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
        
        with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(limited_data, f, indent=4, ensure_ascii=False)
        #with open dosyayı güvenli bir şekilde açar, iş bitince otomatik kapatır
        #json.dump python objesini -> json dosyasına yazar
        #indent=4 → okunabilir format
        #ensure_ascii=False → Türkçe karakterler bozulmaz
        
        print(f"Başarılı! {len(limited_data)} kayıt {RAW_DATA_PATH} dosyasına kaydedildi.")
        return limited_data

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Hatası oluştu: {err}")
    except requests.exceptions.Timeout: #zaman aşımına uğradı
        print("İstek zaman aşımına uğradı (Timeout).")
    except requests.exceptions.RequestException as err: #geç cevap verdi
        print(f"Bir ağ hatası meydana geldi: {err}")
    except Exception as e: #İnternet yok, DNS hatası vb
        print(f"Beklenmedik bir hata: {e}")
    
    return []