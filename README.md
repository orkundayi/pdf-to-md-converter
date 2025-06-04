# PDF to GitBook Markdown Converter v2.0

GitBook ile uyumlu, profesyonel Markdown dönüştürücü. **Uzun PDF'lerde GitBook'un kod bloğu hatası vermemesi için sayfa bazlı bölümleme özelliği.**

## 🌟 Yeni Özellikler (v2.0)

- ✅ **Sayfa Bazlı Bölümleme**: Her PDF sayfası ayrı Markdown dosyası olur
- ✅ **GitBook Uyumlu**: SUMMARY.md ve README.md otomatik oluşturur  
- ✅ **Modern GUI**: Kullanıcı dostu arayüz
- ✅ **Akıllı Mod Seçimi**: Büyük dosyalar için otomatik sayfa bazlı önerir
- ✅ **İlerleme Takibi**: Detaylı log ve durum bilgisi

## 🚀 Hızlı Başlangıç

### 1. GUI ile Kullanım (Önerilen)
```bash
python gui_v2.py
```

### 2. Komut Satırı ile Kullanım
```bash
# Tek dosya olarak
python main.py input.pdf

# Sayfa bazlı bölümleme ile
python -c "from pdf_to_markdown import PDFToMarkdownConverter; PDFToMarkdownConverter().convert_pdf_to_pages('input.pdf')"
```

## 📋 Kurulum

### Windows (Otomatik)
```bash
install.bat
```

### Manuel Kurulum
```bash
pip install -r requirements.txt
```

## 🎯 GitBook ile Kullanım

### Sayfa Bazlı Mod (Önerilen)
1. PDF'yi **"Sayfa Bazlı Bölümleme"** ile dönüştürün
2. Oluşan `{dosya_adi}_pages` klasörünü GitBook projenize kopyalayın
3. `SUMMARY.md` dosyasını GitBook'un tanıması için kullanın
4. Her sayfa ayrı dosya olduğu için GitBook kod bloğu hatası vermez

### Tek Dosya Mod
- Küçük PDF'ler için uygun
- Uzun dosyalarda GitBook tüm içeriği kod bloğu olarak algılayabilir

## 🔧 Özellikler

### Dönüştürme Özellikleri
- **Akıllı Başlık Tanıma**: Büyük harfli metinleri başlık olarak algılar
- **Tablo Formatı**: Boşluklarla ayrılmış tabloları Markdown'a çevirir
- **Görüntü Desteği**: PDF'deki görüntüleri çıkarır (sınırlı)
- **GitBook Meta**: Otomatik başlık, açıklama ve anchor linkler

### GUI Özellikleri
- **Sürükle-Bırak**: PDF dosyalarını direkt sürükleyebilirsiniz
- **Otomatik Ayarlar**: Başlık ve çıktı klasörü otomatik doldurulur
- **Dosya Boyutu Kontrolü**: Büyük dosyalar için sayfa bazlı mod önerir
- **Canlı Log**: İşlem durumunu gerçek zamanlı takip
- **Sonuç Önizleme**: Dönüştürme sonrası dosya/klasör açma

## 📊 Dönüştürme Modları

### 📄 Tek Markdown Dosyası
- Tüm PDF içeriğini tek dosyada birleştirir
- Küçük PDF'ler (< 5MB) için ideal
- Hızlı dönüştürme

### 📚 Sayfa Bazlı Bölümleme (ÖNERİLEN)
- Her PDF sayfası = 1 Markdown dosyası
- GitBook kod bloğu problemini çözer
- Büyük PDF'ler için ideal
- SUMMARY.md ile organize edilmiş yapı
- Klasör: `{baslik}_pages/`
  - `sayfa-01.md`, `sayfa-02.md`, ...
  - `SUMMARY.md` (GitBook için)
  - `README.md` (açıklamalar)

## 🛠️ Gereksinimler

```txt
pdfplumber>=0.9.0
```

## 📝 Örnek Kullanım

### Büyük PDF Dönüştürme
```python
from pdf_to_markdown import PDFToMarkdownConverter

converter = PDFToMarkdownConverter()

# Sayfa bazlı dönüştürme (GitBook için ideal)
dosyalar = converter.convert_pdf_to_pages(
    pdf_path="buyuk_kitap.pdf",
    output_dir="./output",
    title="Büyük Kitap"
)

print(f"{len(dosyalar)} sayfa oluşturuldu!")
```

### GitBook Klasör Yapısı
```
buyuk_kitap_pages/
├── README.md
├── SUMMARY.md
├── sayfa-01.md
├── sayfa-02.md
├── ...
└── sayfa-50.md
```

## ⚠️ GitBook İpuçları

1. **Uzun PDF'ler**: Mutlaka "Sayfa Bazlı Bölümleme" kullanın
2. **SUMMARY.md**: GitBook'un bu dosyayı tanıması için gerekli
3. **Kod Bloğu Sorunu**: Tek dosyada uzun içerik GitBook'ta kod olarak görünür
4. **Sayfa Limiti**: GitBook'un sayfa limiti yoktur, sayfa bazlı mod güvenlidir

## 🐛 Bilinen Sınırlamalar

- Görüntü çıkarma sınırlı (pdfplumber kısıtı)
- Karmaşık tablo yapıları tam desteklenmez
- Font ve stil bilgileri korunmaz

## 📞 Destek

Sorun yaşıyorsanız:
1. Log mesajlarını kontrol edin
2. PDF dosyasının bozuk olmadığından emin olun
3. Büyük dosyalar için sayfa bazlı mod kullandığınızdan emin olun

---

**GitBook Uyumlu • Türkçe Destekli • Modern GUI • Sayfa Bazlı Bölümleme**
