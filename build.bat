@echo off
chcp 65001 >nul
echo ========================================
echo   بناء نسخة قابلة للتثبيت - PDFPageRemover
echo ========================================
echo.

REM التحقق من تثبيت Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    pause
    exit /b 1
)

echo ✅ Python موجود
echo.

REM تثبيت/تحديث المكتبات
echo 📦 تثبيت المكتبات المطلوبة...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ فشل تثبيت المكتبات
    pause
    exit /b 1
)

echo.
echo 🔨 بدء بناء الملف القابل للتنفيذ...
echo.

REM بناء الملف
python build_installer.py

if errorlevel 1 (
    echo.
    echo ❌ فشل البناء
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ تم البناء بنجاح!
echo 📁 الملف موجود في مجلد: dist\PDFPageRemover.exe
echo ========================================
echo.
pause
