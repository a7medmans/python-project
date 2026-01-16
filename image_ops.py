from typing import List, Tuple

from PIL import Image


def images_to_pdf(
    image_paths: List[str],
    output_path: str,
    layout: str = "one_per_page",
    images_per_page: int = 1,
    page_size: Tuple[int, int] = (595, 842),  # A4 default
) -> int:
    """
    Merge images into a single PDF.
    
    Args:
        image_paths: List of image file paths
        output_path: Output PDF path
        layout: "one_per_page" (fill page), "multiple" (auto-fit), or "custom" (user-specified count)
        images_per_page: Number of images per page (for custom layout)
        page_size: Page size in points (width, height), default A4 (595x842)
    
    Returns:
        Number of pages created
    """
    if not image_paths:
        raise ValueError("image_paths cannot be empty")

    pages = []
    page_width, page_height = page_size

    if layout == "one_per_page":
        # صورة واحدة بالصفحة (ملء الصفحة)
        # استخدام DPI عالي جداً (600 DPI) للحفاظ على الجودة القصوى
        target_dpi = 600
        dpi_scale = target_dpi / 72
        page_width_px = int(page_width * dpi_scale)
        page_height_px = int(page_height * dpi_scale)
        
        for img_path in image_paths:
            img = Image.open(img_path).convert("RGB")
            # استخدام الحجم الأصلي للصورة أولاً
            img_width, img_height = img.size
            
            # حساب الحجم المطلوب مع الحفاظ على النسبة
            ratio = min(page_width_px / img_width, page_height_px / img_height)
            
            # إذا كانت الصورة أصغر من الصفحة، نكبرها للحفاظ على الجودة
            if ratio > 1.0:
                # تكبير الصورة بجودة عالية
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                # الصورة كبيرة - نستخدم حجمها الأصلي أو نكبرها قليلاً
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # إنشاء صفحة جديدة بجودة عالية جداً
            page_img = Image.new("RGB", (page_width_px, page_height_px), "white")
            x_offset = (page_width_px - new_width) // 2
            y_offset = (page_height_px - new_height) // 2
            page_img.paste(img_resized, (x_offset, y_offset))
            
            # حفظ بالحجم الكبير (بدون تصغير) للحفاظ على الجودة
            pages.append(page_img)

    elif layout == "multiple":
        # أكثر من صورة (تلقائي - 2x2)
        # استخدام DPI عالي جداً (600 DPI)
        target_dpi = 600
        dpi_scale = target_dpi / 72
        page_width_px = int(page_width * dpi_scale)
        page_height_px = int(page_height * dpi_scale)
        
        cols = 2
        rows = 2
        img_width = int((page_width_px - 30) // cols)  # مع هامش
        img_height = int((page_height_px - 30) // rows)

        current_page = Image.new("RGB", (page_width_px, page_height_px), "white")
        current_count = 0

        for img_path in image_paths:
            img = Image.open(img_path).convert("RGB")
            # استخدام resize بدلاً من thumbnail للحفاظ على الجودة
            img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)
            thumb_width, thumb_height = img.size

            col = current_count % cols
            row = (current_count // cols) % rows
            x = 10 + col * (img_width + 10)
            y = 10 + row * (img_height + 10)

            current_page.paste(img, (x, y))
            current_count += 1

            if current_count % (cols * rows) == 0:
                # حفظ بالحجم الكبير
                pages.append(current_page)
                current_page = Image.new("RGB", (page_width_px, page_height_px), "white")

        if current_count % (cols * rows) != 0:
            pages.append(current_page)

    elif layout == "custom":
        # عدد محدد من الصور في الصفحة
        if images_per_page < 1:
            images_per_page = 1

        # استخدام DPI عالي جداً (600 DPI)
        target_dpi = 600
        dpi_scale = target_dpi / 72
        page_width_px = int(page_width * dpi_scale)
        page_height_px = int(page_height * dpi_scale)

        # حساب عدد الأعمدة والصفوف
        import math
        cols = math.ceil(math.sqrt(images_per_page))
        rows = math.ceil(images_per_page / cols)

        img_width = int((page_width_px - 20 * (cols + 1)) // cols)
        img_height = int((page_height_px - 20 * (rows + 1)) // rows)

        current_page = Image.new("RGB", (page_width_px, page_height_px), "white")
        current_count = 0

        for img_path in image_paths:
            img = Image.open(img_path).convert("RGB")
            img.thumbnail((img_width, img_height), Image.Resampling.LANCZOS)
            thumb_width, thumb_height = img.size

            col = current_count % cols
            row = (current_count // cols) % rows
            x = 20 + col * (img_width + 20)
            y = 20 + row * (img_height + 20)

            current_page.paste(img, (x, y))
            current_count += 1

            if current_count % images_per_page == 0:
                # حفظ بالحجم الكبير
                pages.append(current_page)
                current_page = Image.new("RGB", (page_width_px, page_height_px), "white")

        if current_count % images_per_page != 0:
            pages.append(current_page)

    else:
        raise ValueError(f"Unknown layout: {layout}")

    if pages:
        # حفظ بجودة عالية جداً (600 DPI)
        # استخدام optimize=False وcompress_level=0 للحفاظ على الجودة القصوى
        dpi = 600
        pages[0].save(
            output_path,
            save_all=True,
            append_images=pages[1:],
            resolution=dpi,
            quality=100,  # أقصى جودة
            optimize=False,  # عدم الضغط للحفاظ على الجودة
        )
    return len(pages)
