import sqlite3
from datetime import datetime

class ThreatDatabase:
    """Tehdit göstergelerini yönetmek için veritabanı sınıfı"""
    
    def __init__(self, db_name="threat_intel.db"):
        """Veritabanı bağlantısını başlatır ve tabloları oluşturur"""
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """Gerekli veritabanı tablolarını oluşturur"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            indicator TEXT NOT NULL,        -- IP veya domain adresi
            type TEXT NOT NULL,             -- 'ip' veya 'domain'
            threat_status BOOLEAN DEFAULT FALSE,  -- tehdit durumu
            last_checked TIMESTAMP,         -- son kontrol zamanı
            created_at TIMESTAMP,           -- oluşturulma zamanı
            notes TEXT,                     -- kullanıcı notları
            UNIQUE(indicator)
        )
        ''')
        
        conn.commit()
        conn.close()

    def add_indicator(self, indicator, type_, notes=""):
        """Yeni bir gösterge ekler
        
        Args:
            indicator (str): IP veya domain adresi
            type_ (str): Gösterge tipi ('ip' veya 'domain')
            notes (str): Opsiyonel kullanıcı notları
        
        Returns:
            bool: Ekleme başarılı ise True, değilse False
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO threats (indicator, type, notes, created_at, last_checked)
            VALUES (?, ?, ?, ?, ?)
            ''', (indicator, type_, notes, datetime.now(), datetime.now()))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def update_threat_status(self, indicator, is_threat):
        """Bir göstergenin tehdit durumunu günceller
        
        Args:
            indicator (str): Güncellenecek gösterge
            is_threat (bool): Yeni tehdit durumu
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE threats 
        SET threat_status = ?, last_checked = ?
        WHERE indicator = ?
        ''', (is_threat, datetime.now(), indicator))
        
        conn.commit()
        conn.close()

    def get_all_indicators(self):
        """Tüm göstergeleri getirir
        
        Returns:
            list: Tüm göstergelerin listesi
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM threats')
        results = cursor.fetchall()
        
        conn.close()
        return results 