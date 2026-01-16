@echo off
chcp 65001 >nul
echo ========================================
echo   إنشاء ملف تثبيت احترافي - PDFPageRemover
echo ========================================
echo.

REM التحقق من وجود الملف القابل للتنفيذ
if not exist "dist\PDFPageRemover.exe" (
    echo ❌ الملف القابل للتنفيذ غير موجود!
    echo.
    echo قم ببناء الملف أولاً باستخدام:
    echo python build_installer.py
    echo.
    pause
    exit /b 1
)

REM التحقق من وجود الأيقونة
if not exist "icon.ico" (
    echo ⚠️ ملف الأيقونة غير موجود، سيتم إنشاؤه...
    python create_icon.py
)

REM التحقق من وجود Inno Setup
where iscc >nul 2>&1
if errorlevel 1 (
    echo ❌ Inno Setup غير مثبت أو غير موجود في PATH
    echo.
    echo يرجى تثبيت Inno Setup من:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo بعد التثبيت، أضف المسار إلى PATH:
    echo C:\Program Files (x86)\Inno Setup 6
    echo.
    echo أو استخدم المسار الكامل في الأمر التالي:
    echo "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
    echo.
    pause
    exit /b 1
)

echo ✅ Inno Setup موجود
echo.

REM إنشاء مجلد الإخراج
if not exist "installer_output" mkdir installer_output

echo 🔨 بدء إنشاء ملف التثبيت...
echo.

REM بناء ملف التثبيت
iscc installer.iss

if errorlevel 1 (
    echo.
    echo ❌ فشل إنشاء ملف التثبيت
    echo.
    echo تحقق من:
    echo 1. وجود ملف installer.iss
    echo 2. وجود ملف dist\PDFPageRemover.exe
    echo 3. وجود ملف icon.ico
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ تم إنشاء ملف التثبيت بنجاح!
echo.
echo 📦 الملف: installer_output\PDFPageRemover_Setup_v1.0.exe
echo.
echo يمكنك الآن توزيع هذا الملف للمستخدمين
echo ========================================
echo.

REM فتح مجلد الإخراج
explorer installer_output

pause
