#!/usr/bin/env python3
"""
Basit Tkinter Test
"""
import tkinter as tk
from tkinter import messagebox

print("Test başlatılıyor...")

try:
    root = tk.Tk()
    root.title("Test")
    root.geometry("300x200")
    
    label = tk.Label(root, text="Test başarılı!")
    label.pack(pady=50)
    
    button = tk.Button(root, text="Kapat", command=root.quit)
    button.pack()
    
    print("GUI oluşturuldu, mainloop başlatılıyor...")
    root.mainloop()
    print("GUI kapatıldı.")
    
except Exception as e:
    print(f"Hata: {e}")
    input("Devam etmek için Enter'a basın...")
