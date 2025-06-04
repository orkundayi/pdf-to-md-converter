@echo off
echo PDF to GitBook Markdown Converter Kurulum
echo ==========================================

echo.
echo Python versiyonu kontrol ediliyor...
python --version
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadi! Lutfen Python 3.8+ yukleyin.
    pause
    exit /b 1
)

echo.
echo Gerekli paketler yukleniyor...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo HATA: Paket yukleme basarisiz!
    pause
    exit /b 1
)

echo.
echo Kurulum tamamlandi!
echo.
echo Kullanim:
echo   python main.py dosya.pdf
echo   python main.py dosya.pdf -o cikti_dizini
echo   python main.py dosya.pdf --create-gitbook
echo.
echo Test icin:
echo   python test.py
echo.
pause
