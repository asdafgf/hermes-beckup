# Access Risk Takip Sistemi — VBA Kodları

## Tablo oluşturma
Access'te **Oluştur → Modül** aç, aşağıdaki kodu yapıştır, **F5** bas.

```vb
Public Sub VeriTabaniKur()
    On Error GoTo Hata_Handler
    Dim db As DAO.Database
    Set db = CurrentDb

    ' 1. KULLANICILAR TABLOSU
    db.Execute "CREATE TABLE kullanicilar (" & _
               "kullanici_id COUNTER CONSTRAINT PK_Kullanici PRIMARY KEY, " & _
               "kullanici_adi TEXT(50) NOT NULL, " & _
               "sifre TEXT(50) NOT NULL, " & _
               "yetki TEXT(10) DEFAULT 'kullanici', " & _
               "ad_soyad TEXT(100));"

    ' Benzersiz kullanıcı adı
    db.Execute "CREATE UNIQUE INDEX idx_kullanici_adi ON kullanicilar (kullanici_adi);"

    ' 2. RISKLER TABLOSU
    db.Execute "CREATE TABLE riskler (" & _
               "risk_id COUNTER CONSTRAINT PK_Risk PRIMARY KEY, " & _
               "tarih DATETIME, " & _
               "sorun_turu TEXT(50), " & _
               "aciklama MEMO, " & _
               "satici TEXT(100), " & _
               "risk_seviyesi TEXT(10) DEFAULT 'Dusuk', " & _
               "cozum_durumu TEXT(15) DEFAULT 'Beklemede', " & _
               "kullanici_id INTEGER, " & _
               "kayit_tarihi DATETIME DEFAULT Now(), " & _
               "CONSTRAINT FK_KullaniciRisk FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (kullanici_id));"

    Application.RefreshDatabaseWindow
    MsgBox "Tablolar başarıyla oluşturuldu.", vbInformation

Exit_Sub:
    Set db = Nothing
    Exit Sub

Hata_Handler:
    MsgBox "Hata: " & Err.Description, vbCritical
    Resume Exit_Sub
End Sub
```

## Admin kullanıcı ekle
Tablolar oluştuktan sonra aynı modüle bunu ekleyip F5 bas:

```vb
Public Sub AdminEkle()
    CurrentDb.Execute "INSERT INTO kullanicilar (kullanici_adi, sifre, yetki, ad_soyad) " & _
                      "VALUES ('admin', 'admin123', 'admin', 'Sistem Yoneticisi')"
    MsgBox "Admin kullanici eklendi! Kullanici: admin / Sifre: admin123"
End Sub
```

## Normal kullanıcı ekle
```vb
Public Sub KullaniciEkle(kAdi As String, sifre As String, adSoyad As String)
    CurrentDb.Execute "INSERT INTO kullanicilar (kullanici_adi, sifre, yetki, ad_soyad) " & _
                      "VALUES ('" & kAdi & "', '" & sifre & "', 'kullanici', '" & adSoyad & "')"
    MsgBox "Kullanici eklendi."
End Sub
```
