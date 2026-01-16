"""
Script to build executable installer for PDFPageRemover
"""
import os
import shutil
import subprocess
import sys

def create_icon():
    """Create ICO file from PNG icon"""
    if os.path.exists("icon.ico"):
        print("✅ الأيقونة موجودة بالفعل")
        return True
    
    try:
        from PIL import Image
        
        png_path = "icons/file.png"
        if not os.path.exists(png_path):
            print(f"⚠️ ملف الأيقونة غير موجود: {png_path}")
            return False
        
        img = Image.open(png_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # إنشاء أحجام متعددة
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        images = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
        
        img.save("icon.ico", format='ICO', sizes=[(img.width, img.height) for img in images])
        print("✅ تم إنشاء الأيقونة: icon.ico")
        return True
    except Exception as e:
        print(f"⚠️ لم يتم إنشاء الأيقونة: {e}")
        return False

def build_executable():
    """Build executable using PyInstaller"""
    
    # إنشاء الأيقونة أولاً
    create_icon()
    
    # تنظيف المجلدات القديمة
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # استخدام ملف .spec
    if not os.path.exists("PDFPageRemover.spec"):
        print("❌ ملف PDFPageRemover.spec غير موجود!")
        return False
    
    cmd = ["pyinstaller", "--clean", "PDFPageRemover.spec"]
    
    print("🚀 بدء بناء الملف القابل للتنفيذ...")
    print(f"الأمر: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("✅ تم البناء بنجاح!")
        
        exe_path = os.path.join("dist", "PDFPageRemover.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n📁 الملف موجود في: {os.path.abspath(exe_path)}")
            print(f"📦 الحجم: {size_mb:.2f} ميجابايت")
        else:
            print(f"\n⚠️ الملف غير موجود في: {exe_path}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في البناء:")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except FileNotFoundError:
        print("❌ PyInstaller غير مثبت!")
        print("قم بتثبيته باستخدام: pip install pyinstaller")
        return False

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
