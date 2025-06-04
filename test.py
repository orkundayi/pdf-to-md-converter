"""
Test script for PDF to Markdown converter
Bu dosyayı kullanarak dönüştürücüyü test edebilirsiniz
"""

import os
import sys
from pdf_to_markdown import PDFToMarkdownConverter

def test_converter():
    """Dönüştürücüyü test et"""
    
    # Test PDF dosyası kontrolü
    test_files = [
        "test.pdf",
        "örnek.pdf", 
        "sample.pdf"
    ]
    
    pdf_file = None
    for file in test_files:
        if os.path.exists(file):
            pdf_file = file
            break
    
    if not pdf_file:
        print("❌ Test için PDF dosyası bulunamadı!")
        print("Aşağıdaki dosyalardan birini ekleyin:")
        for file in test_files:
            print(f"  - {file}")
        return
    
    print(f"📄 Test edilen PDF: {pdf_file}")
    
    try:
        # Dönüştürücüyü başlat
        converter = PDFToMarkdownConverter()
        
        # Test çıktı dizini
        output_dir = "test_output"
        
        # Dönüştür
        result = converter.convert_pdf_to_markdown(
            pdf_path=pdf_file,
            output_dir=output_dir,
            title="Test Dökümanı"
        )
        
        print(f"✅ Test başarılı! Çıktı: {result}")
        
        # Dosya boyutunu kontrol et
        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"📊 Oluşturulan dosya boyutu: {size} bytes")
            
            # İlk birkaç satırı göster
            with open(result, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                print("\n📝 Dosya önizlemesi:")
                print("=" * 50)
                for line in lines:
                    print(line.rstrip())
                print("=" * 50)
        
    except Exception as e:
        print(f"❌ Test hatası: {str(e)}")
        return False
    
    return True

def create_sample_markdown():
    """GitBook formatına örnek Markdown oluştur"""
    
    sample_content = """---
title: Örnek GitBook Dökümanı
description: PDF'den dönüştürülmüş örnek Markdown
---

# Örnek GitBook Dökümanı

## İçindekiler

- [Giriş](#giris)
- [Ana Bölüm](#ana-bolum)
  - [Alt Bölüm](#alt-bolum)
- [Sonuç](#sonuc)

---

## Giriş

Bu örnek GitBook uyumlu Markdown dökümanıdır.

## Ana Bölüm

### Alt Bölüm

İçerik burada yer alır.

#### Detay Başlığı

Daha detaylı açıklamalar...

## Sonuç

Döküman sonucu burada.
"""
    
    with open("ornek_gitbook.md", 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print("📚 Örnek GitBook Markdown dosyası oluşturuldu: ornek_gitbook.md")

if __name__ == "__main__":
    print("🧪 PDF to Markdown Converter Test\n")
    
    # Örnek Markdown oluştur
    create_sample_markdown()
    
    # Ana testi çalıştır
    if test_converter():
        print("\n🎉 Tüm testler başarılı!")
    else:
        print("\n❌ Test başarısız!")
        sys.exit(1)
