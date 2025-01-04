import time
import schedule
import requests
from datetime import datetime

class ThreatChecker:
    """VirusTotal API kullanarak tehdit kontrolü yapan sınıf"""
    
    def __init__(self, database, api_key: str):
        """Tehdit kontrolcüsünü başlatır
        
        Args:
            database: Veritabanı bağlantısı
            api_key (str): VirusTotal API anahtarı
        """
        self.database = database
        self.api_key = api_key
        self.headers = {
            'x-apikey': self.api_key
        }
        self.vt_api_url = 'https://www.virustotal.com/vtapi/v3'

    def check_ip(self, ip: str) -> bool:
        """IP adresini VirusTotal'da kontrol eder
        
        Args:
            ip (str): Kontrol edilecek IP adresi
            
        Returns:
            bool: Tehdit tespit edildi ise True, değilse False
        """
        url = f"{self.vt_api_url}/ip_addresses/{ip}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                return stats['malicious'] > 0 or stats['suspicious'] > 0
            return False
        except Exception as e:
            print(f"IP kontrolünde hata: {e}")
            return False

    def check_domain(self, domain: str) -> bool:
        """Domain adresini VirusTotal'da kontrol eder
        
        Args:
            domain (str): Kontrol edilecek domain adresi
            
        Returns:
            bool: Tehdit tespit edildi ise True, değilse False
        """
        url = f"{self.vt_api_url}/domains/{domain}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                return stats['malicious'] > 0 or stats['suspicious'] > 0
            return False
        except Exception as e:
            print(f"Domain kontrolünde hata: {e}")
            return False

    def check_indicator(self, indicator: str, type_: str) -> bool:
        """Göstergeyi tipine göre kontrol eder"""
        if type_ == "ip":
            return self.check_ip(indicator)
        elif type_ == "domain":
            return self.check_domain(indicator)
        return False

    def check_all_indicators(self):
        """Veritabanındaki tüm göstergeleri kontrol eder"""
        print(f"\n[{datetime.now()}] Tüm göstergeler kontrol ediliyor...")
        indicators = self.database.get_all_indicators()
        
        for indicator in indicators:
            id_, ind, type_, current_status, last_checked, created_at, notes = indicator
            is_threat = self.check_indicator(ind, type_)
            
            if is_threat != current_status:
                self.database.update_threat_status(ind, is_threat)
                status_text = "TEHDİT TESPIT EDILDI!" if is_threat else "Tehdit durumu temiz"
                print(f"[!] {ind} için durum değişikliği: {status_text}")
            
            # API rate limiting - VirusTotal limitlerine uyum
            time.sleep(15)

    def start_monitoring(self, interval_minutes=15):
        """Periyodik kontrol döngüsünü başlatır"""
        print(f"Tehdit izleme başlatıldı. Her {interval_minutes} dakikada bir kontrol yapılacak.")
        
        self.check_all_indicators()  # İlk kontrol
        schedule.every(interval_minutes).minutes.do(self.check_all_indicators)
        
        while True:
            schedule.run_pending()
            time.sleep(1) 