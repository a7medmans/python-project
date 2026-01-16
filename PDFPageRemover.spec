# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# جمع البيانات والملفات الثنائية
datas = [('icons', 'icons')]
binaries = []
hiddenimports = [
    'PIL._tkinter_finder', 
    'fitz', 
    'image_ops', 
    'pdf_ops',
    'html',  # مطلوب لـ PyMuPDF
    'html.parser',  # مطلوب لـ PyMuPDF
]

# جمع فقط ما نحتاجه من PIL (تقليل الحجم)
try:
    tmp_ret = collect_all('PIL')
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]
except:
    pass

# جمع فقط ما نحتاجه من fitz (تقليل الحجم)
try:
    tmp_ret = collect_all('fitz')
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]
except:
    pass

# استبعاد المكتبات غير الضرورية لتقليل الحجم
# ملاحظة: لا نستبعد 'html' أو 'xml' لأن PyMuPDF يحتاجها
excludes = [
    'matplotlib', 'numpy', 'scipy', 'pandas', 'jupyter',
    'IPython', 'pytest', 'setuptools', 'distutils',
    'email', 'http', 'urllib3', 'requests',
    'sqlite3', 'xmlrpc',
]

a = Analysis(
    ['PDFPageRemover.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=2,  # تحسين الكود
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# تحديد مسار الأيقونة
icon_path = 'icon.ico' if os.path.exists('icon.ico') else None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDFPageRemover',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # إزالة رموز التصحيح
    upx=True,  # ضغط UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
