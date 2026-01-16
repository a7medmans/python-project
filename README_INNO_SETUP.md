# دليل إنشاء ملف تثبيت احترافي باستخدام Inno Setup

## الخطوة 1: تثبيت Inno Setup

1. قم بتحميل Inno Setup من الموقع الرسمي:
   - **الرابط:** https://jrsoftware.org/isdl.php
   - اختر النسخة المناسبة (Inno Setup 6)

2. قم بتثبيت البرنامج (افتراضي: `C:\Program Files (x86)\Inno Setup 6`)

3. **إضافة إلى PATH (اختياري لكن موصى به):**
   - افتح "Environment Variables"
   - أضف `C:\Program Files (x86)\Inno Setup 6` إلى PATH
   - أو استخدم المسار الكامل في الأوامر

## الخطوة 2: إنشاء ملف التثبيت

### الطريقة السريعة:
```bash
create_installer.bat
```

### الطريقة اليدوية:
```bash
iscc installer.iss
```

أو باستخدام المسار الكامل:
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## الخطوة 3: النتيجة

بعد البناء، ستجد ملف التثبيت في:
- **`installer_output/PDFPageRemover_Setup_v1.0.exe`**

## ميزات ملف التثبيت

✅ **واجهة احترافية** - معالج تثبيت حديث
✅ **دعم اللغة العربية** - واجهة عربية كاملة
✅ **اختصارات** - سطح المكتب، قائمة Start، Quick Launch
✅ **إلغاء التثبيت** - إزالة كاملة من النظام
✅ **تسجيل في النظام** - معلومات التطبيق في Registry
✅ **أيقونة مخصصة** - أيقونة البرنامج في كل مكان

## تخصيص ملف التثبيت

يمكنك تعديل ملف `installer.iss` لتخصيص:

### معلومات التطبيق:
```iss
#define MyAppName "PDFPageRemover"
#define MyAppVersion "1.0"
#define MyAppPublisher "اسمك"
#define MyAppDescription "وصف التطبيق"
```

### مجلد التثبيت:
```iss
DefaultDirName={autopf}\{#MyAppName}  ; Program Files
DefaultDirName={localappdata}\{#MyAppName}  ; AppData\Local
```

### الصلاحيات:
```iss
PrivilegesRequired=lowest  ; بدون صلاحيات إدارية
PrivilegesRequired=admin  ; يحتاج صلاحيات إدارية
```

### الضغط:
```iss
Compression=lzma2  ; أفضل ضغط (أبطأ)
Compression=zip    ; ضغط أسرع (حجم أكبر)
```

## استكشاف الأخطاء

### المشكلة: "iscc غير موجود"
**الحل:**
1. تأكد من تثبيت Inno Setup
2. أضف المسار إلى PATH
3. أو استخدم المسار الكامل

### المشكلة: "لا يمكن العثور على الملفات"
**الحل:**
- تأكد من وجود `dist\PDFPageRemover.exe`
- تأكد من وجود `icon.ico`
- تحقق من المسارات في ملف `installer.iss`

### المشكلة: "خطأ في الترجمة"
**الحل:**
- تأكد من وجود ملف الترجمة العربية في:
  `C:\Program Files (x86)\Inno Setup 6\Languages\Arabic.isl`
- إذا لم يكن موجوداً، قم بتحميله من موقع Inno Setup

## نصائح إضافية

1. **اختبار ملف التثبيت:**
   - قم بتشغيل الملف على جهاز نظيف
   - تأكد من عمل جميع الاختصارات
   - اختبر إلغاء التثبيت

2. **توقيع الملف (اختياري):**
   - يمكنك توقيع ملف التثبيت بـ Code Signing Certificate
   - هذا يزيل تحذيرات Windows Defender

3. **تحديث الإصدار:**
   - غيّر `MyAppVersion` في ملف `.iss`
   - غيّر `AppId` إذا أردت تثبيت منفصل

## الملفات المطلوبة

- ✅ `dist\PDFPageRemover.exe` - الملف القابل للتنفيذ
- ✅ `icon.ico` - أيقونة البرنامج
- ✅ `installer.iss` - ملف إعدادات Inno Setup

## الدعم

للمزيد من المعلومات:
- **وثائق Inno Setup:** https://jrsoftware.org/ishelp/
- **أمثلة:** `C:\Program Files (x86)\Inno Setup 6\Examples`
