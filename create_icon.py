"""
Convert PNG icon to ICO format for the application
"""
from PIL import Image
import os

def create_icon():
    """Create ICO file from PNG icon"""
    # استخدام أيقونة file.png كأيقونة رئيسية
    png_path = "icons/file.png"
    ico_path = "icon.ico"
    
    if not os.path.exists(png_path):
        print(f"❌ ملف الأيقونة غير موجود: {png_path}")
        return False
    
    try:
        # فتح الصورة
        img = Image.open(png_path)
        
        # تحويل إلى RGBA إذا لزم الأمر
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # إنشاء أحجام متعددة للأيقونة (Windows يحتاج أحجام مختلفة)
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        images = []
        
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            images.append(resized)
        
        # حفظ كملف ICO
        img.save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in images])
        print(f"✅ تم إنشاء الأيقونة: {ico_path}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الأيقونة: {e}")
        return False

if __name__ == "__main__":
    create_icon()
