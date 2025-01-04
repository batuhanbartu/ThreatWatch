from database import ThreatDatabase
from threat_checker import ThreatChecker
import os
from dotenv import load_dotenv

def get_user_input():
    """Kullanıcıdan IP veya domain bilgisi alır"""
    print("\n=== Tehdit İstihbarat Sistemine Hoş Geldiniz ===")
    print("1. IP Adresi Ekle")
    print("2. Domain Ekle")
    print("3. Varsayılan test göstergelerini ekle")
    print("4. İzlemeyi başlat")
    print("5. Çıkış")
    
    choice = input("\nSeçiminiz (1-5): ")
    return choice

def add_single_indicator(db):
    """Kullanıcıdan alınan tek bir göstergeyi ekler"""
    indicator_type = input("Tip seçin (ip/domain): ").lower()
    if indicator_type not in ['ip', 'domain']:
        print("Geçersiz tip! 'ip' veya 'domain' girilmelidir.")
        return
    
    indicator = input(f"{indicator_type.upper()} adresi girin: ")
    notes = input("Not eklemek ister misiniz? (opsiyonel): ")
    
    if db.add_indicator(indicator, indicator_type, notes):
        print(f"\n✓ Başarıyla eklendi: {indicator}")
    else:
        print(f"\n! Bu gösterge zaten mevcut: {indicator}")

def add_test_indicators(db):
    """Örnek test göstergelerini ekler"""
    test_indicators = [
        ("8.8.8.8", "ip", "Google Public DNS"),
        ("1.1.1.1", "ip", "Cloudflare DNS"),
        ("google.com", "domain", "Google Ana Sayfası"),
        ("example.com", "domain", "Örnek Domain")
    ]

    print("\nTest göstergeleri ekleniyor...")
    for indicator, type_, notes in test_indicators:
        if db.add_indicator(indicator, type_, notes):
            print(f"✓ Eklendi: {indicator} ({type_})")
        else:
            print(f"! Zaten mevcut: {indicator}")

def main():
    # API anahtarını yükle
    load_dotenv()
    api_key = os.getenv('VIRUSTOTAL_API_KEY')
    
    if not api_key:
        print("Hata: VIRUSTOTAL_API_KEY bulunamadı!")
        print("Lütfen .env dosyasında API anahtarınızı tanımlayın.")
        return

    # Veritabanı ve tehdit kontrolcüsü başlatma
    db = ThreatDatabase()
    checker = ThreatChecker(db, api_key)

    while True:
        choice = get_user_input()
        
        if choice == '1' or choice == '2':
            add_single_indicator(db)
        elif choice == '3':
            add_test_indicators(db)
        elif choice == '4':
            print("\nİzleme başlatılıyor...")
            checker.start_monitoring()
        elif choice == '5':
            print("\nProgram sonlandırılıyor...")
            break
        else:
            print("\nGeçersiz seçim! Lütfen 1-5 arası bir sayı girin.")

if __name__ == "__main__":
    main() 