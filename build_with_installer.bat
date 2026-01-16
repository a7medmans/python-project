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
echo ✅ تم بناء الملف القابل للتنفيذ!
echo.

REM التحقق من وجود Inno Setup
where iscc >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Inno Setup غير مثبت
    echo.
    echo 📦 إنشاء ملف ZIP بسيط بدلاً من ذلك...
    echo.
    powershell -ExecutionPolicy Bypass -File create_simple_installer.ps1
    if errorlevel 1 (
        echo ❌ فشل إنشاء ملف ZIP
        pause
        exit /b 1
    )
    echo.
    echo ========================================
    echo ✅ تم البناء بنجاح!
    echo.
    echo 📁 الملف القابل للتنفيذ: dist\PDFPageRemover.exe
    echo 📦 ملف التثبيت (ZIP): installer_output\PDFPageRemover_Setup.zip
    echo.
    echo 💡 للحصول على installer احترافي، قم بتثبيت Inno Setup من:
    echo    https://jrsoftware.org/isdl.php
    echo ========================================
    echo.
    pause
    exit /b 0
)

echo 🔨 بدء إنشاء ملف التثبيت الاحترافي...
echo.

REM إنشاء مجلد الإخراج
if not exist "installer_output" mkdir installer_output

REM بناء ملف التثبيت
iscc installer.iss

if errorlevel 1 (
    echo.
    echo ❌ فشل إنشاء ملف التثبيت
    echo.
    echo 📦 إنشاء ملف ZIP بسيط بدلاً من ذلك...
    powershell -ExecutionPolicy Bypass -File create_simple_installer.ps1
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ تم البناء بنجاح!
echo.
echo 📁 الملف القابل للتنفيذ: dist\PDFPageRemover.exe
echo 📦 ملف التثبيت: installer_output\PDFPageRemover_Setup.exe
echo ========================================
echo.
pause
