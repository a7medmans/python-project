# PowerShell script to create a simple installer package
# This creates a self-extracting archive with installation script

param(
    [string]$OutputName = "PDFPageRemover_Setup"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  إنشاء ملف تثبيت بسيط" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من وجود الملف القابل للتنفيذ
$exePath = "dist\PDFPageRemover.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "❌ الملف القابل للتنفيذ غير موجود: $exePath" -ForegroundColor Red
    Write-Host "قم ببناء الملف أولاً باستخدام: python build_installer.py" -ForegroundColor Yellow
    exit 1
}

# إنشاء مجلد التثبيت
$installerDir = "installer_output"
if (-not (Test-Path $installerDir)) {
    New-Item -ItemType Directory -Path $installerDir | Out-Null
}

# نسخ الملف
Write-Host "📦 نسخ الملفات..." -ForegroundColor Green
Copy-Item $exePath "$installerDir\PDFPageRemover.exe" -Force

# إنشاء ملف README
$readmeContent = @"
PDFPageRemover - أداة معالجة ملفات PDF

التثبيت:
1. انسخ ملف PDFPageRemover.exe إلى أي مجلد تريده
2. شغّل الملف مباشرة (لا يحتاج تثبيت)

أو يمكنك:
- إنشاء اختصار على سطح المكتب
- إضافته إلى قائمة Start

المتطلبات:
- Windows 7 أو أحدث
- لا يحتاج تثبيت Python أو أي مكتبات إضافية

الإصدار: 1.0
"@

$readmeContent | Out-File "$installerDir\README.txt" -Encoding UTF8

# إنشاء ملف ZIP
Write-Host "📦 إنشاء ملف ZIP..." -ForegroundColor Green
$zipPath = "$installerDir\$OutputName.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path "$installerDir\PDFPageRemover.exe", "$installerDir\README.txt" -DestinationPath $zipPath -Force

Write-Host ""
Write-Host "✅ تم إنشاء ملف التثبيت!" -ForegroundColor Green
Write-Host "📁 الموقع: $zipPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "ملاحظة: هذا ملف ZIP بسيط. للحصول على installer احترافي، قم بتثبيت Inno Setup" -ForegroundColor Yellow
Write-Host "من: https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
Write-Host ""
