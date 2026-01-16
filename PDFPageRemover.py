# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import os
from PIL import Image, ImageTk
import threading

from typing import Optional

import image_ops
import pdf_ops


def load_icon(icon_path, size=(32, 32)):
    try:
        img = Image.open(icon_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"خطأ في تحميل: {icon_path}")
        return None


def show_custom_message(parent, title: str, message: str, msg_type: str = "info"):
    """
    عرض رسالة مخصصة بشكل أفضل وأوضح
    msg_type: "info", "error", "warning", "success"
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.configure(bg="#1e293b")
    dialog.transient(parent)
    dialog.grab_set()
    
    # تحديد الألوان حسب نوع الرسالة
    colors = {
        "info": {"bg": "#3b82f6", "icon": "ℹ️", "title_color": "#ffffff"},
        "error": {"bg": "#ef4444", "icon": "❌", "title_color": "#ffffff"},
        "warning": {"bg": "#f59e0b", "icon": "⚠️", "title_color": "#ffffff"},
        "success": {"bg": "#22c55e", "icon": "✅", "title_color": "#ffffff"}
    }
    
    color_info = colors.get(msg_type, colors["info"])
    
    # رأس الرسالة
    header_frame = tk.Frame(dialog, bg=color_info["bg"], height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text=f"{color_info['icon']} {title}",
        font=("Arial", 18, "bold"),
        fg=color_info["title_color"],
        bg=color_info["bg"],
    )
    title_label.pack(expand=True, pady=20)
    
    # محتوى الرسالة
    content_frame = tk.Frame(dialog, bg="#1e293b", padx=30, pady=40)
    content_frame.pack(fill="both", expand=True)
    
    # نص الرسالة مع دعم السطور المتعددة
    message_label = tk.Label(
        content_frame,
        text=message,
        font=("Arial", 15),
        fg="#e5e7eb",
        bg="#1e293b",
        justify="center",
        wraplength=550,
    )
    message_label.pack(pady=30)
    
    # زر الإغلاق
    button_frame = tk.Frame(content_frame, bg="#1e293b")
    button_frame.pack(pady=25)
    
    ok_button = tk.Button(
        button_frame,
        text="حسناً",
        command=dialog.destroy,
        bg=color_info["bg"],
        fg="white",
        font=("Arial", 16, "bold"),
        padx=60,
        pady=15,
        activebackground=color_info["bg"],
        bd=0,
        cursor="hand2",
        width=12,
        height=2,
    )
    ok_button.pack()
    
    # تحديد حجم النافذة
    dialog.geometry("600x400")
    dialog.resizable(False, False)
    
    # جعل النافذة في المنتصف
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # ربط Enter و Escape
    dialog.bind("<Return>", lambda e: dialog.destroy())
    dialog.bind("<Escape>", lambda e: dialog.destroy())
    ok_button.focus_set()
    
    dialog.wait_window()


def show_custom_input(parent, title: str, prompt: str, initial_value: str = ""):
    """
    عرض نافذة إدخال مخصصة بشكل أفضل وأوضح
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.configure(bg="#1e293b")
    dialog.transient(parent)
    dialog.grab_set()
    
    result = [None]
    
    # رأس النافذة
    header_frame = tk.Frame(dialog, bg="#3b82f6", height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text=f"📝 {title}",
        font=("Arial", 18, "bold"),
        fg="#ffffff",
        bg="#3b82f6",
    )
    title_label.pack(expand=True, pady=20)
    
    # محتوى النافذة
    content_frame = tk.Frame(dialog, bg="#1e293b", padx=40, pady=40)
    content_frame.pack(fill="both", expand=True)
    
    # نص السؤال
    prompt_label = tk.Label(
        content_frame,
        text=prompt,
        font=("Arial", 15),
        fg="#e5e7eb",
        bg="#1e293b",
        justify="right",
    )
    prompt_label.pack(pady=20)
    
    # حقل الإدخال
    input_frame = tk.Frame(content_frame, bg="#1e293b")
    input_frame.pack(pady=20, fill="x")
    
    entry = tk.Entry(
        input_frame,
        font=("Arial", 16),
        bg="#ffffff",
        fg="#1e293b",
        bd=2,
        relief="solid",
        justify="center",
        width=20,
    )
    entry.pack(fill="x", ipady=10)
    entry.insert(0, initial_value)
    entry.select_range(0, tk.END)
    entry.focus_set()
    
    # أزرار التحكم
    button_frame = tk.Frame(content_frame, bg="#1e293b")
    button_frame.pack(pady=30, fill="x", anchor="center")
    
    def confirm():
        result[0] = entry.get()
        dialog.destroy()
    
    def cancel():
        result[0] = None
        dialog.destroy()
    
    ok_button = tk.Button(
        button_frame,
        text="✅ تأكيد",
        command=confirm,
        bg="#22c55e",
        fg="white",
        font=("Arial", 16, "bold"),
        padx=50,
        pady=15,
        activebackground="#16a34a",
        bd=0,
        cursor="hand2",
    )
    ok_button.pack(side="right", padx=10)
    
    cancel_button = tk.Button(
        button_frame,
        text="❌ إلغاء",
        command=cancel,
        bg="#ef4444",
        fg="white",
        font=("Arial", 16, "bold"),
        padx=50,
        pady=15,
        activebackground="#b91c1c",
        bd=0,
        cursor="hand2",
    )
    cancel_button.pack(side="right", padx=10)
    
    # تحديد حجم النافذة
    dialog.geometry("500x400")
    dialog.resizable(False, False)
    
    # جعل النافذة في المنتصف
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
    y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # ربط Enter و Escape
    entry.bind("<Return>", lambda e: confirm())
    dialog.bind("<Escape>", lambda e: cancel())
    
    dialog.wait_window()
    return result[0]


class PDFImageProcessorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 معالج PDF والصور احترافي")
        # فتح في وضع ملء الشاشة
        self.root.state("zoomed")  # Windows
        try:
            self.root.attributes("-zoomed", True)  # Linux
        except:
            pass
        self.root.resizable(True, True)
        # خلفية أوضح وأجمل
        self.root.configure(bg="#1e293b")

        # متغيرات عامة
        self.selected_file = None
        self.pdf_doc = None
        self.total_pages = 0

        self.page_thumbnails = []
        self.canvas_images = []
        self.selected_pages = set()
        self.page_order = []  # ترتيب الصفحات الحالي (0-based indices)
        self.page_rotations = {}  # زوايا التدوير لكل صفحة {page_index: angle}
        self.drag_data = {"item": None, "x": 0, "y": 0, "start_pos": None}  # بيانات السحب
        self.drag_data = {"item": None, "x": 0, "y": 0, "click_time": 0}  # بيانات السحب

        self.zoom_factor = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0

        self.hide_deleted_var = tk.BooleanVar(value=False)

        # متغيرات صور → PDF
        self.selected_images = []
        self.image_thumbnails = []
        self.image_canvas_images = []
        self.selected_image_indices = set()  # فهارس الصور المحددة
        self.image_drag_data = {"item": None, "x": 0, "y": 0, "start_pos": None}  # بيانات السحب
        self.image_layout_var = tk.StringVar(value="one_per_page")  # طريقة الترتيب
        self.images_per_page_var = tk.StringVar(value="4")  # عدد الصور في الصفحة

        # متغيرات استخراج صور
        self.export_format = tk.StringVar(value="png")
        self.export_dpi_var = tk.StringVar(value="600")
        self.export_pages_var = tk.StringVar(value="")

        # متغيرات دمج وتقسيم PDF
        self.selected_pdfs_to_merge = []
        self.split_pdf_file = None

        # تحميل الأيقونات
        self.load_icons()

        self.setup_ui()

    def load_icons(self):
        """تحميل الأيقونات من مجلد icons/"""
        icon_dir = "icons"

        self.icons = {
            'file': load_icon(f"{icon_dir}/file.png", (32, 32)) if os.path.exists(f"{icon_dir}/file.png") else None,
            'save': load_icon(f"{icon_dir}/save.png", (32, 32)) if os.path.exists(f"{icon_dir}/save.png") else None,
            'delete': load_icon(f"{icon_dir}/delete.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/delete.png") else None,
            'select_all': load_icon(f"{icon_dir}/select_all.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/select_all.png") else None,
            'clear': load_icon(f"{icon_dir}/clear.png", (32, 32)) if os.path.exists(f"{icon_dir}/clear.png") else None,
            'invert': load_icon(f"{icon_dir}/invert.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/invert.png") else None,
            'even': load_icon(f"{icon_dir}/even.png", (32, 32)) if os.path.exists(f"{icon_dir}/even.png") else None,
            'odd': load_icon(f"{icon_dir}/odd.png", (32, 32)) if os.path.exists(f"{icon_dir}/odd.png") else None,
            'zoom_in': load_icon(f"{icon_dir}/zoom_in.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/zoom_in.png") else None,
            'zoom_out': load_icon(f"{icon_dir}/zoom_out.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/zoom_out.png") else None,
            'compress': load_icon(f"{icon_dir}/compress.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/compress.png") else None,
            'images': load_icon(f"{icon_dir}/images.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/images.png") else None,
            'up': load_icon(f"{icon_dir}/up.png", (32, 32)) if os.path.exists(f"{icon_dir}/up.png") else None,
            'down': load_icon(f"{icon_dir}/down.png", (32, 32)) if os.path.exists(f"{icon_dir}/down.png") else None,
            'extract': load_icon(f"{icon_dir}/extract.png", (32, 32)) if os.path.exists(
                f"{icon_dir}/extract.png") else None,
        }

    def setup_ui(self):
        # شريط العنوان - لون أوضح وأجمل
        header_frame = tk.Frame(self.root, bg="#3b82f6", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📄 معالج PDF والصور - احترافي",
            font=("Arial", 26, "bold"),
            fg="#ffffff",
            bg="#3b82f6",
        ).pack(expand=True)

        # التبويبات
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "TNotebook",
            background="#1e293b",
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background="#334155",
            foreground="#f1f5f9",
            font=("Arial", 13, "bold"),
            padding=(15, 8),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#3b82f6")],
            foreground=[("selected", "#ffffff")],
        )

        # التبويبات - خلفية أوضح
        self.tab1 = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.tab1, text="✂️ تحرير PDF")

        self.tab2 = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.tab2, text="🖼️ دمج صور")

        self.tab3 = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.tab3, text="📸 استخراج صور")

        self.tab4 = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.tab4, text="🔀 دمج وتقسيم PDF")

        self.tab5 = tk.Frame(self.notebook, bg="#1e293b")
        self.notebook.add(self.tab5, text="🔒 حماية وبيانات")

        self.setup_tab1_pdf_editor()
        self.setup_tab2_images_to_pdf()
        self.setup_tab3_extract_images()
        self.setup_tab4_merge_split()
        self.setup_tab5_security_metadata()

    # ================= TAB 1: تحرير PDF =================
    def setup_tab1_pdf_editor(self):
        file_frame = tk.Frame(self.tab1, relief="ridge", bd=2, bg="#334155")
        file_frame.pack(pady=10, padx=20, fill="x")

        tk.Button(
            file_frame,
            text="اختر ملف PDF",
            command=self.select_pdf,
            bg="#2563eb",
            fg="white",
            font=("Arial", 16, "bold"),
            padx=40,
            pady=15,
            image=self.icons.get('file'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(pady=20, padx=10, side="right")

        self.file_label = tk.Label(
            file_frame,
            text="لم يتم اختيار ملف",
            font=("Arial", 13, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.file_label.pack(pady=5, padx=20, side="right")

        info_frame = tk.Frame(self.tab1, bg="#1e293b")
        info_frame.pack(pady=10, padx=20, fill="x")

        self.pages_label = tk.Label(
            info_frame,
            text="📄 الصفحات: 0",
            font=("Arial", 15, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        )
        self.pages_label.pack(side="right", padx=20)

        self.selected_label = tk.Label(
            info_frame,
            text="🗑️ محدد للحذف: 0 صفحة",
            font=("Arial", 15, "bold"),
            fg="#f97316",
            bg="#1e293b",
        )
        self.selected_label.pack(side="left", padx=20)

        canvas_frame = tk.LabelFrame(
            self.tab1,
            text="📸 انقر على الصور لتحديدها",
            font=("Arial", 16, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        canvas_frame.pack(pady=10, padx=20, fill="both", expand=True)

        scroll_frame = tk.Frame(canvas_frame, bg="#1e293b")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(scroll_frame, bg="#f9fafb", highlightthickness=0)
        self.h_scrollbar = ttk.Scrollbar(
            scroll_frame, orient="horizontal", command=self.canvas.xview
        )
        self.v_scrollbar = ttk.Scrollbar(
            scroll_frame, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(
            xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set
        )

        self.h_scrollbar.pack(side="bottom", fill="x")
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # شريط الأزرار
        btn_frame = tk.Frame(self.tab1, bg="#1e293b")
        btn_frame.pack(pady=8, fill="x")

        top_btns = tk.Frame(btn_frame, bg="#1e293b")
        top_btns.pack(fill="x", pady=3)

        bottom_btns = tk.Frame(btn_frame, bg="#1e293b")
        bottom_btns.pack(fill="x", pady=3)

        left_frame = tk.Frame(top_btns, bg="#1e293b")
        left_frame.pack(side="right", padx=5)

        tk.Button(
            left_frame,
            text="تحديد الكل",
            command=self.select_all_delete,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=12,
            pady=6,
            image=self.icons.get('select_all'),
            compound="left",
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="right", padx=4)

        tk.Button(
            left_frame,
            text="إلغاء الكل",
            command=self.clear_all_selection,
            bg="#eab308",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=12,
            pady=6,
            image=self.icons.get('clear'),
            compound="left",
            activebackground="#ca8a04",
            bd=0,
        ).pack(side="right", padx=4)

        tk.Button(
            left_frame,
            text="عكس التحديد",
            command=self.invert_selection,
            bg="#14b8a6",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=12,
            pady=6,
            image=self.icons.get('invert'),
            compound="left",
            activebackground="#0d9488",
            bd=0,
        ).pack(side="right", padx=4)

        tk.Button(
            left_frame,
            text="زوجية",
            command=self.select_even_pages,
            bg="#a855f7",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=6,
            image=self.icons.get('even'),
            compound="left",
            activebackground="#9333ea",
            bd=0,
        ).pack(side="right", padx=4)

        tk.Button(
            left_frame,
            text="فردية",
            command=self.select_odd_pages,
            bg="#ec4899",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=6,
            image=self.icons.get('odd'),
            compound="left",
            activebackground="#db2777",
            bd=0,
        ).pack(side="right", padx=4)

        # أزرار إعادة ترتيب الصفحات
        reorder_frame = tk.Frame(left_frame, bg="#1e293b")
        reorder_frame.pack(side="right", padx=10)

        tk.Label(
            reorder_frame,
            text="ترتيب:",
            font=("Arial", 11, "bold"),
            bg="#1e293b",
            fg="#9ca3af",
        ).pack(side="right", padx=5)

        tk.Button(
            reorder_frame,
            text="أعلى",
            command=self.move_selected_up,
            bg="#8b5cf6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=6,
            image=self.icons.get('up'),
            compound="left",
            activebackground="#7c3aed",
            bd=0,
        ).pack(side="right", padx=2)

        tk.Button(
            reorder_frame,
            text="أسفل",
            command=self.move_selected_down,
            bg="#8b5cf6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=6,
            image=self.icons.get('down'),
            compound="left",
            activebackground="#7c3aed",
            bd=0,
        ).pack(side="right", padx=2)

        center_frame = tk.Frame(top_btns, bg="#1e293b")
        center_frame.pack(side="right", padx=20)

        tk.Checkbutton(
            center_frame,
            text="🙈 إخفاء المحددة",
            variable=self.hide_deleted_var,
            command=self.display_thumbnails,
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#020617",
            activebackground="#020617",
            font=("Arial", 12, "bold"),
        ).pack(side="right")

        right_frame = tk.Frame(top_btns, bg="#1e293b")
        right_frame.pack(side="left", padx=5)

        tk.Button(
            right_frame,
            text="تكبير",
            command=self.zoom_in,
            bg="#6366f1",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            image=self.icons.get('zoom_in'),
            compound="left",
            activebackground="#4f46e5",
            bd=0,
        ).pack(side="left", padx=4)

        tk.Button(
            right_frame,
            text="تصغير",
            command=self.zoom_out,
            bg="#6366f1",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            image=self.icons.get('zoom_out'),
            compound="left",
            activebackground="#4f46e5",
            bd=0,
        ).pack(side="left", padx=4)

        tk.Button(
            right_frame,
            text="تدوير ⟲",
            command=lambda: self.rotate_selected_pages(-90),
            bg="#0ea5e9",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            compound="left",
            activebackground="#0284c7",
            bd=0,
        ).pack(side="left", padx=4)

        tk.Button(
            right_frame,
            text="تدوير ⟳",
            command=lambda: self.rotate_selected_pages(90),
            bg="#0ea5e9",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            compound="left",
            activebackground="#0284c7",
            bd=0,
        ).pack(side="left", padx=4)

        tk.Button(
            right_frame,
            text="مضغوط",
            command=self.save_compressed_pdf,
            bg="#f97316",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            image=self.icons.get('compress'),
            compound="left",
            activebackground="#ea580c",
            bd=0,
        ).pack(side="left", padx=4)

        # صف الأزرار الثاني
        right_frame2 = tk.Frame(bottom_btns, bg="#1e293b")
        right_frame2.pack(side="left", padx=5)

        self.save_btn = tk.Button(
            right_frame2,
            text="حفظ",
            command=self.save_pdf,
            bg="#22c55e",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            image=self.icons.get('save'),
            compound="left",
            activebackground="#16a34a",
            state="disabled",
            bd=0,
        )
        self.save_btn.pack(side="left", padx=4)

        tk.Button(
            right_frame2,
            text="حفظ المحددة",
            command=self.save_selected_pages,
            bg="#22c55e",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            compound="left",
            activebackground="#16a34a",
            bd=0,
        ).pack(side="left", padx=4)

        tk.Button(
            right_frame2,
            text="➕ إضافة صفحات",
            command=self.add_pages_dialog,
            bg="#10b981",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            compound="left",
            activebackground="#059669",
            bd=0,
        ).pack(side="left", padx=4)

        tk.Button(
            right_frame2,
            text="🔄 حفظ بترتيب جديد",
            command=self.save_reordered_pdf,
            bg="#06b6d4",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=6,
            compound="left",
            activebackground="#0891b2",
            bd=0,
        ).pack(side="left", padx=4)

        # ملاحظة
        note_frame = tk.Frame(self.tab1, bg="#bfdbfe")
        note_frame.pack(fill="x", padx=0, pady=0)

        note_text = (
            "💡 ملاحظة:\n"
            "• ✂️ «حفظ» ينشئ ملف PDF جديد بالصفحات غير المحددة.\n"
            "• 📦 «مضغوط» يحفظ نسخة مضغوطة بالكامل."
        )

        note_label = tk.Label(
            note_frame,
            text=note_text,
            font=("Arial", 13, "bold"),
            fg="#0f172a",
            bg="#bfdbfe",
            anchor="e",
            justify="right",
            wraplength=1300,
        )
        note_label.pack(fill="x", padx=20, pady=6, anchor="e")

        self.progress = ttk.Progressbar(self.tab1, mode="indeterminate")
        self.progress.pack(pady=8, padx=20, fill="x")

    # ================= TAB 2: دمج صور في PDF =================
    def setup_tab2_images_to_pdf(self):
        control_frame = tk.Frame(self.tab2, relief="ridge", bd=2, bg="#334155")
        control_frame.pack(pady=10, padx=20, fill="x")

        tk.Button(
            control_frame,
            text="اختر صور",
            command=self.select_images,
            bg="#2563eb",
            fg="white",
            font=("Arial", 15, "bold"),
            padx=30,
            pady=12,
            image=self.icons.get('images'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(side="right", padx=10, pady=10)

        self.images_label = tk.Label(
            control_frame,
            text="لم يتم اختيار صور",
            font=("Arial", 13, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.images_label.pack(side="right", padx=20, pady=10)

        tk.Button(
            control_frame,
            text="تحديد الكل",
            command=self.select_all_images,
            bg="#a855f7",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('select_all'),
            compound="left",
            activebackground="#9333ea",
            bd=0,
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            control_frame,
            text="إلغاء التحديد",
            command=self.clear_image_selection,
            bg="#eab308",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('clear'),
            compound="left",
            activebackground="#ca8a04",
            bd=0,
        ).pack(side="left", padx=5, pady=10)

        tk.Button(
            control_frame,
            text="مسح",
            command=self.clear_images,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('delete'),
            compound="left",
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="left", padx=10, pady=10)

        canvas_frame = tk.LabelFrame(
            self.tab2,
            text="🖼️ الصور المختارة",
            font=("Arial", 16, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        canvas_frame.pack(pady=10, padx=20, fill="both", expand=True)

        scroll_frame = tk.Frame(canvas_frame, bg="#1e293b")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.images_canvas = tk.Canvas(scroll_frame, bg="#f9fafb", highlightthickness=0)
        images_scrollbar = ttk.Scrollbar(
            scroll_frame, orient="vertical", command=self.images_canvas.yview
        )
        self.images_canvas.configure(yscrollcommand=images_scrollbar.set)

        images_scrollbar.pack(side="right", fill="y")
        self.images_canvas.pack(side="left", fill="both", expand=True)

        # ربط التمرير بالماوس
        def on_images_mousewheel(event):
            self.images_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.images_canvas.bind("<MouseWheel>", on_images_mousewheel)
        self.images_canvas.bind("<Enter>", lambda e: self.images_canvas.focus_set())

        action_frame = tk.Frame(self.tab2, bg="#1e293b")
        action_frame.pack(pady=8, fill="x", padx=20)

        tk.Button(
            action_frame,
            text="أعلى",
            command=self.move_image_up,
            bg="#6366f1",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('up'),
            compound="left",
            activebackground="#4f46e5",
            bd=0,
        ).pack(side="right", padx=5)

        tk.Button(
            action_frame,
            text="أسفل",
            command=self.move_image_down,
            bg="#6366f1",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('down'),
            compound="left",
            activebackground="#4f46e5",
            bd=0,
        ).pack(side="right", padx=5)

        tk.Button(
            action_frame,
            text="حذف المحددة",
            command=self.remove_selected_image,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('delete'),
            compound="left",
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="right", padx=5)

        # خيارات الترتيب
        layout_frame = tk.LabelFrame(
            self.tab2,
            text="⚙️ خيارات الترتيب",
            font=("Arial", 14, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        layout_frame.pack(pady=10, padx=20, fill="x")

        options_inner = tk.Frame(layout_frame, bg="#1e293b")
        options_inner.pack(pady=10, padx=10, fill="x")

        tk.Radiobutton(
            options_inner,
            text="📄 صورة واحدة بالصفحة (ملء الصفحة)",
            variable=self.image_layout_var,
            value="one_per_page",
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#020617",
            font=("Arial", 12, "bold"),
            command=self.update_custom_input_state,
        ).pack(side="right", padx=15, anchor="w")

        tk.Radiobutton(
            options_inner,
            text="🖼️ أكثر من صورة (2x2 تلقائي)",
            variable=self.image_layout_var,
            value="multiple",
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#020617",
            font=("Arial", 12, "bold"),
            command=self.update_custom_input_state,
        ).pack(side="right", padx=15, anchor="w")

        custom_frame = tk.Frame(options_inner, bg="#1e293b")
        custom_frame.pack(side="right", padx=15, anchor="w")

        tk.Radiobutton(
            custom_frame,
            text="🔢 عدد محدد:",
            variable=self.image_layout_var,
            value="custom",
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#020617",
            font=("Arial", 12, "bold"),
            command=self.update_custom_input_state,
        ).pack(side="right", padx=5)

        self.custom_count_entry = tk.Entry(
            custom_frame,
            textvariable=self.images_per_page_var,
            font=("Arial", 11),
            width=5,
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            state="disabled",
        )
        self.custom_count_entry.pack(side="right", padx=5)

        save_frame = tk.Frame(self.tab2, bg="#1e293b")
        save_frame.pack(pady=10, padx=20, fill="x")

        tk.Button(
            save_frame,
            text="👁️ معاينة",
            command=self.preview_images_pdf,
            bg="#8b5cf6",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=25,
            pady=8,
            activebackground="#7c3aed",
            bd=0,
        ).pack(side="right", padx=10)

        tk.Button(
            save_frame,
            text="حفظ PDF",
            command=self.save_images_as_pdf,
            bg="#22c55e",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=25,
            pady=8,
            image=self.icons.get('save'),
            compound="left",
            activebackground="#16a34a",
            bd=0,
        ).pack(side="right", padx=10)

        self.progress2 = ttk.Progressbar(self.tab2, mode="indeterminate")
        self.progress2.pack(pady=8, padx=20, fill="x")

    # ================= TAB 3: استخراج صور من PDF =================
    def setup_tab3_extract_images(self):
        file_frame = tk.Frame(self.tab3, relief="ridge", bd=2, bg="#334155")
        file_frame.pack(pady=10, padx=20, fill="x")

        tk.Button(
            file_frame,
            text="اختر PDF",
            command=self.select_pdf_for_export,
            bg="#2563eb",
            fg="white",
            font=("Arial", 16, "bold"),
            padx=40,
            pady=15,
            image=self.icons.get('file'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(side="right", pady=20, padx=20)

        self.export_file_label = tk.Label(
            file_frame,
            text="لم يتم اختيار ملف",
            font=("Arial", 13, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.export_file_label.pack(side="right", pady=20, padx=20)

        options_frame = tk.Frame(self.tab3, bg="#1e293b")
        options_frame.pack(pady=10, padx=20, fill="x")

        format_frame = tk.Frame(options_frame, bg="#1e293b")
        format_frame.pack(fill="x", pady=5)

        tk.Label(
            format_frame,
            text="📋 صيغة الحفظ:",
            font=("Arial", 14, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        tk.Radiobutton(
            format_frame,
            text="🖼️ PNG",
            variable=self.export_format,
            value="png",
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#020617",
            font=("Arial", 13, "bold"),
        ).pack(side="right", padx=10)

        tk.Radiobutton(
            format_frame,
            text="🗜️ JPG",
            variable=self.export_format,
            value="jpg",
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#020617",
            font=("Arial", 13, "bold"),
        ).pack(side="right", padx=10)

        dpi_frame = tk.Frame(options_frame, bg="#1e293b")
        dpi_frame.pack(fill="x", pady=5)

        tk.Label(
            dpi_frame,
            text="🔍 DPI (الدقة):",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        tk.Entry(
            dpi_frame,
            textvariable=self.export_dpi_var,
            font=("Arial", 12),
            width=8,
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
        ).pack(side="right", padx=10)

        pages_frame = tk.Frame(options_frame, bg="#1e293b")
        pages_frame.pack(fill="x", pady=5)

        tk.Label(
            pages_frame,
            text="📄 الصفحات (مثال: 1-3,5,7):",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        tk.Entry(
            pages_frame,
            textvariable=self.export_pages_var,
            font=("Arial", 12),
            width=30,
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
        ).pack(side="right", padx=10)

        info_frame = tk.Frame(self.tab3, bg="#1e293b")
        info_frame.pack(pady=10, padx=20, fill="x")

        self.export_pages_label = tk.Label(
            info_frame,
            text="📄 الصفحات: 0",
            font=("Arial", 15, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        )
        self.export_pages_label.pack(side="right", padx=20)

        tk.Button(
            self.tab3,
            text="استخراج الصور",
            command=self.export_pages_as_images,
            bg="#22c55e",
            fg="white",
            font=("Arial", 15, "bold"),
            padx=30,
            pady=15,
            image=self.icons.get('extract'),
            compound="left",
            activebackground="#16a34a",
            bd=0,
        ).pack(pady=20)

        note_frame = tk.Frame(self.tab3, bg="#bfdbfe")
        note_frame.pack(fill="x", padx=0, pady=0)

        note_text = (
            "💡 ملاحظة:\n"
            "• 🖼️ PNG: حفظ بجودة عالية بدون فقدان.\n"
            "• 🗜️ JPG: حفظ مضغوط بحجم أصغر."
        )

        note_label = tk.Label(
            note_frame,
            text=note_text,
            font=("Arial", 13, "bold"),
            fg="#0f172a",
            bg="#bfdbfe",
            anchor="e",
            justify="right",
            wraplength=1300,
        )
        note_label.pack(fill="x", padx=20, pady=6, anchor="e")

        self.progress3 = ttk.Progressbar(self.tab3, mode="indeterminate")
        self.progress3.pack(pady=8, padx=20, fill="x")

    # ================= وظائف TAB 1 =================
    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            threading.Thread(
                target=self.load_pdf_thumbnails, args=(file_path,), daemon=True
            ).start()

    def load_pdf_thumbnails(self, file_path):
        try:
            self.progress.start(10)
            self.selected_file = file_path
            self.root.after(
                0,
                lambda: self.file_label.config(
                    text=os.path.basename(file_path), fg="#22c55e"
                ),
            )

            self.page_thumbnails = pdf_ops.load_page_thumbnails(file_path, scale=0.25)
            self.total_pages = len(self.page_thumbnails)
            self.canvas_images.clear()
            self.selected_pages.clear()
            self.zoom_factor = 1.0
            self.page_order = list(range(self.total_pages))  # تهيئة الترتيب
            self.page_rotations = {}  # إعادة تعيين التدويرات
            
            # حفظ التدوير الأصلي لكل صفحة
            import fitz
            doc = fitz.open(file_path)
            self.original_rotations = {}
            try:
                for i in range(doc.page_count):
                    page = doc.load_page(i)
                    self.original_rotations[i] = page.rotation
            finally:
                doc.close()

            self.root.after(0, self.display_thumbnails)
        except Exception as e:
            self.root.after(
                0, lambda: show_custom_message(self.root, "خطأ", f"خطأ في تحميل:\n{str(e)}", "error")
            )
            self.root.after(0, self.progress.stop)

    def display_thumbnails(self):
        self.canvas.delete("all")
        self.canvas_images.clear()

        cols = 4
        base_w = 180
        base_h = 250
        margin = 15

        thumb_width = int(base_w * self.zoom_factor)
        thumb_height = int(base_h * self.zoom_factor)

        visible_index = 0
        for display_idx, original_idx in enumerate(self.page_order):
            if self.hide_deleted_var.get() and original_idx in self.selected_pages:
                continue

            img = self.page_thumbnails[original_idx].copy()
            
            # لا نحتاج لتطبيق التدوير هنا لأن thumbnail أصبح مدوراً بالفعل من update_thumbnails_with_rotation

            col = visible_index % cols
            row = visible_index // cols
            visible_index += 1

            x = col * (thumb_width + margin) + margin
            y = row * (thumb_height + margin) + margin

            img_resized = img.resize(
                (thumb_width - 20, thumb_height - 60), Image.Resampling.LANCZOS
            )
            photo = ImageTk.PhotoImage(img_resized)
            self.canvas_images.append(photo)

            frame_tag = f"frame_{display_idx}"
            num_tag = f"num_{display_idx}"
            img_tag = f"img_{display_idx}"

            outline_color = "#ef4444" if original_idx in self.selected_pages else "#d1d5db"
            outline_width = 4 if original_idx in self.selected_pages else 2

            self.canvas.create_rectangle(
                x,
                y,
                x + thumb_width,
                y + thumb_height,
                fill="#ffffff",
                outline=outline_color,
                width=outline_width,
                tags=frame_tag,
            )

            self.canvas.create_text(
                x + thumb_width // 2,
                y + 15,
                text=f"صفحة {original_idx + 1}",
                font=("Arial", max(9, int(12 * self.zoom_factor)), "bold"),
                fill="#111827",
                tags=num_tag,
            )

            self.canvas.create_image(
                x + thumb_width // 2,
                y + thumb_height // 2,
                image=photo,
                anchor="center",
                tags=img_tag,
            )

            # ربط أحداث السحب والإفلات
            for tag in (frame_tag, num_tag, img_tag):
                self.canvas.tag_bind(
                    tag,
                    "<Button-1>",
                    lambda e, idx=display_idx, orig=original_idx: self.start_drag_reorder(
                        e, idx, orig
                    ),
                )
                self.canvas.tag_bind(tag, "<B1-Motion>", self.on_drag_reorder)
                self.canvas.tag_bind(tag, "<ButtonRelease-1>", self.end_drag_reorder)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.pages_label.config(text=f"📄 الصفحات: {self.total_pages}")
        self.save_btn.config(state="normal")
        self.progress.stop()

    def start_drag_reorder(self, event, display_idx: int, original_idx: int):
        """بدء السحب لإعادة الترتيب"""
        self.drag_data["item"] = display_idx
        self.drag_data["start_pos"] = (event.x, event.y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        # تمييز الصفحة المسحوبة
        self.canvas.delete("drag_highlight")
        self.highlight_dragged_page(display_idx)

    def on_drag_reorder(self, event):
        """أثناء السحب"""
        if self.drag_data["item"] is not None:
            # حساب المسافة المقطوعة
            dx = abs(event.x - self.drag_data["x"])
            dy = abs(event.y - self.drag_data["y"])

            # إذا تحرك الماوس مسافة كافية، نعتبره سحب
            if dx > 5 or dy > 5:
                # الحصول على موضع الصفحة الجديد
                new_display_idx = self.get_page_at_position(event.x, event.y)
                if new_display_idx is not None and new_display_idx != self.drag_data["item"]:
                    # إعادة ترتيب الصفحات
                    old_idx = self.drag_data["item"]
                    self.page_order.insert(new_display_idx, self.page_order.pop(old_idx))
                    self.drag_data["item"] = new_display_idx
                    self.display_thumbnails()

    def end_drag_reorder(self, event):
        """إنهاء السحب"""
        if self.drag_data["item"] is not None:
            # إذا كانت المسافة صغيرة، نعتبره نقر عادي
            if self.drag_data["start_pos"]:
                dx = abs(event.x - self.drag_data["start_pos"][0])
                dy = abs(event.y - self.drag_data["start_pos"][1])
                if dx < 5 and dy < 5:
                    # نقر عادي - تبديل التحديد
                    display_idx = self.drag_data["item"]
                    if display_idx < len(self.page_order):
                        original_idx = self.page_order[display_idx]
                        self.toggle_selection(original_idx)
                        return

            self.drag_data["item"] = None
            self.drag_data["start_pos"] = None
            self.canvas.delete("drag_highlight")
            self.display_thumbnails()

    def get_page_at_position(self, x, y):
        """الحصول على رقم الصفحة في الموضع المحدد (display index)"""
        canvas_y = self.canvas.canvasy(y)
        cols = 4
        base_w = 180
        base_h = 250
        margin = 15

        thumb_width = int(base_w * self.zoom_factor)
        thumb_height = int(base_h * self.zoom_factor)

        col = int((x - margin) / (thumb_width + margin))
        row = int((canvas_y - margin) / (thumb_height + margin))

        if col < 0 or col >= cols:
            return None

        # حساب display index مع مراعاة الصفحات المخفية
        visible_index = row * cols + col
        visible_count = 0
        for display_idx, original_idx in enumerate(self.page_order):
            if self.hide_deleted_var.get() and original_idx in self.selected_pages:
                continue
            if visible_count == visible_index:
                return display_idx
            visible_count += 1

        return None

    def highlight_dragged_page(self, display_idx: int):
        """تمييز صفحة مسحوبة"""
        cols = 4
        base_w = 180
        base_h = 250
        margin = 15

        thumb_width = int(base_w * self.zoom_factor)
        thumb_height = int(base_h * self.zoom_factor)

        # حساب موضع الصفحة
        visible_count = 0
        for idx, original_idx in enumerate(self.page_order):
            if self.hide_deleted_var.get() and original_idx in self.selected_pages:
                continue
            if idx == display_idx:
                col = visible_count % cols
                row = visible_count // cols
                x = col * (thumb_width + margin) + margin
                y = row * (thumb_height + margin) + margin

                self.canvas.create_rectangle(
                    x - 5,
                    y - 5,
                    x + thumb_width + 5,
                    y + thumb_height + 5,
                    outline="#2563eb",
                    width=4,
                    tags="drag_highlight",
                )
                break
            visible_count += 1

    def toggle_selection(self, page_idx: int):
        """تبديل تحديد صفحة (نقر عادي)"""
        if page_idx in self.selected_pages:
            self.selected_pages.remove(page_idx)
        else:
            self.selected_pages.add(page_idx)

        self.update_selection_count()
        self.display_thumbnails()

    def update_selection_count(self):
        self.selected_label.config(
            text=f"🗑️ محدد للحذف: {len(self.selected_pages)} صفحة"
        )

    def select_all_delete(self):
        self.selected_pages = set(range(self.total_pages))
        self.update_selection_count()
        self.display_thumbnails()

    def clear_all_selection(self):
        self.selected_pages.clear()
        self.update_selection_count()
        self.display_thumbnails()

    def invert_selection(self):
        self.selected_pages = {
            i for i in range(self.total_pages) if i not in self.selected_pages
        }
        self.update_selection_count()
        self.display_thumbnails()

    def select_even_pages(self):
        self.selected_pages = {i for i in range(self.total_pages) if (i + 1) % 2 == 0}
        self.update_selection_count()
        self.display_thumbnails()

    def select_odd_pages(self):
        self.selected_pages = {i for i in range(self.total_pages) if (i + 1) % 2 == 1}
        self.update_selection_count()
        self.display_thumbnails()

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor += 0.25
            self.display_thumbnails()

    def zoom_out(self):
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor -= 0.25
            self.display_thumbnails()

    def rotate_selected_pages(self, angle: int):
        if not self.selected_file:
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return
        
        if not self.selected_pages:
            show_custom_message(self.root, "تحذير", "اختر صفحات أولاً!", "warning")
            return

        # تطبيق التدوير مباشرة على الصفحات المحددة
        pages_to_rotate = sorted(self.selected_pages)
        
        # تحديث زوايا التدوير (90 درجة فقط في كل مرة)
        for page_idx in pages_to_rotate:
            current_angle = self.page_rotations.get(page_idx, 0)
            # إضافة 90 درجة فقط (اتجاه عقارب الساعة) أو -90 (عكس عقارب الساعة)
            new_angle = (current_angle + angle) % 360
            self.page_rotations[page_idx] = new_angle
        
        # تحديث thumbnails مع التدوير
        threading.Thread(
            target=self.update_thumbnails_with_rotation,
            args=(pages_to_rotate,),
            daemon=True,
        ).start()

    def update_thumbnails_with_rotation(self, pages_to_rotate):
        """تحديث thumbnails مع التدوير"""
        try:
            import fitz
            doc = fitz.open(self.selected_file)
            try:
                for page_idx in pages_to_rotate:
                    if 0 <= page_idx < doc.page_count:
                        page = doc.load_page(page_idx)
                        rotation_angle = self.page_rotations.get(page_idx, 0)
                        # نطبق التدوير المطلق (التدوير الأصلي + التدوير الإضافي)
                        original_rotation = self.original_rotations.get(page_idx, 0)
                        total_rotation = (original_rotation + rotation_angle) % 360
                        page.set_rotation(total_rotation)
                        # إعادة تحميل thumbnail
                        mat = fitz.Matrix(0.25, 0.25)
                        pix = page.get_pixmap(matrix=mat)
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        self.page_thumbnails[page_idx] = img
            finally:
                doc.close()
            
            # تحديث العرض
            self.root.after(0, self.display_thumbnails)
        except Exception as e:
            self.root.after(0, lambda: show_custom_message(self.root, "❌ خطأ", f"خطأ في التدوير:\n{str(e)}", "error"))

    def apply_rotations_to_pdf(self, pdf_path: str, output_path: str, page_rotations: dict):
        """تطبيق التدويرات على PDF عند الحفظ"""
        import fitz
        doc = fitz.open(pdf_path)
        try:
            for page_idx, angle in page_rotations.items():
                if 0 <= page_idx < doc.page_count:
                    page = doc.load_page(page_idx)
                    # نطبق التدوير المطلق (التدوير الأصلي + التدوير الإضافي)
                    original_rotation = self.original_rotations.get(page_idx, 0) if hasattr(self, 'original_rotations') else 0
                    total_rotation = (original_rotation + angle) % 360
                    page.set_rotation(total_rotation)
            doc.save(output_path)
        finally:
            doc.close()

    def save_selected_pages(self):
        if not self.selected_pages:
            show_custom_message(self.root, "تحذير", "اختر صفحات أولاً!", "warning")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        pages_to_keep = sorted(self.selected_pages)

        threading.Thread(
            target=self.process_and_save_selected,
            args=(output_path, pages_to_keep),
            daemon=True,
        ).start()

    def move_selected_up(self):
        if not self.selected_pages:
            show_custom_message(self.root, "تحذير", "اختر صفحات أولاً!", "warning")
            return

        selected_list = sorted([self.page_order.index(p) for p in self.selected_pages])
        if selected_list[0] == 0:
            show_custom_message(self.root, "معلومة", "الصفحات المحددة في البداية بالفعل!", "info")
            return

        # نقل الصفحات المحددة لأعلى في الترتيب
        for pos in selected_list:
            if pos > 0:
                self.page_order[pos], self.page_order[pos - 1] = (
                    self.page_order[pos - 1],
                    self.page_order[pos],
                )

        self.display_thumbnails()

    def move_selected_down(self):
        if not self.selected_pages:
            show_custom_message(self.root, "تحذير", "اختر صفحات أولاً!", "warning")
            return

        selected_list = sorted(
            [self.page_order.index(p) for p in self.selected_pages], reverse=True
        )
        if selected_list[0] == len(self.page_order) - 1:
            show_custom_message(self.root, "معلومة", "الصفحات المحددة في النهاية بالفعل!", "info")
            return

        # نقل الصفحات المحددة لأسفل في الترتيب
        for pos in selected_list:
            if pos < len(self.page_order) - 1:
                self.page_order[pos], self.page_order[pos + 1] = (
                    self.page_order[pos + 1],
                    self.page_order[pos],
                )

        self.display_thumbnails()

    def save_reordered_pdf(self):
        if not self.selected_file:
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        threading.Thread(
            target=self.process_reorder_pdf, args=(output_path,), daemon=True
        ).start()

    def process_reorder_pdf(self, output_path: str):
        try:
            self.progress.start()
            
            # حفظ في ملف مؤقت أولاً
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path = temp_file.name
            temp_file.close()
            
            pdf_ops.reorder_pages(self.selected_file, self.page_order, temp_path)
            
            # تطبيق التدويرات إذا كانت موجودة
            if self.page_rotations:
                # إعادة ترتيب التدويرات حسب الترتيب الجديد
                reordered_rotations = {}
                for new_idx, old_idx in enumerate(self.page_order):
                    if old_idx in self.page_rotations:
                        reordered_rotations[new_idx] = self.page_rotations[old_idx]
                self.apply_rotations_to_pdf(temp_path, output_path, reordered_rotations)
            else:
                import shutil
                shutil.move(temp_path, output_path)
            
            self.root.after(0, self.progress.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم حفظ الملف بالترتيب الجديد!\n📁 {os.path.basename(output_path)}",
                    "success",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab1_fields)
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def add_pages_dialog(self):
        if not self.selected_file:
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("➕ إضافة صفحات")
        dialog.geometry("500x300")
        dialog.configure(bg="#1e293b")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="اختر طريقة الإضافة:",
            font=("Arial", 14, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(pady=20)

        btn_frame = tk.Frame(dialog, bg="#1e293b")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="📄 من ملف PDF آخر",
            command=lambda: self.add_pages_from_pdf(dialog),
            bg="#2563eb",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=15,
            activebackground="#1d4ed8",
            bd=0,
        ).pack(pady=10, fill="x", padx=30)

        tk.Button(
            btn_frame,
            text="📄 صفحة فارغة",
            command=lambda: self.add_blank_page(dialog),
            bg="#10b981",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=15,
            activebackground="#059669",
            bd=0,
        ).pack(pady=10, fill="x", padx=30)

        tk.Button(
            btn_frame,
            text="إلغاء",
            command=dialog.destroy,
            bg="#6b7280",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            activebackground="#4b5563",
            bd=0,
        ).pack(pady=10, fill="x", padx=30)

    def add_pages_from_pdf(self, dialog):
        dialog.destroy()
        file_path = filedialog.askopenfilename(
            title="اختر ملف PDF لإضافة صفحات منه", filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        # فتح الملف لمعرفة عدد الصفحات
        try:
            import fitz
            temp_doc = fitz.open(file_path)
            total_pages_in_file = temp_doc.page_count
            temp_doc.close()
        except Exception as e:
            show_custom_message(self.root, "خطأ", f"خطأ في قراءة الملف:\n{str(e)}", "error")
            return

        # نافذة اختيار الصفحات
        pages_selection = self.show_pages_selection_dialog(file_path, total_pages_in_file)
        if pages_selection is None:
            return

        insert_pos_str = show_custom_input(
            self.root,
            "موضع الإضافة",
            f"أدخل موضع الإضافة (1-{self.total_pages + 1}):",
            str(self.total_pages + 1),
        )
        if not insert_pos_str:
            return

        try:
            insert_pos = int(insert_pos_str) - 1
            if insert_pos < 0 or insert_pos > self.total_pages:
                raise ValueError("موضع غير صحيح")
        except ValueError:
            show_custom_message(self.root, "خطأ", "موضع غير صحيح!", "error")
            return

        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()

        threading.Thread(
            target=self.process_add_pages_from_pdf,
            args=(file_path, insert_pos, temp_path, pages_selection),
            daemon=True,
        ).start()

    def show_pages_selection_dialog(self, file_path: str, total_pages: int):
        """نافذة اختيار صفحات محددة من الملف"""
        selection_window = tk.Toplevel(self.root)
        selection_window.title("اختر الصفحات المطلوبة")
        selection_window.geometry("800x600")
        selection_window.configure(bg="#1e293b")
        selection_window.transient(self.root)
        selection_window.grab_set()

        selected_pages = set()

        # رأس النافذة
        header_frame = tk.Frame(selection_window, bg="#3b82f6", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"اختر الصفحات من الملف ({total_pages} صفحة)",
            font=("Arial", 14, "bold"),
            fg="#ffffff",
            bg="#3b82f6",
        ).pack(expand=True, pady=10)

        # Canvas لعرض الصفحات
        canvas_frame = tk.Frame(selection_window, bg="#1e293b")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scroll_frame = tk.Frame(canvas_frame, bg="#1e293b")
        scroll_frame.pack(fill="both", expand=True)

        selection_canvas = tk.Canvas(scroll_frame, bg="#1e293b", highlightthickness=0)
        selection_scrollbar = ttk.Scrollbar(
            scroll_frame, orient="vertical", command=selection_canvas.yview
        )
        selection_canvas.configure(yscrollcommand=selection_scrollbar.set)

        selection_scrollbar.pack(side="right", fill="y")
        selection_canvas.pack(side="left", fill="both", expand=True)

        # تحميل المصغرات
        def load_thumbnails():
            try:
                thumbnails = pdf_ops.load_page_thumbnails(file_path, scale=0.15)
                canvas_images = []

                cols = 4
                thumb_width = 150
                thumb_height = 200
                margin = 10

                for i, thumbnail in enumerate(thumbnails):
                    col = i % cols
                    row = i // cols

                    x = col * (thumb_width + margin) + margin
                    y = row * (thumb_height + margin) + margin

                    img_resized = thumbnail.resize(
                        (thumb_width - 20, thumb_height - 40), Image.Resampling.LANCZOS
                    )
                    photo = ImageTk.PhotoImage(img_resized)
                    canvas_images.append(photo)

                    # إطار الصفحة
                    rect_tag = f"rect_{i}"
                    selection_canvas.create_rectangle(
                        x, y, x + thumb_width, y + thumb_height,
                        fill="#ffffff", outline="#d1d5db", width=2,
                        tags=(rect_tag, "page_item")
                    )

                    # الصورة
                    img_tag = f"img_{i}"
                    selection_canvas.create_image(
                        x + thumb_width // 2, y + 30,
                        image=photo, anchor="center",
                        tags=(img_tag, "page_item")
                    )

                    # رقم الصفحة
                    text_tag = f"text_{i}"
                    selection_canvas.create_text(
                        x + thumb_width // 2, y + thumb_height - 20,
                        text=f"صفحة {i + 1}",
                        font=("Arial", 10, "bold"),
                        fill="#1e293b",
                        tags=(text_tag, "page_item")
                    )

                    # ربط النقر
                    def toggle_selection(idx):
                        if idx in selected_pages:
                            selected_pages.remove(idx)
                            selection_canvas.itemconfig(f"rect_{idx}", outline="#d1d5db", width=2)
                        else:
                            selected_pages.add(idx)
                            selection_canvas.itemconfig(f"rect_{idx}", outline="#3b82f6", width=4)

                    for tag in [rect_tag, img_tag, text_tag]:
                        selection_canvas.tag_bind(
                            tag, "<Button-1>", lambda e, idx=i: toggle_selection(idx)
                        )

                selection_canvas.configure(scrollregion=selection_canvas.bbox("all"))
                selection_canvas.canvas_images = canvas_images
            except Exception as e:
                show_custom_message(self.root, "خطأ", f"خطأ في تحميل الصفحات:\n{str(e)}", "error")

        threading.Thread(target=load_thumbnails, daemon=True).start()

        # أزرار التحكم
        control_frame = tk.Frame(selection_window, bg="#1e293b")
        control_frame.pack(fill="x", padx=10, pady=10)

        def select_all():
            for i in range(total_pages):
                selected_pages.add(i)
                selection_canvas.itemconfig(f"rect_{i}", outline="#3b82f6", width=4)

        def clear_selection():
            selected_pages.clear()
            for i in range(total_pages):
                selection_canvas.itemconfig(f"rect_{i}", outline="#d1d5db", width=2)

        tk.Button(
            control_frame,
            text="تحديد الكل",
            command=select_all,
            bg="#3b82f6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
        ).pack(side="right", padx=5)

        tk.Button(
            control_frame,
            text="إلغاء التحديد",
            command=clear_selection,
            bg="#64748b",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
        ).pack(side="right", padx=5)

        result = [None]

        def confirm():
            if selected_pages:
                result[0] = sorted(selected_pages)
            else:
                result[0] = list(range(total_pages))  # إذا لم يتم التحديد، نأخذ الكل
            selection_window.destroy()

        def cancel():
            result[0] = None
            selection_window.destroy()

        tk.Button(
            control_frame,
            text="✅ تأكيد",
            command=confirm,
            bg="#22c55e",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=8,
        ).pack(side="left", padx=5)

        tk.Button(
            control_frame,
            text="❌ إلغاء",
            command=cancel,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=8,
        ).pack(side="left", padx=5)

        selection_window.wait_window()
        return result[0]

    def process_add_pages_from_pdf(self, insert_pdf_path: str, insert_at: int, temp_path: str, pages_to_insert: list = None):
        try:
            self.progress.start()
            total_pages = pdf_ops.insert_pages_from_pdf(
                self.selected_file, insert_pdf_path, insert_at, pages_to_insert, temp_path
            )
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.show_preview_dialog(temp_path, total_pages))
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def add_blank_page(self, dialog):
        dialog.destroy()
        insert_pos_str = show_custom_input(
            self.root,
            "موضع الإضافة",
            f"أدخل موضع الإضافة (1-{self.total_pages + 1}):",
            str(self.total_pages + 1),
        )
        if not insert_pos_str:
            return

        try:
            insert_pos = int(insert_pos_str) - 1
            if insert_pos < 0 or insert_pos > self.total_pages:
                raise ValueError("موضع غير صحيح")
        except ValueError:
            show_custom_message(self.root, "خطأ", "موضع غير صحيح!", "error")
            return

        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()

        threading.Thread(
            target=self.process_add_blank_page,
            args=(insert_pos, temp_path),
            daemon=True,
        ).start()

    def process_add_blank_page(self, insert_at: int, temp_path: str):
        try:
            self.progress.start()
            total_pages = pdf_ops.insert_blank_page(
                self.selected_file, insert_at, output_path=temp_path
            )
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.show_preview_dialog(temp_path, total_pages))
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def show_preview_dialog(self, preview_pdf_path: str, total_pages: int):
        """نافذة معاينة للملف بعد إضافة الصفحات"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("🔍 معاينة الملف بعد الإضافة")
        preview_window.geometry("1200x800")
        preview_window.configure(bg="#1e293b")
        preview_window.transient(self.root)

        # متغيرات السحب والإفلات
        drag_data = {"item": None, "x": 0, "y": 0}
        page_order = list(range(total_pages))  # ترتيب الصفحات الحالي
        selected_pages_in_preview = set()  # الصفحات المحددة في المعاينة
        deleted_pages = set()  # الصفحات المحذوفة
        selected_pages_in_preview = set()  # الصفحات المحددة في المعاينة
        deleted_pages = set()  # الصفحات المحذوفة

        # رأس النافذة
        header_frame = tk.Frame(preview_window, bg="#3b82f6", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"🔍 معاينة الملف - {total_pages} صفحة (اسحب الصفحات لإعادة الترتيب)",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg="#3b82f6",
        ).pack(expand=True)

        # Canvas للمعاينة
        canvas_frame = tk.LabelFrame(
            preview_window,
            text="📄 جميع الصفحات",
            font=("Arial", 14, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scroll_frame = tk.Frame(canvas_frame, bg="#1e293b")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        preview_canvas = tk.Canvas(scroll_frame, bg="#f9fafb", highlightthickness=0)
        preview_scrollbar = ttk.Scrollbar(
            scroll_frame, orient="vertical", command=preview_canvas.yview
        )
        preview_canvas.configure(yscrollcommand=preview_scrollbar.set)

        preview_scrollbar.pack(side="right", fill="y")
        preview_canvas.pack(side="left", fill="both", expand=True)

        # ربط التمرير بالماوس
        def on_mousewheel(event):
            preview_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        preview_canvas.bind("<MouseWheel>", on_mousewheel)
        preview_canvas.bind("<Enter>", lambda e: preview_canvas.focus_set())

        # وظائف السحب والإفلات
        def get_page_at_position(x, y):
            """الحصول على رقم الصفحة في الموضع المحدد"""
            canvas_y = preview_canvas.canvasy(y)
            cols = 3
            base_w = 200
            base_h = 280
            margin = 15

            col = int((x - margin) / (base_w + margin))
            row = int((canvas_y - margin) / (base_h + margin))

            if col < 0 or col >= cols:
                return None

            page_idx = row * cols + col
            if 0 <= page_idx < len(page_order):
                return page_idx
            return None

        def start_drag(event):
            """بدء السحب"""
            x, y = event.x, event.y
            page_idx = get_page_at_position(x, y)
            if page_idx is not None:
                drag_data["item"] = page_idx
                drag_data["x"] = x
                drag_data["y"] = y
                # تمييز الصفحة المسحوبة
                highlight_page(page_idx)

        def on_drag(event):
            """أثناء السحب"""
            if drag_data["item"] is not None:
                x, y = event.x, event.y
                new_page_idx = get_page_at_position(x, y)
                if new_page_idx is not None and new_page_idx != drag_data["item"]:
                    # إعادة ترتيب الصفحات
                    old_idx = drag_data["item"]
                    page_order.insert(new_page_idx, page_order.pop(old_idx))
                    drag_data["item"] = new_page_idx
                    refresh_preview()

        def end_drag(event):
            """إنهاء السحب"""
            if drag_data["item"] is not None:
                drag_data["item"] = None
                refresh_preview()

        def highlight_page(page_idx):
            """تمييز صفحة معينة"""
            cols = 3
            base_w = 200
            base_h = 280
            margin = 15

            actual_idx = page_order[page_idx]
            col = page_idx % cols
            row = page_idx // cols

            x = col * (base_w + margin) + margin
            y = row * (base_h + margin) + margin

            # إزالة التمييز السابق
            preview_canvas.delete("highlight")
            # إضافة تمييز جديد
            preview_canvas.create_rectangle(
                x - 5,
                y - 5,
                x + base_w + 5,
                y + base_h + 5,
                outline="#2563eb",
                width=4,
                tags="highlight",
            )

        def toggle_page_selection(display_idx):
            """تبديل تحديد صفحة في المعاينة"""
            if display_idx in selected_pages_in_preview:
                selected_pages_in_preview.remove(display_idx)
                preview_canvas.itemconfig(f"rect_{display_idx}", outline="#d1d5db", width=2)
            else:
                selected_pages_in_preview.add(display_idx)
                preview_canvas.itemconfig(f"rect_{display_idx}", outline="#3b82f6", width=4)

        def delete_selected_pages():
            """حذف الصفحات المحددة من المعاينة"""
            if not selected_pages_in_preview:
                show_custom_message(self.root, "تحذير", "اختر صفحات للحذف أولاً!", "warning")
                return
            
            # إضافة الصفحات المحددة إلى المحذوفة
            for display_idx in list(selected_pages_in_preview):
                if display_idx < len(page_order):
                    original_idx = page_order[display_idx]
                    deleted_pages.add(original_idx)
            
            # إزالة الصفحات المحذوفة من page_order
            page_order[:] = [idx for idx in page_order if idx not in deleted_pages]
            selected_pages_in_preview.clear()
            refresh_preview()

        def refresh_preview():
            """تحديث عرض الصفحات حسب الترتيب الجديد"""
            preview_canvas.delete("all")
            try:
                thumbnails = pdf_ops.load_page_thumbnails(preview_pdf_path, scale=0.2)
                canvas_images = []

                cols = 3
                base_w = 200
                base_h = 280
                margin = 15

                # عرض الصفحات غير المحذوفة فقط
                visible_pages = [idx for idx in page_order if idx not in deleted_pages]

                for display_idx, original_idx in enumerate(visible_pages):
                    col = display_idx % cols
                    row = display_idx // cols

                    x = col * (base_w + margin) + margin
                    y = row * (base_h + margin) + margin

                    img = thumbnails[original_idx]
                    img_resized = img.resize(
                        (base_w - 20, base_h - 60), Image.Resampling.LANCZOS
                    )
                    photo = ImageTk.PhotoImage(img_resized)
                    canvas_images.append(photo)

                    # حفظ tags لكل عنصر
                    rect_tag = f"rect_{display_idx}"
                    text_tag = f"text_{display_idx}"
                    img_tag = f"img_{display_idx}"

                    # تحديد لون الإطار حسب التحديد
                    outline_color = "#3b82f6" if display_idx in selected_pages_in_preview else "#d1d5db"
                    outline_width = 4 if display_idx in selected_pages_in_preview else 2

                    preview_canvas.create_rectangle(
                        x,
                        y,
                        x + base_w,
                        y + base_h,
                        fill="#ffffff",
                        outline=outline_color,
                        width=outline_width,
                        tags=(rect_tag, "page"),
                    )

                    preview_canvas.create_text(
                        x + base_w // 2,
                        y + 15,
                        text=f"صفحة {original_idx + 1}",
                        font=("Arial", 11, "bold"),
                        fill="#111827",
                        tags=(text_tag, "page"),
                    )

                    preview_canvas.create_image(
                        x + base_w // 2,
                        y + base_h // 2,
                        image=photo,
                        anchor="center",
                        tags=(img_tag, "page"),
                    )

                    # ربط أحداث النقر للتحديد (Ctrl+Click) والسحب
                    def on_page_click(event, idx=display_idx):
                        if event.state & 0x4:  # Ctrl key
                            toggle_page_selection(idx)
                        else:
                            start_drag(event)

                    for tag in (rect_tag, text_tag, img_tag):
                        preview_canvas.tag_bind(tag, "<Button-1>", on_page_click)
                        preview_canvas.tag_bind(tag, "<B1-Motion>", on_drag)
                        preview_canvas.tag_bind(tag, "<ButtonRelease-1>", end_drag)

                preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))
                preview_canvas.canvas_images = canvas_images
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في تحديث المعاينة:\n{str(e)}")

        # تحميل الصور المصغرة في Thread
        def load_preview_thumbnails():
            try:
                refresh_preview()
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في تحميل المعاينة:\n{str(e)}")

        threading.Thread(target=load_preview_thumbnails, daemon=True).start()

        # حفظ الترتيب الجديد في متغير النافذة
        preview_window.page_order = page_order
        preview_window.preview_pdf_path = preview_pdf_path
        preview_window.deleted_pages = deleted_pages

        # أزرار التحكم
        control_frame = tk.Frame(preview_window, bg="#1e293b")
        control_frame.pack(fill="x", padx=10, pady=10)

        # زر حذف المحدد
        tk.Button(
            control_frame,
            text="🗑️ حذف المحدد",
            command=delete_selected_pages,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="right", padx=5)

        tk.Label(
            control_frame,
            text="💡 اضغط Ctrl+Click لتحديد صفحات للحذف",
            font=("Arial", 10),
            fg="#9ca3af",
            bg="#1e293b",
        ).pack(side="right", padx=10)

        tk.Button(
            control_frame,
            text="💾 حفظ",
            command=lambda: self.save_preview_file(
                preview_window, preview_pdf_path, page_order, deleted_pages
            ),
            bg="#22c55e",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#16a34a",
            bd=0,
        ).pack(side="left", padx=10)

        tk.Button(
            control_frame,
            text="❌ إلغاء",
            command=lambda: self.cancel_preview(preview_window, preview_pdf_path),
            bg="#ef4444",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="left", padx=10)

    def save_preview_file(self, preview_window, temp_path: str, page_order: list = None, deleted_pages: set = None):
        """حفظ الملف من المعاينة مع إمكانية إعادة الترتيب وحذف الصفحات"""
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if output_path:
            try:
                # الحصول على الصفحات المتبقية (غير المحذوفة)
                if deleted_pages:
                    pages_to_keep = [idx for idx in page_order if idx not in deleted_pages]
                else:
                    pages_to_keep = page_order if page_order else list(range(len(page_order)))

                if not pages_to_keep:
                    messagebox.showwarning("تحذير", "لا توجد صفحات للحفظ!")
                    return

                # إذا كان هناك حذف أو إعادة ترتيب، نحفظ الصفحات المتبقية فقط
                if deleted_pages or (page_order and page_order != list(range(len(page_order)))):
                    # إعادة ترتيب الصفحات المتبقية
                    pdf_ops.reorder_pages(temp_path, pages_to_keep, output_path)
                else:
                    import shutil
                    shutil.copy2(temp_path, output_path)
                
                show_custom_message(
                    self.root,
                    "✅ نجح",
                    f"تم حفظ الملف!\n📁 {os.path.basename(output_path)}\n📄 عدد الصفحات: {len(pages_to_keep)}",
                    "success",
                )
                preview_window.destroy()
                os.unlink(temp_path)  # حذف الملف المؤقت
            except Exception as e:
                messagebox.showerror("❌ خطأ", f"خطأ في الحفظ:\n{str(e)}")
        else:
            preview_window.destroy()
            os.unlink(temp_path)

    def cancel_preview(self, preview_window, temp_path: str):
        """إلغاء المعاينة وحذف الملف المؤقت"""
        preview_window.destroy()
        try:
            os.unlink(temp_path)
        except:
            pass

    # ================= TAB 5: حماية وبيانات =================
    def setup_tab5_security_metadata(self):
        # Canvas مع Scrollbar للتمرير
        canvas = tk.Canvas(self.tab5, bg="#1e293b", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab5, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e293b")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # قسم حماية PDF
        protect_frame = tk.LabelFrame(
            scrollable_frame,
            text="🔒 حماية PDF بكلمة مرور",
            font=("Arial", 15, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        protect_frame.pack(pady=15, padx=20, fill="x")

        file_protect_frame = tk.Frame(protect_frame, bg="#334155")
        file_protect_frame.pack(pady=10, padx=10, fill="x")

        tk.Button(
            file_protect_frame,
            text="اختر ملف PDF",
            command=self.select_pdf_for_protection,
            bg="#2563eb",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=25,
            pady=10,
            image=self.icons.get('file'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(side="right", padx=10)

        self.protect_file_label = tk.Label(
            file_protect_frame,
            text="لم يتم اختيار ملف",
            font=("Arial", 12, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.protect_file_label.pack(side="right", padx=10, fill="x", expand=True)

        password_frame = tk.Frame(protect_frame, bg="#1e293b")
        password_frame.pack(pady=15, padx=10, fill="x")

        tk.Label(
            password_frame,
            text="🔑 كلمة المرور:",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Arial", 12),
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            show="*",
        )
        password_entry.pack(side="right", padx=10, fill="x", expand=True)

        # خيارات الحفظ
        save_options_frame = tk.Frame(protect_frame, bg="#1e293b")
        save_options_frame.pack(pady=15, padx=10, fill="x")

        self.protect_save_option = tk.StringVar(value="same")
        tk.Radiobutton(
            save_options_frame,
            text="💾 حفظ على نفس الملف",
            variable=self.protect_save_option,
            value="same",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#334155",
            activebackground="#1e293b",
            activeforeground="#e5e7eb",
        ).pack(side="right", padx=15)

        tk.Radiobutton(
            save_options_frame,
            text="💾 حفظ باسم جديد",
            variable=self.protect_save_option,
            value="new",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#334155",
            activebackground="#1e293b",
            activeforeground="#e5e7eb",
        ).pack(side="right", padx=15)

        buttons_frame = tk.Frame(protect_frame, bg="#1e293b")
        buttons_frame.pack(pady=15, padx=10, fill="x")

        tk.Button(
            buttons_frame,
            text="🔒 حماية الملف",
            command=self.protect_pdf_action,
            bg="#ef4444",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="right", padx=10)

        # قسم إزالة الحماية
        remove_protect_frame = tk.LabelFrame(
            scrollable_frame,
            text="🔓 إزالة حماية PDF",
            font=("Arial", 15, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        remove_protect_frame.pack(pady=15, padx=20, fill="x")

        file_remove_frame = tk.Frame(remove_protect_frame, bg="#334155")
        file_remove_frame.pack(pady=10, padx=10, fill="x")

        tk.Button(
            file_remove_frame,
            text="اختر ملف PDF محمي",
            command=self.select_protected_pdf,
            bg="#2563eb",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=25,
            pady=10,
            image=self.icons.get('file'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(side="right", padx=10)

        self.remove_protect_file_label = tk.Label(
            file_remove_frame,
            text="لم يتم اختيار ملف",
            font=("Arial", 12, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.remove_protect_file_label.pack(side="right", padx=10, fill="x", expand=True)

        remove_password_frame = tk.Frame(remove_protect_frame, bg="#1e293b")
        remove_password_frame.pack(pady=15, padx=10, fill="x")

        tk.Label(
            remove_password_frame,
            text="🔑 كلمة المرور:",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        self.remove_password_var = tk.StringVar()
        remove_password_entry = tk.Entry(
            remove_password_frame,
            textvariable=self.remove_password_var,
            font=("Arial", 12),
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
            show="*",
        )
        remove_password_entry.pack(side="right", padx=10, fill="x", expand=True)

        # خيارات الحفظ
        remove_save_options_frame = tk.Frame(remove_protect_frame, bg="#1e293b")
        remove_save_options_frame.pack(pady=15, padx=10, fill="x")

        self.remove_protect_save_option = tk.StringVar(value="same")
        tk.Radiobutton(
            remove_save_options_frame,
            text="💾 حفظ على نفس الملف",
            variable=self.remove_protect_save_option,
            value="same",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#334155",
            activebackground="#1e293b",
            activeforeground="#e5e7eb",
        ).pack(side="right", padx=15)

        tk.Radiobutton(
            remove_save_options_frame,
            text="💾 حفظ باسم جديد",
            variable=self.remove_protect_save_option,
            value="new",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
            selectcolor="#334155",
            activebackground="#1e293b",
            activeforeground="#e5e7eb",
        ).pack(side="right", padx=15)

        remove_buttons_frame = tk.Frame(remove_protect_frame, bg="#1e293b")
        remove_buttons_frame.pack(pady=15, padx=10, fill="x")

        tk.Button(
            remove_buttons_frame,
            text="🔓 إزالة الحماية",
            command=self.remove_protection_action,
            bg="#10b981",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#059669",
            bd=0,
        ).pack(side="right", padx=10)

        # Progress bar
        self.progress5 = ttk.Progressbar(scrollable_frame, mode="indeterminate")
        self.progress5.pack(pady=8, padx=20, fill="x")

        # ربط عجلة الماوس بالتمرير
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # تحديث Canvas عند تغيير حجم النافذة
        def update_canvas_width(event):
            canvas_width = event.width
            items = canvas.find_all()
            if items:
                canvas.itemconfig(items[0], width=canvas_width)
        canvas.bind('<Configure>', update_canvas_width)

    def select_pdf_for_protection(self):
        file_path = filedialog.askopenfilename(
            title="اختر ملف PDF للحماية", filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.protect_pdf_file = file_path
            self.protect_file_label.config(
                text=os.path.basename(file_path), fg="#22c55e"
            )

    def protect_pdf_action(self):
        if not hasattr(self, "protect_pdf_file"):
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        password = self.password_var.get().strip()
        if not password:
            messagebox.showwarning("تحذير", "أدخل كلمة المرور!")
            return

        save_option = self.protect_save_option.get()
        if save_option == "same":
            # حفظ على نفس الملف
            output_path = self.protect_pdf_file
            # تأكيد من المستخدم
            if not messagebox.askyesno(
                "تأكيد",
                f"سيتم حفظ الملف المحمي على نفس الملف:\n{os.path.basename(output_path)}\n\nهل تريد المتابعة؟"
            ):
                return
        else:
            # حفظ باسم جديد
            output_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
            )
            if not output_path:
                return

        threading.Thread(
            target=self.process_protect_pdf, args=(output_path, password), daemon=True
        ).start()

    def process_protect_pdf(self, output_path: str, password: str):
        try:
            self.progress5.start()
            pdf_ops.protect_pdf_with_password(
                self.protect_pdf_file, output_path, password
            )
            self.root.after(0, self.progress5.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم حماية الملف بكلمة مرور!\n📁 {os.path.basename(output_path)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_protect_fields)
        except Exception as e:
            self.root.after(0, self.progress5.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def select_protected_pdf(self):
        file_path = filedialog.askopenfilename(
            title="اختر ملف PDF محمي", filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.remove_protect_pdf_file = file_path
            self.remove_protect_file_label.config(
                text=os.path.basename(file_path), fg="#22c55e"
            )

    def remove_protection_action(self):
        if not hasattr(self, "remove_protect_pdf_file"):
            messagebox.showwarning("تحذير", "اختر ملف PDF محمي أولاً!")
            return

        password = self.remove_password_var.get().strip()
        if not password:
            messagebox.showwarning("تحذير", "أدخل كلمة المرور!")
            return

        save_option = self.remove_protect_save_option.get()
        if save_option == "same":
            # حفظ على نفس الملف
            output_path = self.remove_protect_pdf_file
            # تأكيد من المستخدم
            if not messagebox.askyesno(
                "تأكيد",
                f"سيتم حفظ الملف غير المحمي على نفس الملف:\n{os.path.basename(output_path)}\n\nهل تريد المتابعة؟"
            ):
                return
        else:
            # حفظ باسم جديد
            output_path = filedialog.asksaveasfilename(
                defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
            )
            if not output_path:
                return

        threading.Thread(
            target=self.process_remove_protection,
            args=(output_path, password),
            daemon=True,
        ).start()

    def process_remove_protection(self, output_path: str, password: str):
        try:
            self.progress5.start()
            pdf_ops.remove_password_protection(
                self.remove_protect_pdf_file, output_path, password
            )
            self.root.after(0, self.progress5.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم إزالة الحماية من الملف!\n📁 {os.path.basename(output_path)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_remove_protect_fields)
        except Exception as e:
            self.root.after(0, self.progress5.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def clear_protect_fields(self):
        """مسح حقول قسم الحماية بعد النجاح"""
        if hasattr(self, "protect_pdf_file"):
            delattr(self, "protect_pdf_file")
        self.protect_file_label.config(text="لم يتم اختيار ملف", fg="#9ca3af")
        self.password_var.set("")

    def clear_remove_protect_fields(self):
        """مسح حقول قسم إزالة الحماية بعد النجاح"""
        if hasattr(self, "remove_protect_pdf_file"):
            delattr(self, "remove_protect_pdf_file")
        self.remove_protect_file_label.config(text="لم يتم اختيار ملف", fg="#9ca3af")
        self.remove_password_var.set("")

    def clear_tab1_fields(self):
        """مسح حقول تبويب تحرير PDF بعد النجاح"""
        if hasattr(self, "selected_file"):
            self.selected_file = None
        if hasattr(self, "file_label"):
            self.file_label.config(text="لم يتم اختيار ملف", fg="#9ca3af")
        if hasattr(self, "pages_label"):
            self.pages_label.config(text="📄 الصفحات: 0")
        if hasattr(self, "selected_pages"):
            self.selected_pages.clear()
        if hasattr(self, "page_order"):
            self.page_order = []
        if hasattr(self, "page_rotations"):
            self.page_rotations = {}
        if hasattr(self, "original_rotations"):
            self.original_rotations = {}
        if hasattr(self, "canvas"):
            self.canvas.delete("all")
        if hasattr(self, "page_labels"):
            self.page_labels.clear()
        if hasattr(self, "page_thumbnails"):
            self.page_thumbnails.clear()
        if hasattr(self, "total_pages"):
            self.total_pages = 0
        # تحديث عداد الصفحات المحددة
        if hasattr(self, "update_selection_count"):
            self.update_selection_count()

    def clear_tab2_fields(self):
        """مسح حقول تبويب دمج صور بعد النجاح"""
        if hasattr(self, "selected_images"):
            self.selected_images.clear()
        if hasattr(self, "selected_image_indices"):
            self.selected_image_indices.clear()
        if hasattr(self, "images_label"):
            self.images_label.config(text="لم يتم اختيار صور", fg="#9ca3af")
        if hasattr(self, "images_canvas"):
            self.images_canvas.delete("all")
        if hasattr(self, "image_canvas_images"):
            self.image_canvas_images.clear()

    def clear_tab3_fields(self):
        """مسح حقول تبويب استخراج صور بعد النجاح"""
        if hasattr(self, "export_file_path"):
            self.export_file_path = None
        if hasattr(self, "export_file_label"):
            self.export_file_label.config(text="لم يتم اختيار ملف", fg="#9ca3af")
        if hasattr(self, "export_pages_label"):
            self.export_pages_label.config(text="📄 الصفحات: 0")
        if hasattr(self, "export_dpi_var"):
            self.export_dpi_var.set("600")
        if hasattr(self, "export_pages_var"):
            self.export_pages_var.set("")
        if hasattr(self, "export_format_var"):
            self.export_format_var.set("png")

    def clear_tab4_fields(self):
        """مسح حقول تبويب دمج وتقسيم PDF بعد النجاح"""
        # مسح حقول الدمج
        if hasattr(self, "selected_pdfs_to_merge"):
            self.selected_pdfs_to_merge.clear()
        if hasattr(self, "merge_listbox"):
            self.merge_listbox.delete(0, tk.END)
        # مسح حقول التقسيم
        if hasattr(self, "split_pdf_file"):
            self.split_pdf_file = None
        if hasattr(self, "split_file_label"):
            self.split_file_label.config(text="لم يتم اختيار ملف", fg="#9ca3af")
        if hasattr(self, "num_parts_var"):
            self.num_parts_var.set("2")
        if hasattr(self, "ranges_var"):
            self.ranges_var.set("")

    def save_pdf(self):
        if not self.selected_pages:
            messagebox.showwarning("تحذير", "اختر صفحات للحذف أولاً!")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        pages_to_delete = sorted(self.selected_pages, reverse=True)

        threading.Thread(
            target=self.process_and_save, args=(output_path, pages_to_delete), daemon=True
        ).start()

    def process_rotate_selected(
        self, output_path: str, pages_to_rotate, angle: int
    ):
        try:
            self.progress.start()

            rotated_count = pdf_ops.rotate_pages(
                self.selected_file, pages_to_rotate, angle, output_path
            )

            self.root.after(0, self.progress.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم حفظ الملف بعد التدوير!\n📁 {os.path.basename(output_path)}\n\nتم تدوير {rotated_count} صفحة",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab1_fields)
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def process_and_save_selected(self, output_path: str, pages_to_keep):
        try:
            self.progress.start()
            
            # حفظ في ملف مؤقت أولاً
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path = temp_file.name
            temp_file.close()

            kept_count = pdf_ops.extract_pages(
                self.selected_file, pages_to_keep, temp_path
            )
            
            # تطبيق التدويرات إذا كانت موجودة
            if self.page_rotations:
                # إعادة ترتيب التدويرات حسب الصفحات المحفوظة
                kept_rotations = {}
                for new_idx, old_idx in enumerate(sorted(pages_to_keep)):
                    if old_idx in self.page_rotations:
                        kept_rotations[new_idx] = self.page_rotations[old_idx]
                self.apply_rotations_to_pdf(temp_path, output_path, kept_rotations)
            else:
                import shutil
                shutil.move(temp_path, output_path)

            self.root.after(0, self.progress.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم حفظ الملف!\n📁 {os.path.basename(output_path)}\n\nتم حفظ {kept_count} صفحة محددة",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab1_fields)
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def process_and_save(self, output_path: str, pages_to_delete):
        try:
            self.progress.start()
            
            # حفظ في ملف مؤقت أولاً
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path = temp_file.name
            temp_file.close()

            deleted_count = pdf_ops.delete_pages(
                self.selected_file, pages_to_delete, temp_path
            )
            
            # تطبيق التدويرات إذا كانت موجودة
            if self.page_rotations:
                # إعادة ترتيب التدويرات بعد الحذف
                remaining_rotations = {}
                pages_to_keep = [i for i in range(self.total_pages) if i not in pages_to_delete]
                for new_idx, old_idx in enumerate(pages_to_keep):
                    if old_idx in self.page_rotations:
                        remaining_rotations[new_idx] = self.page_rotations[old_idx]
                self.apply_rotations_to_pdf(temp_path, output_path, remaining_rotations)
            else:
                import shutil
                shutil.move(temp_path, output_path)

            self.root.after(0, self.progress.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم حفظ الملف!\n📁 {os.path.basename(output_path)}\n\nتم حذف {deleted_count} صفحة",
                ),
            )
            # مسح جميع الحقول بعد الحفظ
            self.root.after(0, self.clear_tab1_fields)
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def save_compressed_pdf(self):
        if not self.selected_file:
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        output_path = filedialog.asksaveasfilename(
            title="حفظ نسخة مضغوطة",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        threading.Thread(
            target=self.compress_and_save, args=(output_path,), daemon=True
        ).start()

    def compress_and_save(self, output_path: str):
        try:
            self.progress.start()
            
            # حفظ في ملف مؤقت أولاً
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_path = temp_file.name
            temp_file.close()

            pdf_ops.compress_pdf(self.selected_file, temp_path)
            
            # تطبيق التدويرات إذا كانت موجودة
            if self.page_rotations:
                self.apply_rotations_to_pdf(temp_path, output_path, self.page_rotations)
            else:
                import shutil
                shutil.move(temp_path, output_path)

            self.root.after(0, self.progress.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم حفظ النسخة المضغوطة!\n📁 {os.path.basename(output_path)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab1_fields)
        except Exception as e:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    # ================= وظائف TAB 2 =================
    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("صور", "*.png *.jpg *.jpeg *.bmp *.gif"), ("الكل", "*.*")]
        )
        if file_paths:
            self.selected_images.extend(file_paths)
            self.selected_image_indices.clear()  # مسح التحديد عند إضافة صور جديدة
            self.images_label.config(
                text=f"✅ تم اختيار {len(self.selected_images)} صورة", fg="#22c55e"
            )
            self.display_selected_images()

    def display_selected_images(self):
        self.images_canvas.delete("all")
        self.image_canvas_images.clear()

        cols = 4
        base_w = 180
        base_h = 250
        margin = 15

        for i, img_path in enumerate(self.selected_images):
            try:
                img = Image.open(img_path)
                img.thumbnail((base_w - 20, base_h - 60), Image.Resampling.LANCZOS)

                col = i % cols
                row = i // cols
                x = col * (base_w + margin) + margin
                y = row * (base_h + margin) + margin

                photo = ImageTk.PhotoImage(img)
                self.image_canvas_images.append(photo)

                # تحديد لون الإطار حسب التحديد
                outline_color = "#ef4444" if i in self.selected_image_indices else "#2563eb"
                outline_width = 4 if i in self.selected_image_indices else 2

                rect_tag = f"img_rect_{i}"
                text_tag = f"img_text_{i}"
                img_tag = f"img_img_{i}"
                filename_tag = f"img_filename_{i}"

                self.images_canvas.create_rectangle(
                    x,
                    y,
                    x + base_w,
                    y + base_h,
                    outline=outline_color,
                    width=outline_width,
                    tags=rect_tag,
                )

                self.images_canvas.create_text(
                    x + base_w // 2,
                    y + 15,
                    text=f"#{i + 1}",
                    font=("Arial", 13, "bold"),
                    fill="#111827",
                    tags=text_tag,
                )

                self.images_canvas.create_image(
                    x + base_w // 2,
                    y + base_h // 2,
                    image=photo,
                    anchor="center",
                    tags=img_tag,
                )

                filename = os.path.basename(img_path)
                self.images_canvas.create_text(
                    x + base_w // 2,
                    y + base_h - 10,
                    text=filename[:22],
                    font=("Arial", 9, "bold"),
                    fill="#374151",
                    tags=filename_tag,
                )

                # ربط أحداث النقر والسحب
                for tag in (rect_tag, text_tag, img_tag, filename_tag):
                    self.images_canvas.tag_bind(
                        tag,
                        "<Button-1>",
                        lambda e, idx=i: self.start_image_drag(e, idx),
                    )
                    self.images_canvas.tag_bind(tag, "<B1-Motion>", self.on_image_drag)
                    self.images_canvas.tag_bind(tag, "<ButtonRelease-1>", self.end_image_drag)

            except Exception as e:
                print(f"خطأ: {img_path}")

        self.images_canvas.configure(scrollregion=self.images_canvas.bbox("all"))

    def select_all_images(self):
        """تحديد جميع الصور"""
        self.selected_image_indices = set(range(len(self.selected_images)))
        self.display_selected_images()

    def clear_image_selection(self):
        """إلغاء تحديد جميع الصور"""
        self.selected_image_indices.clear()
        self.display_selected_images()

    def clear_images(self):
        self.selected_images.clear()
        self.selected_image_indices.clear()
        self.images_label.config(text="لم يتم اختيار صور", fg="#9ca3af")
        self.display_selected_images()

    def start_image_drag(self, event, img_idx: int):
        """بدء السحب لإعادة الترتيب أو التحديد"""
        self.image_drag_data["item"] = img_idx
        self.image_drag_data["start_pos"] = (event.x, event.y)
        self.image_drag_data["x"] = event.x
        self.image_drag_data["y"] = event.y

    def on_image_drag(self, event):
        """أثناء السحب"""
        if self.image_drag_data["item"] is not None:
            dx = abs(event.x - self.image_drag_data["x"])
            dy = abs(event.y - self.image_drag_data["y"])

            if dx > 5 or dy > 5:
                new_idx = self.get_image_at_position(event.x, event.y)
                if new_idx is not None and new_idx != self.image_drag_data["item"]:
                    old_idx = self.image_drag_data["item"]
                    self.selected_images.insert(new_idx, self.selected_images.pop(old_idx))
                    # تحديث التحديد
                    if old_idx in self.selected_image_indices:
                        self.selected_image_indices.remove(old_idx)
                        self.selected_image_indices.add(new_idx)
                    self.image_drag_data["item"] = new_idx
                    self.display_selected_images()

    def end_image_drag(self, event):
        """إنهاء السحب"""
        if self.image_drag_data["item"] is not None:
            if self.image_drag_data["start_pos"]:
                dx = abs(event.x - self.image_drag_data["start_pos"][0])
                dy = abs(event.y - self.image_drag_data["start_pos"][1])
                if dx < 5 and dy < 5:
                    # نقر عادي - تبديل التحديد
                    img_idx = self.image_drag_data["item"]
                    if img_idx in self.selected_image_indices:
                        self.selected_image_indices.remove(img_idx)
                    else:
                        self.selected_image_indices.add(img_idx)
                    self.display_selected_images()
                    return

            self.image_drag_data["item"] = None
            self.image_drag_data["start_pos"] = None

    def get_image_at_position(self, x, y):
        """الحصول على فهرس الصورة في الموضع المحدد"""
        canvas_y = self.images_canvas.canvasy(y)
        cols = 4
        base_w = 180
        base_h = 250
        margin = 15

        col = int((x - margin) / (base_w + margin))
        row = int((canvas_y - margin) / (base_h + margin))

        if col < 0 or col >= cols:
            return None

        img_idx = row * cols + col
        if 0 <= img_idx < len(self.selected_images):
            return img_idx
        return None

    def move_image_up(self):
        """نقل الصور المحددة لأعلى"""
        if not self.selected_image_indices:
            messagebox.showwarning("تحذير", "اختر صورة أولاً!")
            return

        if len(self.selected_images) < 2:
            messagebox.showwarning("تحذير", "أنت بحاجة لصورتين على الأقل!")
            return

        # نقل الصور المحددة لأعلى (من الأصغر للأكبر)
        indices_to_move = sorted(self.selected_image_indices)
        updated_indices = set()

        for idx in indices_to_move:
            if idx > 0:  # يمكن النقل لأعلى
                # التبديل مع الصورة السابقة
                self.selected_images[idx], self.selected_images[idx - 1] = (
                    self.selected_images[idx - 1],
                    self.selected_images[idx],
                )
                # تحديث التحديد
                updated_indices.add(idx - 1)
                if idx - 1 in self.selected_image_indices:
                    updated_indices.add(idx)
            else:
                updated_indices.add(idx)

        self.selected_image_indices = updated_indices
        self.display_selected_images()

    def move_image_down(self):
        """نقل الصور المحددة لأسفل"""
        if not self.selected_image_indices:
            messagebox.showwarning("تحذير", "اختر صورة أولاً!")
            return

        if len(self.selected_images) < 2:
            messagebox.showwarning("تحذير", "أنت بحاجة لصورتين على الأقل!")
            return

        # نقل الصور المحددة لأسفل (من الأكبر للأصغر)
        indices_to_move = sorted(self.selected_image_indices, reverse=True)
        updated_indices = set()

        for idx in indices_to_move:
            if idx < len(self.selected_images) - 1:  # يمكن النقل لأسفل
                # التبديل مع الصورة التالية
                self.selected_images[idx], self.selected_images[idx + 1] = (
                    self.selected_images[idx + 1],
                    self.selected_images[idx],
                )
                # تحديث التحديد
                updated_indices.add(idx + 1)
                if idx + 1 in self.selected_image_indices:
                    updated_indices.add(idx)
            else:
                updated_indices.add(idx)

        self.selected_image_indices = updated_indices
        self.display_selected_images()

    def remove_selected_image(self):
        """حذف الصور المحددة"""
        if not self.selected_image_indices:
            messagebox.showwarning("تحذير", "اختر صوراً للحذف أولاً!")
            return

        # حذف الصور المحددة (من الأكبر للأصغر لتجنب مشاكل الفهارس)
        indices_to_remove = sorted(self.selected_image_indices, reverse=True)
        for idx in indices_to_remove:
            if 0 <= idx < len(self.selected_images):
                self.selected_images.pop(idx)

        self.selected_image_indices.clear()
        self.images_label.config(
            text=f"✅ تم اختيار {len(self.selected_images)} صورة"
            if self.selected_images
            else "لم يتم اختيار صور",
            fg="#22c55e" if self.selected_images else "#9ca3af",
        )
        self.display_selected_images()

    def update_custom_input_state(self):
        """تفعيل/تعطيل حقل عدد الصور"""
        if self.image_layout_var.get() == "custom":
            self.custom_count_entry.config(state="normal")
        else:
            self.custom_count_entry.config(state="disabled")

    def preview_images_pdf(self):
        """معاينة PDF قبل الحفظ"""
        if not self.selected_images:
            messagebox.showwarning("تحذير", "اختر صوراً أولاً!")
            return

        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()

        threading.Thread(
            target=self.process_preview_images_pdf, args=(temp_path,), daemon=True
        ).start()

    def process_preview_images_pdf(self, temp_path: str):
        """معالجة معاينة PDF"""
        try:
            self.progress2.start()

            layout = self.image_layout_var.get()
            images_per_page = int(self.images_per_page_var.get()) if layout == "custom" else 1

            total_pages = image_ops.images_to_pdf(
                self.selected_images, temp_path, layout=layout, images_per_page=images_per_page
            )

            self.root.after(0, self.progress2.stop)
            self.root.after(0, lambda: self.show_images_preview(temp_path, total_pages))
        except Exception as e:
            self.root.after(0, self.progress2.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def show_images_preview(self, preview_pdf_path: str, total_pages: int):
        """نافذة معاينة PDF للصور"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("👁️ معاينة PDF")
        preview_window.geometry("1200x800")
        preview_window.configure(bg="#1e293b")
        preview_window.transient(self.root)

        # رأس النافذة
        header_frame = tk.Frame(preview_window, bg="#8b5cf6", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=f"👁️ معاينة PDF - {total_pages} صفحة",
            font=("Arial", 18, "bold"),
            fg="#ffffff",
            bg="#8b5cf6",
        ).pack(expand=True)

        # Canvas للمعاينة
        canvas_frame = tk.LabelFrame(
            preview_window,
            text="📄 الصفحات",
            font=("Arial", 14, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scroll_frame = tk.Frame(canvas_frame, bg="#1e293b")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        preview_canvas = tk.Canvas(scroll_frame, bg="#f9fafb", highlightthickness=0)
        preview_scrollbar = ttk.Scrollbar(
            scroll_frame, orient="vertical", command=preview_canvas.yview
        )
        preview_canvas.configure(yscrollcommand=preview_scrollbar.set)

        preview_scrollbar.pack(side="right", fill="y")
        preview_canvas.pack(side="left", fill="both", expand=True)

        # ربط التمرير بالماوس
        def on_mousewheel(event):
            preview_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        preview_canvas.bind("<MouseWheel>", on_mousewheel)
        preview_canvas.bind("<Enter>", lambda e: preview_canvas.focus_set())

        # تحميل الصور المصغرة
        def load_preview():
            try:
                thumbnails = pdf_ops.load_page_thumbnails(preview_pdf_path, scale=0.25)
                canvas_images = []

                cols = 2
                base_w = 400
                base_h = 550
                margin = 20

                for i, img in enumerate(thumbnails):
                    col = i % cols
                    row = i // cols

                    x = col * (base_w + margin) + margin
                    y = row * (base_h + margin) + margin

                    img_resized = img.resize(
                        (base_w - 40, base_h - 80), Image.Resampling.LANCZOS
                    )
                    photo = ImageTk.PhotoImage(img_resized)
                    canvas_images.append(photo)

                    preview_canvas.create_rectangle(
                        x, y, x + base_w, y + base_h, fill="#ffffff", outline="#d1d5db", width=2
                    )

                    preview_canvas.create_text(
                        x + base_w // 2,
                        y + 20,
                        text=f"صفحة {i + 1}",
                        font=("Arial", 14, "bold"),
                        fill="#111827",
                    )

                    preview_canvas.create_image(
                        x + base_w // 2, y + base_h // 2, image=photo, anchor="center"
                    )

                preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))
                preview_canvas.canvas_images = canvas_images
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في تحميل المعاينة:\n{str(e)}")

        threading.Thread(target=load_preview, daemon=True).start()

        # أزرار التحكم
        control_frame = tk.Frame(preview_window, bg="#1e293b")
        control_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            control_frame,
            text="💾 حفظ",
            command=lambda: self.save_preview_images_pdf(preview_window, preview_pdf_path),
            bg="#22c55e",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#16a34a",
            bd=0,
        ).pack(side="right", padx=10)

        tk.Button(
            control_frame,
            text="❌ إلغاء",
            command=lambda: self.cancel_images_preview(preview_window, preview_pdf_path),
            bg="#ef4444",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="right", padx=10)

    def save_preview_images_pdf(self, preview_window, temp_path: str):
        """حفظ PDF من المعاينة"""
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if output_path:
            try:
                import shutil
                shutil.copy2(temp_path, output_path)
                messagebox.showinfo(
                    "✅ نجح", f"تم حفظ الملف!\n📁 {os.path.basename(output_path)}"
                )
                preview_window.destroy()
                os.unlink(temp_path)
                # مسح الحقول بعد النجاح
                self.clear_tab2_fields()
            except Exception as e:
                messagebox.showerror("❌ خطأ", f"خطأ في الحفظ:\n{str(e)}")
        else:
            preview_window.destroy()
            os.unlink(temp_path)

    def cancel_images_preview(self, preview_window, temp_path: str):
        """إلغاء المعاينة"""
        preview_window.destroy()
        try:
            os.unlink(temp_path)
        except:
            pass

    def save_images_as_pdf(self):
        """حفظ PDF مباشرة"""
        if not self.selected_images:
            messagebox.showwarning("تحذير", "اختر صوراً أولاً!")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if not output_path:
            return

        threading.Thread(
            target=self.process_images_to_pdf, args=(output_path,), daemon=True
        ).start()

    def process_images_to_pdf(self, output_path: str):
        try:
            self.progress2.start()

            layout = self.image_layout_var.get()
            images_per_page = int(self.images_per_page_var.get()) if layout == "custom" else 1

            total_pages = image_ops.images_to_pdf(
                self.selected_images, output_path, layout=layout, images_per_page=images_per_page
            )

            self.root.after(0, self.progress2.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم دمج {len(self.selected_images)} صورة في {total_pages} صفحة!\n📁 {os.path.basename(output_path)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab2_fields)
        except Exception as e:
            self.root.after(0, self.progress2.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    # ================= وظائف TAB 3 =================
    def select_pdf_for_export(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            threading.Thread(
                target=self.load_pdf_for_export, args=(file_path,), daemon=True
            ).start()

    def load_pdf_for_export(self, file_path):
        try:
            thumbnails = pdf_ops.load_page_thumbnails(file_path, scale=0.1)
            total_pages = len(thumbnails)

            self.export_file_path = file_path
            self.root.after(
                0,
                lambda: self.export_file_label.config(
                    text=os.path.basename(file_path), fg="#22c55e"
                ),
            )
            self.root.after(
                0,
                lambda: self.export_pages_label.config(
                    text=f"📄 الصفحات: {total_pages}"
                ),
            )
        except Exception as e:
            self.root.after(
                0, lambda: messagebox.showerror("❌ خطأ", f"خطأ في تحميل:\n{str(e)}")
            )

    def export_pages_as_images(self):
        if not hasattr(self, "export_file_path"):
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        output_dir = filedialog.askdirectory(title="اختر مجلد الحفظ")
        if not output_dir:
            return

        format_ext = self.export_format.get()
        dpi_str = self.export_dpi_var.get().strip() or "600"
        try:
            dpi = int(dpi_str)
            if dpi < 72:
                raise ValueError("DPI يجب أن يكون 72 أو أكثر")
        except ValueError as e:
            messagebox.showerror("خطأ", f"DPI غير صحيح: {e}")
            return

        pages_str = self.export_pages_var.get().strip()
        pages_list = None
        if pages_str:
            try:
                pages_list = []
                parts = pages_str.split(",")
                for part in parts:
                    part = part.strip()
                    if "-" in part:
                        start_str, end_str = part.split("-", 1)
                        start = int(start_str.strip()) - 1
                        end = int(end_str.strip()) - 1
                        if start < 0 or end < start:
                            raise ValueError(f"نطاق غير صحيح: {part}")
                        pages_list.extend(list(range(start, end + 1)))
                    else:
                        page = int(part) - 1
                        if page < 0:
                            raise ValueError(f"رقم صفحة غير صحيح: {part}")
                        pages_list.append(page)
            except ValueError as e:
                messagebox.showerror("خطأ", f"تنسيق الصفحات غير صحيح: {e}")
                return

        threading.Thread(
            target=self.process_export_images,
            args=(self.export_file_path, output_dir, format_ext, dpi, pages_list),
            daemon=True,
        ).start()

    def process_export_images(
        self,
        pdf_path: str,
        output_dir: str,
        format_ext: str,
        dpi: int,
        pages: Optional[list],
    ):
        try:
            self.progress3.start()

            if pages:
                total_pages = pdf_ops.export_selected_pages_to_images(
                    pdf_path, pages, output_dir, format_ext=format_ext, dpi=dpi
                )
            else:
                total_pages = pdf_ops.export_pages_to_images(
                    pdf_path, output_dir, format_ext=format_ext, dpi=dpi
                )

            self.root.after(0, self.progress3.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم استخراج {total_pages} صورة!\n📁 {os.path.basename(output_dir)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab3_fields)
        except Exception as e:
            self.root.after(0, self.progress3.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    # ================= TAB 4: دمج وتقسيم PDF =================
    def setup_tab4_merge_split(self):
        # قسم دمج PDF
        merge_frame = tk.LabelFrame(
            self.tab4,
            text="🔀 دمج ملفات PDF متعددة",
            font=("Arial", 16, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        merge_frame.pack(pady=15, padx=20, fill="x")

        merge_control = tk.Frame(merge_frame, bg="#334155")
        merge_control.pack(pady=10, padx=10, fill="x")

        tk.Button(
            merge_control,
            text="اختر ملفات PDF",
            command=self.select_pdfs_to_merge,
            bg="#2563eb",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=25,
            pady=10,
            image=self.icons.get('file'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(side="right", padx=10)

        self.merge_files_label = tk.Label(
            merge_control,
            text="لم يتم اختيار ملفات",
            font=("Arial", 13, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.merge_files_label.pack(side="right", padx=10)

        tk.Button(
            merge_control,
            text="مسح",
            command=self.clear_merge_list,
            bg="#ef4444",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=6,
            image=self.icons.get('delete'),
            compound="left",
            activebackground="#b91c1c",
            bd=0,
        ).pack(side="left", padx=10)

        tk.Button(
            merge_frame,
            text="🔀 دمج الملفات",
            command=self.merge_pdfs_action,
            bg="#22c55e",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#16a34a",
            bd=0,
        ).pack(pady=10)

        # قسم تقسيم PDF
        split_frame = tk.LabelFrame(
            self.tab4,
            text="✂️ تقسيم ملف PDF",
            font=("Arial", 16, "bold"),
            fg="#e5e7eb",
            bg="#1e293b",
        )
        split_frame.pack(pady=15, padx=20, fill="x")

        split_file_frame = tk.Frame(split_frame, bg="#334155")
        split_file_frame.pack(pady=10, padx=10, fill="x")

        tk.Button(
            split_file_frame,
            text="اختر ملف PDF",
            command=self.select_pdf_to_split,
            bg="#2563eb",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=25,
            pady=10,
            image=self.icons.get('file'),
            compound="left",
            activebackground="#1d4ed8",
            bd=0,
        ).pack(side="right", padx=10)

        self.split_file_label = tk.Label(
            split_file_frame,
            text="لم يتم اختيار ملف",
            font=("Arial", 13, "bold"),
            fg="#9ca3af",
            bg="#334155",
        )
        self.split_file_label.pack(side="right", padx=10)

        split_options = tk.Frame(split_frame, bg="#1e293b")
        split_options.pack(pady=15, padx=10, fill="x")

        tk.Label(
            split_options,
            text="عدد الأجزاء:",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        self.num_parts_var = tk.StringVar(value="2")
        parts_entry = tk.Entry(
            split_options,
            textvariable=self.num_parts_var,
            font=("Arial", 13),
            width=10,
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
        )
        parts_entry.pack(side="right", padx=10)

        tk.Button(
            split_frame,
            text="✂️ تقسيم إلى أجزاء متساوية",
            command=self.split_pdf_equal_action,
            bg="#f97316",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#ea580c",
            bd=0,
        ).pack(pady=10)

        tk.Label(
            split_frame,
            text="أو أدخل النطاقات يدوياً (مثال: 1-5,6-10,11-15)",
            font=("Arial", 12),
            bg="#1e293b",
            fg="#9ca3af",
        ).pack(pady=5)

        ranges_frame = tk.Frame(split_frame, bg="#1e293b")
        ranges_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(
            ranges_frame,
            text="النطاقات:",
            font=("Arial", 13, "bold"),
            bg="#1e293b",
            fg="#e5e7eb",
        ).pack(side="right", padx=10)

        self.ranges_var = tk.StringVar(value="")
        ranges_entry = tk.Entry(
            ranges_frame,
            textvariable=self.ranges_var,
            font=("Arial", 12),
            width=40,
            bg="#1e293b",
            fg="#e5e7eb",
            insertbackground="#e5e7eb",
        )
        ranges_entry.pack(side="right", padx=10, fill="x", expand=True)

        tk.Button(
            split_frame,
            text="✂️ تقسيم حسب النطاقات",
            command=self.split_pdf_ranges_action,
            bg="#a855f7",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=30,
            pady=12,
            activebackground="#9333ea",
            bd=0,
        ).pack(pady=10)

        self.progress4 = ttk.Progressbar(self.tab4, mode="indeterminate")
        self.progress4.pack(pady=8, padx=20, fill="x")

    def select_pdfs_to_merge(self):
        file_paths = filedialog.askopenfilenames(
            title="اختر ملفات PDF للدمج",
            filetypes=[("PDF files", "*.pdf")],
        )
        if file_paths:
            self.selected_pdfs_to_merge = list(file_paths)
            self.merge_files_label.config(
                text=f"✅ تم اختيار {len(self.selected_pdfs_to_merge)} ملف",
                fg="#22c55e",
            )

    def clear_merge_list(self):
        self.selected_pdfs_to_merge.clear()
        self.merge_files_label.config(text="لم يتم اختيار ملفات", fg="#9ca3af")

    def merge_pdfs_action(self):
        if not self.selected_pdfs_to_merge:
            messagebox.showwarning("تحذير", "اختر ملفات PDF أولاً!")
            return

        output_path = filedialog.asksaveasfilename(
            title="حفظ ملف PDF المدمج",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if not output_path:
            return

        threading.Thread(
            target=self.process_merge_pdfs, args=(output_path,), daemon=True
        ).start()

    def process_merge_pdfs(self, output_path: str):
        try:
            self.progress4.start()
            total_pages = pdf_ops.merge_pdfs(
                self.selected_pdfs_to_merge, output_path
            )
            self.root.after(0, self.progress4.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم دمج {len(self.selected_pdfs_to_merge)} ملف!\n📁 {os.path.basename(output_path)}\n\nإجمالي الصفحات: {total_pages}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab4_fields)
        except Exception as e:
            self.root.after(0, self.progress4.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def select_pdf_to_split(self):
        file_path = filedialog.askopenfilename(
            title="اختر ملف PDF للتقسيم", filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.split_pdf_file = file_path
            self.split_file_label.config(
                text=os.path.basename(file_path), fg="#22c55e"
            )

    def split_pdf_equal_action(self):
        if not self.split_pdf_file:
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        try:
            num_parts = int(self.num_parts_var.get())
            if num_parts < 1:
                raise ValueError("عدد الأجزاء يجب أن يكون >= 1")
        except ValueError as e:
            messagebox.showerror("خطأ", f"عدد غير صحيح: {e}")
            return

        output_dir = filedialog.askdirectory(title="اختر مجلد الحفظ")
        if not output_dir:
            return

        threading.Thread(
            target=self.process_split_equal,
            args=(self.split_pdf_file, num_parts, output_dir),
            daemon=True,
        ).start()

    def process_split_equal(self, pdf_path: str, num_parts: int, output_dir: str):
        try:
            self.progress4.start()
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            files_created = pdf_ops.split_pdf_equal(
                pdf_path, num_parts, output_dir, base_name
            )
            self.root.after(0, self.progress4.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم تقسيم الملف إلى {files_created} جزء!\n📁 {os.path.basename(output_dir)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab4_fields)
        except Exception as e:
            self.root.after(0, self.progress4.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    def split_pdf_ranges_action(self):
        if not self.split_pdf_file:
            messagebox.showwarning("تحذير", "اختر ملف PDF أولاً!")
            return

        ranges_str = self.ranges_var.get().strip()
        if not ranges_str:
            messagebox.showwarning("تحذير", "أدخل النطاقات أولاً!")
            return

        try:
            ranges = []
            parts = ranges_str.split(",")
            for part in parts:
                part = part.strip()
                if "-" not in part:
                    raise ValueError(f"نطاق غير صحيح: {part}")
                start_str, end_str = part.split("-", 1)
                start = int(start_str.strip()) - 1
                end = int(end_str.strip()) - 1
                if start < 0 or end < start:
                    raise ValueError(f"نطاق غير صحيح: {part}")
                ranges.append((start, end))
        except ValueError as e:
            messagebox.showerror("خطأ", f"تنسيق النطاقات غير صحيح: {e}")
            return

        output_dir = filedialog.askdirectory(title="اختر مجلد الحفظ")
        if not output_dir:
            return

        threading.Thread(
            target=self.process_split_ranges,
            args=(self.split_pdf_file, ranges, output_dir),
            daemon=True,
        ).start()

    def process_split_ranges(
        self, pdf_path: str, ranges: list, output_dir: str
    ):
        try:
            self.progress4.start()
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            files_created = pdf_ops.split_pdf_by_ranges(
                pdf_path, ranges, output_dir, base_name
            )
            self.root.after(0, self.progress4.stop)
            self.root.after(
                0,
                lambda: show_custom_message(self.root,
                    "✅ نجح",
                    f"تم تقسيم الملف إلى {files_created} جزء!\n📁 {os.path.basename(output_dir)}",
                ),
            )
            # مسح الحقول بعد النجاح
            self.root.after(0, self.clear_tab4_fields)
        except Exception as e:
            self.root.after(0, self.progress4.stop)
            self.root.after(0, lambda: messagebox.showerror("❌ خطأ", str(e)))

    # ================= وظائف مشتركة =================
    def _bind_mousewheel(self, _event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _unbind_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")

    def _on_mousewheel(self, event):
        delta = -1 * (event.delta // 120)
        self.canvas.yview_scroll(delta, "units")

    def _on_shift_mousewheel(self, event):
        delta = -1 * (event.delta // 120)
        self.canvas.xview_scroll(delta, "units")

    # ================= TAB 6: تحرير محتوى PDF (معلق مؤقتاً) =================
    # سيتم تطوير هذا التبويب لاحقاً


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFImageProcessorPro(root)
    root.mainloop()
