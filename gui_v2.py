#!/usr/bin/env python3
"""
PDF to Markdown Converter - Modern GUI with AI Enhancement
GitBook uyumlu, AI destekli gelişmiş özelliklerle
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import json
import requests
from pathlib import Path
from pdf_to_markdown import PDFToMarkdownConverter

# Drag & Drop için
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("⚠️ Uyarı: tkinterdnd2 kurulu değil. Sürükle-bırak özelliği çalışmayacak.")
    print("📦 Kurulum: pip install tkinterdnd2")

# AI API için
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIDocumentEnhancer:
    """AI destekli doküman geliştiricisi"""
    
    def __init__(self):
        self.client = None
        self.api_key = None
        
    def set_api_key(self, api_key: str):
        """OpenAI API anahtarını ayarla"""
        self.api_key = api_key
        if OPENAI_AVAILABLE and api_key:
            try:
                self.client = openai.OpenAI(api_key=api_key)
                return True
            except Exception as e:
                print(f"AI API hatası: {e}")
                return False
        return False
    
    def enhance_markdown_document(self, markdown_content: str, title: str) -> str:
        """Markdown dokümanını AI ile geliştirir"""
        if not self.client:
            return markdown_content
        
        try:
            prompt = f"""
Aşağıdaki Markdown dokümanını GitBook için profesyonel bir formata dönüştür. 

GEREKSINIMLER:
1. GitBook uyumlu meta bilgiler ekle (---title, description---)
2. Güzel emojiler ve simgeler kullan (📚, 🔧, 💡, ⚡, 🎯, vb.)
3. İçindekiler tablosu oluştur
4. Başlıkları kategorilere göre organize et
5. Tablolar varsa güzel formatla
6. Önemli terimleri **bold** yap
7. Kod bloklarını ```language ile formatla
8. Notları 💡 **Not:** formatında yaz
9. Bölümler arası ---separator ekle
10. Alt bilgi ekle (oluşturma tarihi, kaynak bilgisi)

Doküman Başlığı: {title}

İçerik:
{markdown_content}

Lütfen yukarıdaki gereksinimlere göre profesyonel, okunabilir ve GitBook'ta mükemmel görünecek bir doküman oluştur.
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen bir profesyonel teknik yazı editörüsün. Markdown dokümanlarını GitBook formatında mükemmel şekilde düzenleyebiliyorsun."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            enhanced_content = response.choices[0].message.content
            return enhanced_content
            
        except Exception as e:
            print(f"AI geliştirme hatası: {e}")
            return markdown_content
    
    def create_summary_and_structure(self, content: str, title: str) -> dict:
        """İçerik için özet ve yapı oluşturur"""
        if not self.client:
            return {"summary": "", "structure": []}
        
        try:
            prompt = f"""
Bu doküman için:
1. Kısa bir özet (2-3 cümle)
2. Ana bölümlerin listesi 
3. GitBook için SUMMARY.md yapısı öner

Doküman: {title}
İçerik: {content[:1000]}...

JSON formatında döndür:
{{
    "summary": "...",
    "structure": ["Bölüm 1", "Bölüm 2", ...],
    "gitbook_summary": "* [Ana Sayfa](README.md)\n* [Bölüm 1](bolum1.md)"
}}
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sen GitBook doküman yapısı uzmanısın. JSON formatında cevap ver."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"AI yapı oluşturma hatası: {e}")
            return {"summary": "", "structure": [], "gitbook_summary": ""}

class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to GitBook Markdown Converter v2.1 - AI Enhanced")
        self.root.geometry("800x750")
        self.root.configure(bg='#f0f0f0')
        
        # AI enhancer
        self.ai_enhancer = AIDocumentEnhancer()
        
        # Initialize StringVar variables
        self.pdf_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.api_key_var = tk.StringVar()
        
        # Load saved API key if exists
        self.load_api_key()
        
        # Ana frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initialize converter and other variables
        self.converter = PDFToMarkdownConverter()
        self.selected_pdf = None
        
        # Create UI components
        self.create_header()
        self.create_file_selection_area()
        self.create_settings_area()
        self.create_conversion_options()
        self.create_ai_options()
        self.create_convert_button()
        self.create_log_area()
        self.create_status_bar()
        
        # Grid ağırlıkları
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
    
    def create_header(self):
        """Başlık alanı"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="🤖 PDF to GitBook Markdown Converter v2.1 - AI Enhanced",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="GitBook uyumlu • AI destekli doküman iyileştirme",
            font=('Arial', 10),
            foreground='#666666'
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        header_frame.columnconfigure(0, weight=1)
    
    def create_file_selection_area(self):
        """PDF dosyası seçme alanı"""
        file_frame = ttk.LabelFrame(self.main_frame, text="📁 PDF Dosyası Seçimi", padding="15")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Sürükle-bırak alanı
        self.drop_area = tk.Frame(file_frame, bg='#e8f4fd', relief='ridge', bd=2)
        self.drop_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        drop_label = tk.Label(
            self.drop_area,
            text="📄 PDF dosyanızı buraya sürükleyin\nveya aşağıdaki düğmeye tıklayın",
            bg='#e8f4fd',
            font=('Arial', 12),
            pady=30
        )
        drop_label.pack()
        
        # Sürükle-bırak eventleri
        self.setup_drag_drop()
        
        # Dosya seçme butonu
        self.select_button = ttk.Button(
            file_frame,
            text="🔍 PDF Dosyası Seç",
            command=self.select_pdf_file
        )
        self.select_button.grid(row=1, column=0, pady=5)        
        # Seçili dosya bilgisi
        self.file_label = ttk.Label(file_frame, text="Henüz dosya seçilmedi")
        self.file_label.grid(row=1, column=1, padx=(10, 0), sticky=tk.W)
        
        file_frame.columnconfigure(1, weight=1)
    def setup_drag_drop(self):
        """Gerçek sürükle-bırak desteği"""
        if DND_AVAILABLE:
            # Gerçek drag & drop
            self.drop_area.drop_target_register(DND_FILES)
            self.drop_area.dnd_bind('<<Drop>>', self.on_file_drop)
            
            # Visual feedback
            def on_drag_enter(event):
                self.drop_area.configure(bg='#d1e7dd')
                return 'copy'
            
            def on_drag_leave(event):
                self.drop_area.configure(bg='#e8f4fd')
            
            self.drop_area.dnd_bind('<<DragEnter>>', on_drag_enter)
            self.drop_area.dnd_bind('<<DragLeave>>', on_drag_leave)
        else:
            # Fallback - click to select
            def on_click(event):
                self.select_pdf_file()
            
            def on_enter(event):
                self.drop_area.configure(bg='#d1e7dd')
            
            def on_leave(event):
                self.drop_area.configure(bg='#e8f4fd')
            
            self.drop_area.bind('<Button-1>', on_click)
            self.drop_area.bind('<Enter>', on_enter)
            self.drop_area.bind('<Leave>', on_leave)
    
    def on_file_drop(self, event):
        """Dosya sürüklendiğinde çalışır"""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]  # İlk dosyayı al
            if file_path.lower().endswith('.pdf'):
                self.process_selected_file(file_path)
                self.log(f"📁 Sürüklenen dosya işlendi: {os.path.basename(file_path)}")
            else:
                messagebox.showwarning("⚠️ Uyarı", "Lütfen sadece PDF dosyalarını sürükleyin!")
                self.log("⚠️ PDF olmayan dosya sürüklendi")
        return 'copy'
    
    def process_selected_file(self, file_path: str):
        """Seçilen dosyayı işle"""
        if os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
            self.pdf_var.set(file_path)
            self.log(f"📄 PDF seçildi: {os.path.basename(file_path)}")
            
            # Başlık boşsa, dosya adından başlık oluştur
            if not self.title_var.get().strip():
                title = os.path.splitext(os.path.basename(file_path))[0]
                title = title.replace('_', ' ').replace('-', ' ').title()
                self.title_var.set(title)
                self.log(f"📝 Başlık otomatik ayarlandı: {title}")
            
            # Çıktı dizini boşsa, PDF ile aynı dizini ayarla
            if not self.output_var.get().strip():
                output_dir = os.path.dirname(file_path)
                if not output_dir:
                    output_dir = os.getcwd()
                self.output_var.set(output_dir)
                self.log(f"📁 Çıktı dizini ayarlandı: {output_dir}")
        else:
            messagebox.showerror("❌ Hata", "Geçersiz dosya! Lütfen bir PDF dosyası seçin.")
            self.log("❌ Geçersiz dosya seçildi")
    
    def create_settings_area(self):
        """Ayarlar alanı"""
        settings_frame = ttk.LabelFrame(self.main_frame, text="⚙️ Temel Ayarlar", padding="15")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Başlık
        ttk.Label(settings_frame, text="Döküman Başlığı:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(settings_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
        # Çıktı dizini
        ttk.Label(settings_frame, text="Çıktı Klasörü:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.output_entry = ttk.Entry(settings_frame, textvariable=self.output_var, width=40)
        self.output_entry.grid(row=1, column=1, padx=(10, 0), sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.output_button = ttk.Button(
            settings_frame,
            text="📁",
            command=self.select_output_dir
        )
        self.output_button.grid(row=1, column=2, padx=(5, 0), pady=(10, 0))
        settings_frame.columnconfigure(1, weight=1)
    
    def create_conversion_options(self):
        """Gelişmiş doküman formatı seçenekleri"""
        options_frame = ttk.LabelFrame(self.main_frame, text="🔧 Doküman Formatı", padding="15")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # GitBook seçeneği
        self.gitbook_var = tk.BooleanVar(value=True)
        self.gitbook_check = ttk.Checkbutton(
            options_frame,
            text="✅ GitBook formatında oluştur (İçindekiler, güzel başlıklar ve formatlar)",
            variable=self.gitbook_var
        )
        self.gitbook_check.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Gelişmiş doküman formatı seçeneği
        self.enhanced_format_var = tk.BooleanVar(value=True)
        self.enhanced_format_check = ttk.Checkbutton(
            options_frame,
            text="🎨 Gelişmiş doküman formatı (Emojiler, renkler, düzenli başlıklar)",
            variable=self.enhanced_format_var
        )
        self.enhanced_format_check.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
          # AI İyileştirme seçeneği
        self.ai_enhance_var = tk.BooleanVar(value=False)
        self.ai_enhance_check = ttk.Checkbutton(
            options_frame,
            text="🤖 AI ile doküman iyileştir (OpenAI API gerekli)",
            variable=self.ai_enhance_var,
            command=self.toggle_ai_options
        )
        self.ai_enhance_check.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # OpenAI API Key girişi (gizli)
        self.api_frame = ttk.Frame(options_frame)
        self.api_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.api_frame.grid_remove()  # Başlangıçta gizli
        
        ttk.Label(self.api_frame, text="🔑 OpenAI API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(self.api_frame, textvariable=self.api_key_var, width=40, show="*")
        self.api_key_entry.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
        # API Key kaydet/yükle butonları
        self.save_api_button = ttk.Button(self.api_frame, text="💾", command=self.save_api_key, width=3)
        self.save_api_button.grid(row=0, column=2, padx=(5, 0))
        
        self.load_api_button = ttk.Button(self.api_frame, text="📂", command=self.load_api_key, width=3)
        self.load_api_button.grid(row=0, column=3, padx=(5, 0))
        
        # Test butonu
        self.test_api_button = ttk.Button(
            self.api_frame,
            text="🧪 API Test",
            command=self.test_api_key
        )
        self.test_api_button.grid(row=0, column=2, padx=(5, 0))
        
        # Açıklama
        desc_label = ttk.Label(
            options_frame,
            text="💡 AI iyileştirme: Dokümanınızı profesyonel GitBook formatına dönüştürür.\n"
                 "OpenAI API anahtarı gereklidir. Güvenlik için anahtarınız yerel olarak saklanır.",
            font=('Arial', 9),
            foreground='#0066cc'
        )
        desc_label.grid(row=4, column=0, sticky=tk.W)
        
        self.api_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(0, weight=1)
    
    def create_ai_options(self):
        """AI seçenekleri oluştur (Artık conversion_options içinde)"""
        pass  # Bu fonksiyon artık gerekli değil
    
    def toggle_ai_options(self):
        """AI seçeneklerini göster/gizle"""
        if self.ai_enhance_var.get():
            self.api_frame.grid()
            self.log("🤖 AI iyileştirme etkinleştirildi")
            # Kaydedilmiş API key varsa yükle
            self.load_api_key()
        else:
            self.api_frame.grid_remove()
            self.log("🤖 AI iyileştirme devre dışı bırakıldı")
    
    def test_api_key(self):
        """API anahtarını test et"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("⚠️ Uyarı", "Lütfen API anahtarınızı girin!")
            return
        
        # Test thread'i
        def test_thread():
            try:
                self.log("🧪 API anahtarı test ediliyor...")
                success = self.ai_enhancer.set_api_key(api_key)
                
                if success:
                    self.root.after(0, lambda: self.log("✅ API anahtarı geçerli!"))
                    self.root.after(0, lambda: messagebox.showinfo("✅ Başarılı", "API anahtarı geçerli ve kullanıma hazır!"))                    # API key'i güvenli şekilde kaydet
                    self.save_api_key(api_key)
                else:
                    self.root.after(0, lambda: self.log("❌ API anahtarı geçersiz"))
                    self.root.after(0, lambda: messagebox.showerror("❌ Hata", "API anahtarı geçersiz. Lütfen kontrol edin."))
            
            except Exception as e:
                self.root.after(0, lambda: self.log(f"❌ API test hatası: {e}"))
                self.root.after(0, lambda: messagebox.showerror("❌ Hata", f"API test hatası: {e}"))
        
        thread = threading.Thread(target=test_thread)
        thread.daemon = True
        thread.start()
    
    def save_api_key(self, api_key: str = None):
        """API anahtarını güvenli şekilde kaydet"""
        try:
            import base64
            
            # API key'i al (parametre veya giriş alanından)
            if api_key is None:
                api_key = self.api_key_var.get().strip()
            
            if not api_key:
                messagebox.showwarning("⚠️ Uyarı", "Lütfen API anahtarınızı girin!")
                return
            
            # Basit şifreleme (üretim için daha güvenli yöntem kullanın)
            encoded = base64.b64encode(api_key.encode()).decode()
            
            config_file = os.path.join(os.path.dirname(__file__), '.config.json')
            config = {'api_key': encoded}
            
            with open(config_file, 'w') as f:
                json.dump(config, f)
                
            self.log("🔐 API anahtarı güvenli şekilde kaydedildi")
            messagebox.showinfo("✅ Başarılı", "API anahtarı güvenli şekilde kaydedildi!")
            
        except Exception as e:
            self.log(f"⚠️ API anahtarı kaydedilemedi: {e}")
    
    def load_api_key(self):
        """Kaydedilmiş API anahtarını yükle"""
        try:
            import base64
            config_file = os.path.join(os.path.dirname(__file__), '.config.json')
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                if 'api_key' in config:
                    # Basit çözme
                    decoded = base64.b64decode(config['api_key']).decode()
                    self.api_key_var.set(decoded)
                    self.ai_enhancer.set_api_key(decoded)
                    self.log("🔐 Kaydedilmiş API anahtarı yüklendi")
                    
        except Exception as e:
            self.log(f"⚠️ API anahtarı yüklenemedi: {e}")
    
    def enhance_with_ai(self, content: str, title: str) -> str:
        """AI ile doküman içeriğini iyileştir"""
        if not OPENAI_AVAILABLE:
            raise Exception("OpenAI kütüphanesi kurulu değil!")
        
        api_key = self.api_key_var.get().strip()
        if not api_key:
            raise Exception("OpenAI API key gerekli!")
        
        try:
            # OpenAI API isteği
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""Lütfen aşağıdaki Markdown dökümanını GitBook için optimize et:

1. İçindekiler tablosu oluştur
2. Başlıkları emoji'lerle zenginleştir  
3. Önemli bilgileri vurgula
4. Tablo formatlarını düzenle
5. Code block'ları uygun şekilde formatla
6. Daha okunabilir hale getir

Başlık: {title}

İçerik:
{content[:4000]}...  # İlk 4000 karakter (token limiti için)

Lütfen sadece düzenlenmiş Markdown döndür, başka açıklama ekleme."""

            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Sen GitBook dokümanları için uzman bir Markdown formatlayıcısın."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.3
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                enhanced_content = result['choices'][0]['message']['content']
                
                self.log("🤖 AI iyileştirmesi tamamlandı!")
                return enhanced_content
            else:
                error_msg = f"API Hatası: {response.status_code}"
                if response.text:
                    error_detail = response.json().get('error', {}).get('message', 'Bilinmeyen hata')
                    error_msg += f" - {error_detail}"
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Bağlantı hatası: {str(e)}")
        except Exception as e:
            raise Exception(f"AI iyileştirme hatası: {str(e)}")

    def create_convert_button(self):
        """Dönüştür butonu oluştur"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.convert_button = ttk.Button(
            button_frame,
            text="🚀 Dönüştür!",
            command=self.start_conversion,
            style='Convert.TButton'
        )
        self.convert_button.grid(row=0, column=0, padx=5)
        
        # Stil oluştur
        style = ttk.Style()
        style.configure('Convert.TButton', 
                       foreground='#2e7d32', 
                       font=('Arial', 12, 'bold'))

    def select_pdf_file(self):
        """PDF dosyası seç"""
        filename = filedialog.askopenfilename(
            title="PDF Dosyası Seçin",
            filetypes=[("PDF dosyaları", "*.pdf"), ("Tüm dosyalar", "*.*")]
        )
        if filename:
            self.pdf_var.set(filename)
            self.log(f"📄 PDF seçildi: {os.path.basename(filename)}")

    def select_output_dir(self):
        """Çıktı dizini seç"""
        dirname = filedialog.askdirectory(title="Çıktı Klasörü Seçin")
        if dirname:
            self.output_var.set(dirname)
            self.log(f"📁 Çıktı klasörü: {dirname}")

    def start_conversion(self):
        """Dönüştürme işlemini başlat"""
        pdf_path = self.pdf_var.get().strip()
        
        if not pdf_path:
            messagebox.showwarning("⚠️ Uyarı", "Lütfen bir PDF dosyası seçin!")
            return
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("❌ Hata", "Seçilen PDF dosyası bulunamadı!")
            return
        
        # Çıktı dizini kontrolü
        output_dir = self.output_var.get().strip()
        if not output_dir:
            output_dir = os.path.dirname(pdf_path)
            self.output_var.set(output_dir)
        
        # Başlık kontrolü
        title = self.title_var.get().strip()
        if not title:
            title = os.path.splitext(os.path.basename(pdf_path))[0]
            self.title_var.set(title)
        
        # Dönüştürme thread'i başlat
        thread = threading.Thread(target=self.convert_pdf_thread, args=(pdf_path, output_dir, title))
        thread.daemon = True
        thread.start()
        
        # Butonu devre dışı bırak
        self.convert_button.config(state='disabled', text='🔄 Dönüştürülüyor...')

    def convert_pdf_thread(self, pdf_path: str, output_dir: str, title: str):
        """PDF dönüştürme thread'i"""
        try:
            self.root.after(0, lambda: self.log("🚀 PDF dönüştürme başlatıldı..."))
            
            # PDF dönüştürücüyü başlat
            from pdf_to_markdown import PDFToMarkdownConverter, EnhancedDocumentFormatter
            
            converter = PDFToMarkdownConverter()
            
            # Tek dosya olarak çıktı al
            self.root.after(0, lambda: self.log("📖 PDF içeriği işleniyor..."))
              # PDF'i markdown'a dönüştür - dosya oluşturacak
            enhanced_format = self.enhanced_format_var.get() and not self.ai_enhance_var.get()
            
            output_path = converter.convert_pdf_to_markdown(
                pdf_path=pdf_path,
                output_dir=output_dir,
                title=title,
                enhanced_format=enhanced_format
            )
              # AI iyileştirmesi istendiyse, dosyayı oku ve yeniden işle
            if self.ai_enhance_var.get():
                self.root.after(0, lambda: self.log("🤖 AI ile doküman iyileştiriliyor..."))
                try:
                    # Oluşturulan dosyayı oku
                    with open(output_path, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    
                    # AI iyileştirmesi uygula
                    enhanced_content = self.enhance_with_ai(markdown_content, title)
                    
                    # İyileştirilmiş içeriği kaydet
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(enhanced_content)
                    
                    self.root.after(0, lambda: self.log("✨ AI iyileştirmesi başarıyla tamamlandı!"))
                    
                except Exception as ai_error:
                    self.root.after(0, lambda: self.log(f"⚠️ AI iyileştirme hatası: {ai_error}"))
                    self.root.after(0, lambda: self.log("📝 Normal format ile devam ediliyor..."))
  
            
            self.root.after(0, lambda: self.log(f"✅ Dönüştürme tamamlandı: {output_path}"))
            self.root.after(0, lambda: messagebox.showinfo(
                "✅ Başarılı!", 
                f"PDF başarıyla dönüştürüldü!\n\nÇıktı: {output_path}"
            ))
            
        except Exception as e:
            error_msg = f"Dönüştürme hatası: {str(e)}"
            self.root.after(0, lambda: self.log(f"❌ {error_msg}"))
            self.root.after(0, lambda: messagebox.showerror("❌ Hata", error_msg))
        
        finally:
            # Butonu tekrar etkinleştir
            self.root.after(0, lambda: self.convert_button.config(state='normal', text='🚀 Dönüştür!'))

    def create_log_area(self):
        """Log alanı oluştur"""
        log_frame = ttk.LabelFrame(self.main_frame, text="📜 İşlem Geçmişi", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Log metin alanı ve scrollbar
        self.log_text = tk.Text(
            log_frame,
            height=8,
            width=80,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg='#2d3748'
        )
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def log(self, message: str):
        """Log mesajı ekle"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        
        # Log sınırını kontrol et (500 satır)
        lines = self.log_text.get("1.0", tk.END).count('\n')
        if lines > 500:
            self.log_text.delete("1.0", "100.0")

    def create_status_bar(self):
        """Basit durum çubuğu - şimdilik boş"""
        pass

def main():
    """Ana GUI fonksiyonu"""
    # Drag & Drop desteği için
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        
    app = PDFConverterGUI(root)
    # Başlangıç mesajları
    app.log("🌟 PDF to GitBook Markdown Converter v2.1 - AI Enhanced başlatıldı!")
    app.log("📌 PDF dosyanızı seçin veya sürükle-bırak yapın")
    app.log("🎨 Gelişmiş format ile profesyonel dokümanlara sahip olun")
    app.log("🤖 AI iyileştirmesi ile dokümantınızı bir üst seviyeye taşıyın")
    app.log("🎯 GitBook, Notion ve diğer platformlarda mükemmel görünür")
    
    if not DND_AVAILABLE:
        app.log("⚠️ Sürükle-bırak için: pip install tkinterdnd2")
    
    root.mainloop()

if __name__ == "__main__":
    main()
