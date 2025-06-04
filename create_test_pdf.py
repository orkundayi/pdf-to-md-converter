"""
Test PDF dosyası oluşturucu
Bu script test amaçlı basit bir PDF dosyası oluşturur
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, blue, red
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_test_pdf():
    """Test PDF dosyası oluştur"""
    filename = "test_document.pdf"
    
    # PDF oluştur
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Başlık
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(blue)
    c.drawString(50, height - 80, "Test Document")
    
    # Alt başlık
    c.setFont("Helvetica", 16)
    c.setFillColor(black)
    c.drawString(50, height - 120, "PDF to Markdown Converter Test")
    
    # İçerik
    y_position = height - 160
    content = [
        "Introduction",
        "",
        "This is a test document created for testing the PDF to Markdown converter.",
        "It contains various formatting elements to test the conversion process.",
        "",
        "Chapter 1: Basic Features",
        "",
        "• Bullet point 1",
        "• Bullet point 2", 
        "• Bullet point 3",
        "",
        "Chapter 2: Advanced Features",
        "",
        "This chapter demonstrates more complex formatting and structures.",
        "It includes tables, code blocks, and other elements.",
        "",
        "Table Example:",
        "Name       | Age | City",
        "John       | 25  | New York",
        "Jane       | 30  | London",
        "",
        "Code Example:",
        "def hello_world():",
        "    print('Hello, World!')",
        "",
        "Conclusion",
        "",
        "This document serves as a comprehensive test for the converter.",
        "It should be converted to well-formatted Markdown."
    ]
    
    c.setFont("Helvetica", 12)
    for line in content:
        if line.startswith("Chapter"):
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(red)
        elif line in ["Introduction", "Conclusion"]:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(blue)
        else:
            c.setFont("Helvetica", 12)
            c.setFillColor(black)
        
        c.drawString(50, y_position, line)
        y_position -= 20
        
        # Yeni sayfa gerekirse
        if y_position < 50:
            c.showPage()
            y_position = height - 50
    
    c.save()
    print(f"✅ Test PDF oluşturuldu: {filename}")
    return filename

if __name__ == "__main__":
    try:
        create_test_pdf()
    except ImportError:
        print("❌ reportlab kütüphanesi bulunamadı. Lütfen yükleyin:")
        print("pip install reportlab")
