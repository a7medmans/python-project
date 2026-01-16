# دليل بناء نسخة قابلة للتثبيت

## المتطلبات

1. تثبيت Python 3.8 أو أحدث
2. تثبيت المكتبات المطلوبة:
```bash
pip install -r requirements.txt
```

## طريقة البناء

### الطريقة الأولى: استخدام السكريبت التلقائي
```bash
python build_installer.py
```

### الطريقة الثانية: استخدام PyInstaller مباشرة
```bash
pyinstaller PDFPageRemover.spec
```

### الطريقة الثالثة: استخدام أوامر PyInstaller مباشرة
```bash
pyinstaller --name=PDFPageRemover --onefile --windowed --add-data="icons;icons" PDFPageRemover.py
```

## النتيجة

بعد البناء، ستجد الملف القابل للتنفيذ في مجلد `dist`:
- `dist/PDFPageRemover.exe` - الملف القابل للتنفيذ

## توزيع البرنامج

يمكنك توزيع ملف `PDFPageRemover.exe` مباشرة. المستخدمون لا يحتاجون تثبيت Python أو أي مكتبات.

## ملاحظات

- حجم الملف النهائي قد يكون كبيراً (حوالي 50-100 ميجابايت) بسبب تضمين جميع المكتبات
- يمكن تقليل الحجم باستخدام UPX (مفعل افتراضياً)
- لإضافة أيقونة للبرنامج، أضف `--icon=icon.ico` في الأمر

## استكشاف الأخطاء

إذا واجهت مشاكل:
1. تأكد من تثبيت جميع المكتبات: `pip install -r requirements.txt`
2. تأكد من تثبيت PyInstaller: `pip install pyinstaller`
3. جرب حذف مجلدات `build` و `dist` و `__pycache__` وإعادة البناء
