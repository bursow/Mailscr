# E-posta Gönderim Aracı

Bu Python betiği, Outlook veya Gmail SMTP sunucularını kullanarak e-posta göndermenizi sağlar. Tek bir alıcıya veya birden fazla alıcıya e-posta gönderebilirsiniz. Alıcı bilgilerini bir SQLite veritabanı veya CSV dosyasından alabilirsiniz.

## Başlangıç

### Gereksinimler

- Python 3.x
- `smtplib`, `email`, `getpass`, `sqlite3`, `csv` (Python standart kütüphaneleridir, ekstra bir kurulum gerektirmez)

### Kullanımm
mail göndermek için şu adımları izleyin:

scripti çalıştırın 

    python eposta_gonder.py

Sunucu seçimini yapın:

    1 : Outlook
    2 : Gmail
    
    E-posta adresinizi ve şifrenizi girin.
    E-posta konusunu ve içeriğini girin.

E-posta gönderim türünü seçin:

    1 : Tek alıcı
    2 : Birden fazla alıcı

Eğer birden fazla alıcı seçerseniz, e-posta alıcılarını bir SQLite veritabanı (mail.db) veya CSV dosyası (mail.csv) üzerinden alabilirsiniz.

    SQLite Kullanımı:
        Veritabanının adı mail.db olmalı.
        Veritabanında bir email tablosu bulunmalı.
    CSV Kullanımı:
        CSV dosyasının adı mail.csv olmalı.





