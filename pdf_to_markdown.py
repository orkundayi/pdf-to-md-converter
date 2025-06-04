import pdfplumber
import os
import re
from pathlib import Path
from typing import List, Dict, Optional
import io

class PDFToMarkdownConverter:
    def __init__(self):
        self.current_chapter = 1
        self.current_section = 1
        self.toc_entries = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """PDF'den metin ve görüntüleri çıkarır"""
        pages_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Metin çıkar
                text = page.extract_text() or ""
                
                # Görüntüleri çıkar (pdfplumber ile basit görüntü çıkarma)
                images = []
                try:
                    # Sayfadaki görüntüleri tespit et
                    if hasattr(page, 'images') and page.images:
                        for img_index, img in enumerate(page.images):
                            images.append({
                                'data': None,  # pdfplumber ile görüntü verisi çıkarımı sınırlı
                                'filename': f'page_{page_num + 1}_img_{img_index + 1}.png'
                            })
                except:
                    pass
                
                pages_content.append({
                    'page_num': page_num + 1,
                    'text': text,
                    'images': images
                })
        
        return pages_content
    
    def clean_text(self, text: str) -> str:
        """Metni temizler ve düzenler"""
        # Gereksiz boşlukları temizle
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Sayfa numaralarını kaldır (genellikle tek başına sayılar)
        text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def detect_headings(self, text: str) -> str:
        """Başlıkları tespit eder ve Markdown formatına çevirir"""
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                processed_lines.append('')
                continue
            
            # Büyük harflerle yazılmış satırlar (başlık olabilir)
            if len(line) > 5 and line.isupper() and not line.isdigit():
                processed_lines.append(f'## {line.title()}')
                self.toc_entries.append({
                    'level': 2,
                    'title': line.title(),
                    'anchor': self.create_anchor(line.title())
                })
            
            # Sayı ile başlayan başlıklar
            elif re.match(r'^\d+\.?\s+[A-ZÇĞIİÖŞÜ]', line):
                processed_lines.append(f'### {line}')
                self.toc_entries.append({
                    'level': 3,
                    'title': line,
                    'anchor': self.create_anchor(line)
                })
            
            # Büyük harfle başlayan ve sonunda noktalama işareti olmayan kısa satırlar
            elif (len(line) < 100 and 
                  line[0].isupper() and 
                  not line.endswith('.') and 
                  not line.endswith(',') and
                  len(line.split()) <= 10):
                processed_lines.append(f'#### {line}')
                self.toc_entries.append({
                    'level': 4,
                    'title': line,
                    'anchor': self.create_anchor(line)
                })
            
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def create_anchor(self, title: str) -> str:
        """GitBook uyumlu anchor oluşturur"""
        # Türkçe karakterleri dönüştür
        tr_chars = {
            'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
            'Ç': 'C', 'Ğ': 'G', 'I': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
        }
        
        for tr_char, en_char in tr_chars.items():
            title = title.replace(tr_char, en_char)
        
        # Özel karakterleri kaldır ve küçük harfe çevir
        anchor = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        anchor = re.sub(r'\s+', '-', anchor.strip().lower())
        
        return anchor
    
    def format_for_gitbook(self, content: str, title: str = "PDF Dönüştürülmüş Döküman") -> str:
        """GitBook formatına uygun Markdown oluşturur"""
        
        # GitBook meta bilgileri
        gitbook_header = f"""---
title: {title}
description: PDF'den dönüştürülmüş Markdown dökümanı
---

# {title}

"""
        
        # İçindekiler tablosu oluştur
        if self.toc_entries:
            toc = "\n## İçindekiler\n\n"
            for entry in self.toc_entries:
                indent = "  " * (entry['level'] - 2)
                toc += f"{indent}- [{entry['title']}](#{entry['anchor']})\n"
            toc += "\n---\n\n"
        else:
            toc = ""
        
        # Görüntü referanslarını düzenle
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'![Alt text](\2)\n\n*Resim: \1*\n', content)
        
        # Kod bloklarını düzenle (eğer varsa)
        content = self.format_code_blocks(content)
        
        # Tablolar için düzenleme
        content = self.format_tables(content)
        
        return gitbook_header + toc + content
    
    def format_code_blocks(self, content: str) -> str:
        """Kod bloklarını tespit eder ve formatlar"""
        # Girinti ile kod bloğu gibi görünen kısımları tespit et
        lines = content.split('\n')
        processed_lines = []
        in_code_block = False
        
        for line in lines:
            # 4 veya daha fazla boşlukla başlayan satırlar
            if line.startswith('    ') or line.startswith('\t'):
                if not in_code_block:
                    processed_lines.append('```')
                    in_code_block = True
                processed_lines.append(line.lstrip())
            else:
                if in_code_block:
                    processed_lines.append('```\n')
                    in_code_block = False
                processed_lines.append(line)
        
        if in_code_block:
            processed_lines.append('```')
        
        return '\n'.join(processed_lines)
    
    def format_tables(self, content: str) -> str:
        """Tablo formatını düzenler"""
        # Basit tablo tespiti ve düzenlemesi
        lines = content.split('\n')
        processed_lines = []
        
        for i, line in enumerate(lines):
            # Birden fazla boşlukla ayrılmış kolonlar (tablo olabilir)
            if re.search(r'\s{3,}', line) and len(line.split()) > 2:
                # Tablo satırı olarak formatla
                cells = re.split(r'\s{3,}', line.strip())
                table_row = '| ' + ' | '.join(cells) + ' |'
                processed_lines.append(table_row)
                
                # İlk satırsa header separator ekle
                if i == 0 or not re.search(r'\s{3,}', lines[i-1]):
                    separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                    processed_lines.append(separator)
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def save_images(self, images: List[Dict], output_dir: str):
        """Görüntüleri kaydet (pdfplumber sınırlı görüntü desteği)"""
        images_dir = os.path.join(output_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        # pdfplumber ile görüntü verisi sınırlı olduğu için basit placeholder
        for img in images:
            if img['data']:  # Sadece veri varsa kaydet
                img_path = os.path.join(images_dir, img['filename'])
                with open(img_path, 'wb') as f:
                    f.write(img['data'])
    
    def convert_pdf_to_markdown(self, pdf_path: str, output_dir: str = None, title: str = None) -> str:
        """Ana dönüştürme fonksiyonu"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF dosyası bulunamadı: {pdf_path}")
        
        # Çıktı dizini belirle
        if output_dir is None:
            output_dir = os.path.dirname(pdf_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # PDF'den içerik çıkar
        print("PDF içeriği çıkarılıyor...")
        pages_content = self.extract_text_from_pdf(pdf_path)
        
        # Tüm metinleri birleştir
        full_text = ""
        all_images = []
        
        for page in pages_content:
            if page['text'].strip():
                full_text += f"\n\n<!-- Sayfa {page['page_num']} -->\n\n"
                full_text += page['text']
            
            all_images.extend(page['images'])
        
        # Metni temizle ve başlıkları tespit et
        print("Metin işleniyor...")
        cleaned_text = self.clean_text(full_text)
        formatted_text = self.detect_headings(cleaned_text)
        
        # GitBook formatına çevir
        if title is None:
            title = Path(pdf_path).stem
        
        print("GitBook formatına dönüştürülüyor...")
        gitbook_content = self.format_for_gitbook(formatted_text, title)
        
        # Markdown dosyasını kaydet
        output_file = os.path.join(output_dir, f"{title}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(gitbook_content)
        
        # Görüntüleri kaydet
        if all_images:
            print(f"{len(all_images)} görüntü kaydediliyor...")
            self.save_images(all_images, output_dir)
        
        print(f"Dönüştürme tamamlandı! Çıktı: {output_file}")
        return output_file
    
    def convert_pdf_to_pages(self, pdf_path: str, output_dir: str = None, title: str = None) -> List[str]:
        """PDF'yi sayfa sayfa ayrı Markdown dosyalarına dönüştürür"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF dosyası bulunamadı: {pdf_path}")
        
        # Ana klasör adı
        if title is None:
            title = Path(pdf_path).stem
        
        # Çıktı dizini
        if output_dir is None:
            output_dir = os.path.dirname(pdf_path)
        
        # Ana klasör oluştur
        main_folder = os.path.join(output_dir, f"{title}_pages")
        os.makedirs(main_folder, exist_ok=True)
        
        print(f"📁 Ana klasör oluşturuldu: {main_folder}")
        
        # PDF'den içerik çıkar
        print("📄 PDF sayfa sayfa işleniyor...")
        pages_content = self.extract_text_from_pdf(pdf_path)
        
        created_files = []
        summary_entries = []
        
        for page in pages_content:
            if not page['text'].strip():
                print(f"⚠️  Sayfa {page['page_num']} boş, atlanıyor")
                continue
            
            # Sayfa için yeni converter instance (TOC temizlemek için)
            page_converter = PDFToMarkdownConverter()
            
            # Metni temizle ve formatla
            cleaned_text = page_converter.clean_text(page['text'])
            formatted_text = page_converter.detect_headings(cleaned_text)
            
            # Sayfa başlığı
            page_title = f"{title} - Sayfa {page['page_num']}"
            
            # GitBook formatında oluştur
            gitbook_content = page_converter.format_for_gitbook(formatted_text, page_title)
            
            # Dosya adı
            filename = f"sayfa-{page['page_num']:02d}.md"
            output_file = os.path.join(main_folder, filename)
            
            # Dosyayı kaydet
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(gitbook_content)
            
            created_files.append(output_file)
            summary_entries.append({
                'filename': filename,
                'title': page_title,
                'page_num': page['page_num']
            })
            
            print(f"✅ Sayfa {page['page_num']} oluşturuldu: {filename}")
        
        # SUMMARY.md dosyası oluştur
        self.create_pages_summary(summary_entries, main_folder, title)
        
        # README.md oluştur
        self.create_pages_readme(main_folder, title, len(created_files))
        
        print(f"🎉 {len(created_files)} sayfa başarıyla dönüştürüldü!")
        print(f"📚 GitBook klasörü: {main_folder}")
        
        return created_files
    
    def create_pages_summary(self, entries: List[Dict], output_dir: str, title: str):
        """Sayfa bazında SUMMARY.md oluşturur"""
        summary_content = f"""# {title}

## İçindekiler

"""
        
        for entry in entries:
            summary_content += f"* [Sayfa {entry['page_num']}]({entry['filename']})\n"
        
        summary_path = os.path.join(output_dir, "SUMMARY.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"📑 SUMMARY.md oluşturuldu")
    
    def create_pages_readme(self, output_dir: str, title: str, page_count: int):
        """Ana README.md oluşturur"""
        readme_content = f"""# {title}

Bu klasör **{title}** PDF dosyasının sayfa sayfa Markdown dönüşümünü içerir.

## 📊 İstatistikler
- **Toplam Sayfa:** {page_count}
- **Dönüştürme Tarihi:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
- **Format:** GitBook uyumlu Markdown

## 📖 GitBook ile Kullanım

1. Bu klasörü GitBook projenize kopyalayın
2. `SUMMARY.md` dosyasını kullanın
3. `gitbook serve` ile önizleme yapın

## 📄 Sayfa Listesi

"""
        
        # Sayfa dosyalarını listele
        for i in range(1, page_count + 1):
            readme_content += f"- [Sayfa {i:02d}](sayfa-{i:02d}.md)\n"
        
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"📖 README.md oluşturuldu")
    
    def create_gitbook_summary(self, markdown_files: List[str], output_dir: str, title: str = "PDF Dönüştürülmüş Döküman") -> str:
        """Tek dosya için GitBook SUMMARY.md oluşturur"""
        summary_content = f"""# {title}

## İçindekiler

"""
        
        for md_file in markdown_files:
            filename = os.path.basename(md_file)
            file_title = Path(md_file).stem.replace('_', ' ').replace('-', ' ').title()
            summary_content += f"* [{file_title}]({filename})\n"
        
        summary_path = os.path.join(output_dir, "SUMMARY.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"📑 GitBook SUMMARY.md oluşturuldu")
        return summary_path
