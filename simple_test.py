#!/usr/bin/env python3
"""
Basit PDF to Markdown Converter Test
"""

import sys
import os

# Basit test
def simple_test():
    print("🧪 PDF to Markdown Converter Kurulum Testi")
    print("=" * 50)
    
    # Python versiyonu
    print(f"Python versiyonu: {sys.version}")
    
    # Paket testleri
    try:
        import pdfplumber
        print("✅ pdfplumber başarıyla yüklendi")
    except ImportError as e:
        print(f"❌ pdfplumber hatası: {e}")
        return False
    
    try:
        import click
        print("✅ click başarıyla yüklendi")
    except ImportError as e:
        print(f"❌ click hatası: {e}")
        return False
    
    # Basit PDF test
    print("\n📄 PDF dosyası aranıyor...")
    test_files = ["test.pdf", "örnek.pdf", "sample.pdf"]
    
    for file in test_files:
        if os.path.exists(file):
            print(f"✅ Test PDF bulundu: {file}")
            
            try:
                with pdfplumber.open(file) as pdf:
                    print(f"📊 PDF bilgileri:")
                    print(f"  - Sayfa sayısı: {len(pdf.pages)}")
                    
                    if len(pdf.pages) > 0:
                        page = pdf.pages[0]
                        text = page.extract_text()
                        if text:
                            print(f"  - İlk sayfa karakter sayısı: {len(text)}")
                            print(f"  - İlk 100 karakter: {text[:100]}...")
                        else:
                            print("  - İlk sayfada metin bulunamadı")
                
                print("✅ PDF başarıyla okundu!")
                return True
                
            except Exception as e:
                print(f"❌ PDF okuma hatası: {e}")
                return False
    
    print("⚠️  Test için PDF dosyası bulunamadı")
    print("Herhangi bir PDF dosyasını bu klasöre koyun ve tekrar deneyin")
    return True

if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\n🎉 Kurulum başarılı! Ana programı çalıştırabilirsiniz:")
        print("python main.py dosya.pdf")
    else:
        print("\n❌ Kurulum sorunlu. requirements.txt'i kontrol edin")
        sys.exit(1)
