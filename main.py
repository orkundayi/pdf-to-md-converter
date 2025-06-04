#!/usr/bin/env python3
"""
PDF to GitBook Markdown Converter
Kullanım: python main.py <pdf_dosyasi> [çıktı_dizini] [başlık]
"""

import argparse
import sys
import os
from pdf_to_markdown import PDFToMarkdownConverter, create_gitbook_summary

def main():
    parser = argparse.ArgumentParser(
        description='PDF dosyasını GitBook uyumlu Markdown formatına dönüştürür'
    )
    
    parser.add_argument(
        'pdf_file',
        help='Dönüştürülecek PDF dosyasının yolu'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=None,
        help='Çıktı dizini (varsayılan: PDF ile aynı dizin)'
    )
    
    parser.add_argument(
        '-t', '--title',
        default=None,
        help='Döküman başlığı (varsayılan: PDF dosya adı)'
    )
    
    parser.add_argument(
        '--create-gitbook',
        action='store_true',
        help='GitBook projesi için SUMMARY.md dosyası oluştur'
    )
    
    args = parser.parse_args()
    
    # PDF dosyasının varlığını kontrol et
    if not os.path.exists(args.pdf_file):
        print(f"Hata: PDF dosyası bulunamadı: {args.pdf_file}")
        sys.exit(1)
    
    try:
        # Dönüştürücüyü başlat
        converter = PDFToMarkdownConverter()
        
        # PDF'yi Markdown'a dönüştür
        output_file = converter.convert_pdf_to_markdown(
            pdf_path=args.pdf_file,
            output_dir=args.output,
            title=args.title
        )
        
        print(f"\n✅ Başarılı! Markdown dosyası oluşturuldu: {output_file}")
        
        # GitBook summary dosyası oluştur
        if args.create_gitbook:
            summary_file = create_gitbook_summary([output_file], os.path.dirname(output_file))
            print(f"📚 GitBook SUMMARY.md dosyası oluşturuldu: {summary_file}")
        
        print("\n🔧 GitBook ile kullanım için:")
        print("1. gitbook init ile projeyi başlatın")
        print("2. Oluşturulan .md dosyasını SUMMARY.md'ye ekleyin")
        print("3. gitbook serve ile önizleme yapın")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
