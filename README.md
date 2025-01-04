# Siber Tehdit İstihbarat Aracı

Bu proje, IP adresleri ve domain'ler için tehdit istihbaratı sağlayan bir araçtır. VirusTotal API'sini kullanarak tehdit kontrolü yapar ve sonuçları bir SQLite veritabanında saklar.

## Özellikler

- IP ve domain bilgilerini kaydetme
- VirusTotal API ile tehdit kontrolü
- Gerçek zamanlı tehdit tespiti ve terminal çıktısı
- Otomatik kontrol mekanizması (örneğin, her 15 dakikada bir tüm kayıtların kontrolü)
- Veri tabanında tehdit durumlarını güncelleme ve görüntüleme

## Kurulum

1. **Gereksinimleri Yükleyin**

   Proje gereksinimlerini yüklemek için:

   ```bash
   pip install -r requirements.txt
   ```

2. **API Anahtarını Ayarlayın**

   VirusTotal API anahtarınızı `.env` dosyasına ekleyin:

   ```text
   VIRUSTOTAL_API_KEY=your_api_key_here
   ```

## Kullanım

1. **Programı Çalıştırın**

   ```bash
   python main.py
   ```

2. **Kullanıcı Arayüzü**

   Program çalıştığında, terminal üzerinden aşağıdaki seçenekler sunulacaktır:

   - IP Adresi Ekle
   - Domain Ekle
   - Varsayılan test göstergelerini ekle
   - İzlemeyi başlat
   - Çıkış

3. **Tehdit İzleme**

   İzleme başlatıldığında, program her 15 dakikada bir tüm kayıtları kontrol eder ve tehdit durumlarını günceller.

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir pull request gönderin veya bir issue açın.