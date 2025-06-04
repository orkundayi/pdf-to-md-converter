#!/usr/bin/env python3
"""
PDF to Markdown Converter - Modern GUI
GitBook uyumlu, sayfa bazlı dönüştürme özelliği ile
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from pdf_to_markdown import PDFToMarkdownConverter

class PDFConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to GitBook Markdown Converter v2.0")
        self.root.geometry("750x700")
        self.root.configure(bg='#f0f0f0')
        
        # Ana frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Başlık
        self.create_header()
        
        # PDF seçme alanı
        self.create_file_selection_area()
        
        # Ayarlar
        self.create_settings_area()
        
        # Dönüştürme seçenekleri (YENİ!)
        self.create_conversion_options()
        
        # Dönüştür butonu
        self.create_convert_button()
        
        # Log alanı
        self.create_log_area()
        
        # Durum çubuğu
        self.create_status_bar()
        
        # Grid ağırlıkları
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.converter = PDFToMarkdownConverter()
        self.selected_pdf = None
    
    def create_header(self):
        """Başlık alanı"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="📚 PDF to GitBook Markdown Converter v2.0",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="GitBook uyumlu • Sayfa bazlı bölümleme desteği",
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
        """Basit sürükle-bırak setup"""
        def on_click(event):
            self.select_pdf_file()
        
        def on_enter(event):
            self.drop_area.configure(bg='#d1e7dd')
        
        def on_leave(event):
            self.drop_area.configure(bg='#e8f4fd')
        
        self.drop_area.bind('<Button-1>', on_click)
        self.drop_area.bind('<Enter>', on_enter)
        self.drop_area.bind('<Leave>', on_leave)
    
    def create_settings_area(self):
        """Ayarlar alanı"""
        settings_frame = ttk.LabelFrame(self.main_frame, text="⚙️ Temel Ayarlar", padding="15")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Başlık
        ttk.Label(settings_frame, text="Döküman Başlığı:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(settings_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        
        # Çıktı dizini
        ttk.Label(settings_frame, text="Çıktı Klasörü:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.output_var = tk.StringVar()
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
        """Dönüştürme seçenekleri - YENİ ÖZELLIK"""
        options_frame = ttk.LabelFrame(self.main_frame, text="🔧 Dönüştürme Seçenekleri", padding="15")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Dönüştürme modu
        mode_label = ttk.Label(options_frame, text="Dönüştürme Modu:", font=('Arial', 10, 'bold'))
        mode_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Radio button'lar
        self.conversion_mode = tk.StringVar(value="pages")  # Sayfa bazlı varsayılan
        
        # Tek dosya modu
        self.single_radio = ttk.Radiobutton(
            options_frame,
            text="📄 Tek Markdown Dosyası (Küçük PDF'ler için)",
            variable=self.conversion_mode,
            value="single"
        )
        self.single_radio.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Sayfa bazlı mod (ÖNERİLEN)
        self.pages_radio = ttk.Radiobutton(
            options_frame,
            text="📚 Sayfa Bazlı Bölümleme (ÖNERİLEN - GitBook için ideal)",
            variable=self.conversion_mode,
            value="pages"
        )
        self.pages_radio.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # Açıklama
        desc_label = ttk.Label(
            options_frame,
            text="💡 Sayfa bazlı mod: Her PDF sayfası ayrı Markdown dosyası olur.\n"
                 "GitBook'ta uzun içeriklerin kod bloğu olarak algılanmasını önler.",
            font=('Arial', 9),
            foreground='#0066cc'
        )
        desc_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        # GitBook seçeneği
        self.gitbook_var = tk.BooleanVar(value=True)
        self.gitbook_check = ttk.Checkbutton(
            options_frame,
            text="✅ GitBook formatında oluştur (SUMMARY.md ve README.md dahil)",
            variable=self.gitbook_var
        )
        self.gitbook_check.grid(row=4, column=0, sticky=tk.W)
        
        options_frame.columnconfigure(0, weight=1)
    
    def create_convert_button(self):
        """Dönüştür butonu"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        self.convert_button = ttk.Button(
            button_frame,
            text="🚀 Dönüştürmeyi Başlat",
            command=self.convert_pdf
        )
        self.convert_button.pack()
        self.convert_button.configure(state='disabled')
        
        # İpucu
        tip_label = ttk.Label(
            button_frame,
            text="💡 Büyük PDF'ler için mutlaka 'Sayfa Bazlı Bölümleme' kullanın",
            font=('Arial', 9),
            foreground='#ff8c00'
        )
        tip_label.pack(pady=(10, 0))
    
    def create_log_area(self):
        """Log alanı"""
        log_frame = ttk.LabelFrame(self.main_frame, text="📊 İşlem Durumu", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            width=80,
            font=('Consolas', 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Temizle butonu
        clear_button = ttk.Button(log_frame, text="🗑️ Temizle", command=self.clear_log)
        clear_button.pack(anchor='e', pady=(5, 0))
        
        self.main_frame.rowconfigure(5, weight=1)
    
    def create_status_bar(self):
        """Durum çubuğu"""
        self.status_var = tk.StringVar()
        self.status_var.set("🔄 Hazır - PDF dosyanızı seçin")
        
        status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding="5"
        )
        status_bar.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E))
    
    def clear_log(self):
        """Log temizle"""
        self.log_text.delete(1.0, tk.END)
        self.log("🧹 Log temizlendi")
    
    def select_pdf_file(self):
        """PDF dosyası seçme"""
        file_path = filedialog.askopenfilename(
            title="PDF Dosyası Seçin",
            filetypes=[("PDF dosyaları", "*.pdf"), ("Tüm dosyalar", "*.*")]
        )
        
        if file_path:
            if not file_path.lower().endswith('.pdf'):
                messagebox.showwarning("⚠️ Uyarı", "Lütfen sadece PDF dosyalarını seçin!")
                return
            
            if not os.path.exists(file_path):
                messagebox.showerror("❌ Hata", "Seçilen dosya bulunamadı!")
                return
            
            self.process_selected_file(file_path)
    
    def process_selected_file(self, file_path):
        """Seçilen dosyayı işle"""
        self.selected_pdf = file_path
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        # Dosya bilgisi
        self.file_label.config(text=f"✅ {filename} ({file_size:.1f} MB)")
        
        # Otomatik başlık
        if not self.title_var.get():
            title = Path(file_path).stem.replace('_', ' ').replace('-', ' ').title()
            self.title_var.set(title)
        
        # Otomatik çıktı dizini
        if not self.output_var.get():
            output_dir = os.path.dirname(file_path)
            self.output_var.set(output_dir)
        
        # Büyük dosyalar için sayfa bazlı öner
        if file_size > 5:  # 5MB'den büyükse
            self.conversion_mode.set("pages")
            self.log(f"📊 Büyük dosya tespit edildi ({file_size:.1f} MB)")
            self.log("💡 Sayfa bazlı dönüştürme önerilir")
        
        # Butonu aktif et
        self.convert_button.configure(state='normal')
        self.status_var.set(f"✅ PDF seçildi: {filename}")
        self.log(f"📄 PDF yüklendi: {filename} ({file_size:.1f} MB)")
    
    def select_output_dir(self):
        """Çıktı dizini seçme"""
        dir_path = filedialog.askdirectory(title="Çıktı Klasörü Seçin")
        if dir_path:
            self.output_var.set(dir_path)
            self.log(f"📁 Çıktı klasörü: {os.path.basename(dir_path)}")
    
    def log(self, message):
        """Log mesajı ekle"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        
        self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def convert_pdf(self):
        """PDF dönüştürme başlat"""
        if not self.selected_pdf:
            messagebox.showerror("❌ Hata", "Lütfen PDF dosyası seçin!")
            return
        
        if not self.title_var.get().strip():
            messagebox.showwarning("⚠️ Uyarı", "Lütfen döküman başlığı girin!")
            return
        
        # Thread ile dönüştür
        thread = threading.Thread(target=self._convert_thread)
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self):
        """Dönüştürme thread'i"""
        try:
            # UI'yi devre dışı bırak
            self.root.after(0, lambda: self.convert_button.configure(state='disabled', text="⏳ Dönüştürülüyor..."))
            
            # Parametreler
            pdf_path = self.selected_pdf
            output_dir = self.output_var.get() or os.path.dirname(pdf_path)
            title = self.title_var.get().strip()
            mode = self.conversion_mode.get()
            
            self.root.after(0, lambda: self.log("🚀 Dönüştürme başladı..."))
            self.root.after(0, lambda: self.log(f"📂 Çıktı: {output_dir}"))
            self.root.after(0, lambda: self.log(f"🔧 Mod: {'Sayfa Bazlı' if mode == 'pages' else 'Tek Dosya'}"))
            
            # Converter
            self.converter = PDFToMarkdownConverter()
            
            # Print capture setup
            original_print = print
            def capture_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                if message.strip():
                    self.root.after(0, lambda: self.log(f"ℹ️ {message}"))
                original_print(*args, **kwargs)
            
            import builtins
            builtins.print = capture_print
            
            try:
                if mode == "pages":
                    # Sayfa bazlı dönüştürme
                    self.root.after(0, lambda: self.log("📚 Sayfa bazlı dönüştürme başlatılıyor..."))
                    result_files = self.converter.convert_pdf_to_pages(
                        pdf_path=pdf_path,
                        output_dir=output_dir,
                        title=title
                    )
                    
                    # Sonuç
                    result_count = len(result_files)
                    main_folder = os.path.join(output_dir, f"{title}_pages")
                    
                    self.root.after(0, lambda: self.log(f"✅ {result_count} sayfa dönüştürüldü!"))
                    self.root.after(0, lambda: self.log(f"📁 Klasör: {main_folder}"))
                    
                    # Başarı mesajı
                    self.root.after(0, lambda: messagebox.showinfo(
                        "🎉 Başarılı!",
                        f"PDF başarıyla {result_count} Markdown dosyasına dönüştürüldü!\n\n"
                        f"Klasör: {main_folder}\n\n"
                        f"GitBook için SUMMARY.md dosyasını kullanın.\n\n"
                        f"Klasörü açmak ister misiniz?"
                    ))
                    
                    # Klasörü aç
                    self.root.after(0, lambda: self._open_folder(main_folder))
                    
                else:
                    # Tek dosya dönüştürme
                    self.root.after(0, lambda: self.log("📄 Tek dosya dönüştürme..."))
                    result_file = self.converter.convert_pdf_to_markdown(
                        pdf_path=pdf_path,
                        output_dir=output_dir,
                        title=title
                    )
                    
                    # GitBook summary
                    if self.gitbook_var.get():
                        from pdf_to_markdown import create_gitbook_summary
                        summary_file = create_gitbook_summary([result_file], output_dir)
                        self.root.after(0, lambda: self.log(f"📚 SUMMARY.md: {summary_file}"))
                    
                    self.root.after(0, lambda: self.log("✅ Dönüştürme tamamlandı!"))
                    self.root.after(0, lambda: self.log(f"📄 Dosya: {result_file}"))
                    
                    # Başarı mesajı
                    self.root.after(0, lambda: messagebox.showinfo(
                        "🎉 Başarılı!",
                        f"PDF başarıyla Markdown'a dönüştürüldü!\n\nDosya: {result_file}\n\nDosyayı açmak ister misiniz?"
                    ))
                    
                    # Dosyayı aç
                    self.root.after(0, lambda: self._open_file(result_file))
                
                self.root.after(0, lambda: self.status_var.set("🎉 Dönüştürme başarıyla tamamlandı!"))
                
            finally:
                builtins.print = original_print
                
        except Exception as e:
            error_msg = f"❌ Hata: {str(e)}"
            self.root.after(0, lambda: self.log(error_msg))
            self.root.after(0, lambda: self.status_var.set("💥 Dönüştürme hatası!"))
            self.root.after(0, lambda: messagebox.showerror("❌ Hata", str(e)))
        
        finally:
            # UI'yi tekrar aktif et
            self.root.after(0, lambda: self.convert_button.configure(state='normal', text="🚀 Dönüştürmeyi Başlat"))
    
    def _open_folder(self, folder_path):
        """Klasörü aç"""
        if messagebox.askyesno("Klasör Aç", "Oluşturulan klasörü açmak ister misiniz?"):
            try:
                os.startfile(folder_path)  # Windows
            except:
                self.log("📁 Klasör konumunu manuel olarak açın")
    
    def _open_file(self, file_path):
        """Dosyayı aç"""
        if messagebox.askyesno("Dosya Aç", "Oluşturulan dosyayı açmak ister misiniz?"):
            try:
                os.startfile(file_path)  # Windows
            except:
                self.log("📁 Dosya konumunu manuel olarak açın")

def main():
    """Ana GUI fonksiyonu"""
    root = tk.Tk()
    app = PDFConverterGUI(root)
    
    # Başlangıç mesajları
    app.log("🌟 PDF to GitBook Markdown Converter v2.0 başlatıldı!")
    app.log("📌 PDF dosyanızı seçin ve dönüştürme modunu belirleyin")
    app.log("💡 Büyük PDF'ler için 'Sayfa Bazlı Bölümleme' kullanın")
    app.log("🎯 GitBook'ta uzun içeriklerin kod bloğu olmasını önler")
    
    root.mainloop()

if __name__ == "__main__":
    main()
