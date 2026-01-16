import io
import os
from typing import List, Dict, Any

import fitz  # PyMuPDF
from PIL import Image


def load_page_thumbnails(pdf_path: str, scale: float = 0.25) -> List[Image.Image]:
    """Return PIL thumbnails for each page in the PDF."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    thumbnails: List[Image.Image] = []
    doc = fitz.open(pdf_path)
    try:
        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            thumbnails.append(img)
    finally:
        doc.close()
    return thumbnails


def delete_pages(pdf_path: str, pages_to_delete: List[int], output_path: str) -> int:
    """Delete given pages (0-based) and save to output. Returns deleted count."""
    if not pages_to_delete:
        raise ValueError("pages_to_delete cannot be empty")

    doc = fitz.open(pdf_path)
    try:
        for page_no in sorted(set(pages_to_delete), reverse=True):
            if 0 <= page_no < doc.page_count:
                doc.delete_page(page_no)
        doc.save(output_path)
    finally:
        doc.close()
    return len(set(pages_to_delete))


def compress_pdf(pdf_path: str, output_path: str) -> None:
    """Save a compressed copy of the PDF."""
    doc = fitz.open(pdf_path)
    try:
        doc.save(output_path, deflate=True, garbage=4)
    finally:
        doc.close()


def extract_pages(pdf_path: str, pages_to_keep: List[int], output_path: str) -> int:
    """
    Create a new PDF that contains only the given 0-based pages (order preserved).
    Returns number of pages copied.
    """
    if not pages_to_keep:
        raise ValueError("pages_to_keep cannot be empty")

    src = fitz.open(pdf_path)
    dst = fitz.open()
    try:
        unique_pages = sorted(set(pages_to_keep))
        for page_index in unique_pages:
            if 0 <= page_index < src.page_count:
                dst.insert_pdf(src, from_page=page_index, to_page=page_index)
        dst.save(output_path)
    finally:
        src.close()
        dst.close()
    return len(unique_pages)


def rotate_pages(
    pdf_path: str, pages_to_rotate: List[int], angle: int, output_path: str
) -> int:
    """
    Rotate selected pages by angle (degrees, multiple of 90) and save to output_path.
    Returns number of pages rotated.
    """
    if not pages_to_rotate:
        raise ValueError("pages_to_rotate cannot be empty")

    doc = fitz.open(pdf_path)
    try:
        rotated_count = 0
        for page_index in sorted(set(pages_to_rotate)):
            if 0 <= page_index < doc.page_count:
                page = doc.load_page(page_index)
                page.set_rotation((page.rotation + angle) % 360)
                rotated_count += 1
        doc.save(output_path)
    finally:
        doc.close()
    return rotated_count


def export_pages_to_images(
    pdf_path: str, output_dir: str, format_ext: str = "png", dpi: int = 144
) -> int:
    """
    Export all pages as images to output_dir. Returns number of pages exported.
    format_ext: 'png' or 'jpg'. dpi controls rasterization quality.
    """
    if format_ext not in ("png", "jpg", "jpeg"):
        raise ValueError("format_ext must be png or jpg")

    os.makedirs(output_dir, exist_ok=True)

    scale = dpi / 72
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    try:
        for page_index in range(total_pages):
            page = doc.load_page(page_index)
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
            file_name = f"page_{page_index + 1:03d}.{format_ext}"
            img_path = os.path.join(output_dir, file_name)

            if format_ext.lower() == "png":
                pix.save(img_path)
            else:
                image = Image.open(io.BytesIO(pix.tobytes("png")))
                image.save(img_path, "JPEG", quality=85)
    finally:
        doc.close()

    return total_pages


def export_selected_pages_to_images(
    pdf_path: str,
    pages: List[int],
    output_dir: str,
    format_ext: str = "png",
    dpi: int = 144,
) -> int:
    """
    Export only selected 0-based pages as images. Returns number of pages exported.
    """
    if not pages:
        raise ValueError("pages cannot be empty")
    if format_ext not in ("png", "jpg", "jpeg"):
        raise ValueError("format_ext must be png or jpg")

    os.makedirs(output_dir, exist_ok=True)

    scale = dpi / 72
    doc = fitz.open(pdf_path)
    exported = 0
    try:
        for page_index in sorted(set(pages)):
            if 0 <= page_index < doc.page_count:
                page = doc.load_page(page_index)
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
                file_name = f"page_{page_index + 1:03d}.{format_ext}"
                img_path = os.path.join(output_dir, file_name)

                if format_ext.lower() == "png":
                    pix.save(img_path)
                else:
                    image = Image.open(io.BytesIO(pix.tobytes("png")))
                    image.save(img_path, "JPEG", quality=85)
                exported += 1
    finally:
        doc.close()

    return exported


def merge_pdfs(pdf_paths: List[str], output_path: str) -> int:
    """
    Merge multiple PDF files into one. Returns total number of pages merged.
    """
    if not pdf_paths:
        raise ValueError("pdf_paths cannot be empty")

    merged_doc = fitz.open()
    total_pages = 0

    try:
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF not found: {pdf_path}")
            src_doc = fitz.open(pdf_path)
            try:
                merged_doc.insert_pdf(src_doc)
                total_pages += src_doc.page_count
            finally:
                src_doc.close()

        merged_doc.save(output_path)
    finally:
        merged_doc.close()

    return total_pages


def split_pdf_by_ranges(
    pdf_path: str, ranges: List[tuple], output_dir: str, base_name: str = "part"
) -> int:
    """
    Split PDF into multiple files based on page ranges.
    ranges: List of (start_page, end_page) tuples (0-based, inclusive).
    Returns number of files created.
    """
    if not ranges:
        raise ValueError("ranges cannot be empty")

    os.makedirs(output_dir, exist_ok=True)
    src_doc = fitz.open(pdf_path)
    files_created = 0

    try:
        for idx, (start, end) in enumerate(ranges, 1):
            if start < 0 or end >= src_doc.page_count or start > end:
                continue

            dst_doc = fitz.open()
            try:
                dst_doc.insert_pdf(src_doc, from_page=start, to_page=end)
                output_file = os.path.join(output_dir, f"{base_name}_{idx:02d}.pdf")
                dst_doc.save(output_file)
                files_created += 1
            finally:
                dst_doc.close()
    finally:
        src_doc.close()

    return files_created


def split_pdf_equal(
    pdf_path: str, num_parts: int, output_dir: str, base_name: str = "part"
) -> int:
    """
    Split PDF into equal parts. Returns number of files created.
    """
    if num_parts < 1:
        raise ValueError("num_parts must be >= 1")

    src_doc = fitz.open(pdf_path)
    total_pages = src_doc.page_count

    if total_pages == 0:
        src_doc.close()
        return 0

    pages_per_part = (total_pages + num_parts - 1) // num_parts
    ranges = []

    for i in range(num_parts):
        start = i * pages_per_part
        end = min(start + pages_per_part - 1, total_pages - 1)
        if start < total_pages:
            ranges.append((start, end))

    src_doc.close()
    return split_pdf_by_ranges(pdf_path, ranges, output_dir, base_name)


def reorder_pages(pdf_path: str, new_order: List[int], output_path: str) -> int:
    """
    Reorder pages according to new_order (0-based indices).
    Returns number of pages in the new PDF.
    """
    if not new_order:
        raise ValueError("new_order cannot be empty")

    src_doc = fitz.open(pdf_path)
    dst_doc = fitz.open()
    try:
        for page_index in new_order:
            if 0 <= page_index < src_doc.page_count:
                dst_doc.insert_pdf(src_doc, from_page=page_index, to_page=page_index)
        dst_doc.save(output_path)
    finally:
        src_doc.close()
        dst_doc.close()

    return len(new_order)


def insert_pages_from_pdf(
    pdf_path: str,
    insert_pdf_path: str,
    insert_at: int,
    pages_to_insert: List[int] = None,
    output_path: str = None,
) -> int:
    """
    Insert pages from another PDF into the main PDF at position insert_at (0-based).
    If pages_to_insert is None, inserts all pages from insert_pdf_path.
    Returns total number of pages in the new PDF.
    """
    if output_path is None:
        output_path = pdf_path

    main_doc = fitz.open(pdf_path)
    insert_doc = fitz.open(insert_pdf_path)
    new_doc = fitz.open()

    try:
        # Copy pages before insert position
        for i in range(insert_at):
            if i < main_doc.page_count:
                new_doc.insert_pdf(main_doc, from_page=i, to_page=i)

        # Insert pages from the other PDF
        if pages_to_insert is None:
            pages_to_insert = list(range(insert_doc.page_count))
        for page_idx in pages_to_insert:
            if 0 <= page_idx < insert_doc.page_count:
                new_doc.insert_pdf(insert_doc, from_page=page_idx, to_page=page_idx)

        # Copy remaining pages from main PDF
        for i in range(insert_at, main_doc.page_count):
            new_doc.insert_pdf(main_doc, from_page=i, to_page=i)

        new_doc.save(output_path)
        total_pages = new_doc.page_count
    finally:
        main_doc.close()
        insert_doc.close()
        new_doc.close()

    return total_pages


def insert_blank_page(
    pdf_path: str, insert_at: int, width: float = 595, height: float = 842, output_path: str = None
) -> int:
    """
    Insert a blank page at position insert_at (0-based).
    width and height are in points (default A4: 595x842).
    Returns total number of pages in the new PDF.
    """
    if output_path is None:
        output_path = pdf_path

    doc = fitz.open(pdf_path)
    new_doc = fitz.open()

    try:
        # Copy pages before insert position
        for i in range(insert_at):
            if i < doc.page_count:
                new_doc.insert_pdf(doc, from_page=i, to_page=i)

        # Insert blank page
        new_doc.new_page(width=width, height=height, pno=insert_at)

        # Copy remaining pages
        for i in range(insert_at, doc.page_count):
            new_doc.insert_pdf(doc, from_page=i, to_page=i)

        new_doc.save(output_path)
        total_pages = new_doc.page_count
    finally:
        doc.close()
        new_doc.close()

    return total_pages


def protect_pdf_with_password(
    pdf_path: str, output_path: str, user_password: str, owner_password: str = None
) -> None:
    """
    Protect PDF with password.
    user_password: Password required to open the PDF.
    owner_password: Password for full access (if None, uses user_password).
    """
    if not user_password:
        raise ValueError("user_password cannot be empty")

    if owner_password is None:
        owner_password = user_password

    # إذا كان الحفظ على نفس الملف، استخدم ملف مؤقت
    save_to_same = (os.path.abspath(pdf_path) == os.path.abspath(output_path))
    if save_to_same:
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()
        final_output = temp_path
    else:
        final_output = output_path

    doc = fitz.open(pdf_path)
    try:
        # Set encryption - use only available permissions
        perm = int(
            fitz.PDF_PERM_ACCESSIBILITY
            | fitz.PDF_PERM_PRINT
            | fitz.PDF_PERM_MODIFY
            | fitz.PDF_PERM_COPY
            | fitz.PDF_PERM_ANNOTATE
        )
        # Try to add additional permissions if available
        try:
            perm |= fitz.PDF_PERM_ASSEMBLE
        except AttributeError:
            pass
        doc.save(
            final_output,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            user_pw=user_password,
            owner_pw=owner_password,
            permissions=perm,
        )
    finally:
        doc.close()

    # إذا كان الحفظ على نفس الملف، استبدل الملف الأصلي
    if save_to_same:
        import shutil
        try:
            shutil.move(final_output, output_path)
        except Exception as e:
            # في حالة الخطأ، احذف الملف المؤقت
            try:
                os.unlink(final_output)
            except:
                pass
            raise e


def remove_password_protection(
    pdf_path: str, output_path: str, password: str
) -> None:
    """
    Remove password protection from PDF.
    """
    # إذا كان الحفظ على نفس الملف، استخدم ملف مؤقت
    save_to_same = (os.path.abspath(pdf_path) == os.path.abspath(output_path))
    if save_to_same:
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_path = temp_file.name
        temp_file.close()
        final_output = temp_path
    else:
        final_output = output_path

    doc = fitz.open(pdf_path)
    if doc.is_encrypted:
        if not doc.authenticate(password):
            doc.close()
            raise ValueError("كلمة المرور غير صحيحة")
    try:
        doc.save(final_output, incremental=False)
    finally:
        doc.close()

    # إذا كان الحفظ على نفس الملف، استبدل الملف الأصلي
    if save_to_same:
        import shutil
        try:
            shutil.move(final_output, output_path)
        except Exception as e:
            # في حالة الخطأ، احذف الملف المؤقت
            try:
                os.unlink(final_output)
            except:
                pass
            raise e


def update_pdf_metadata(
    pdf_path: str,
    output_path: str,
    title: str = None,
    author: str = None,
    subject: str = None,
    keywords: str = None,
) -> None:
    """
    Update PDF metadata (title, author, subject, keywords).
    """
    doc = fitz.open(pdf_path)
    try:
        metadata = doc.metadata
        if title:
            metadata["title"] = title
        if author:
            metadata["author"] = author
        if subject:
            metadata["subject"] = subject
        if keywords:
            metadata["keywords"] = keywords

        doc.set_metadata(metadata)
        doc.save(output_path)
    finally:
        doc.close()


def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Get PDF metadata. Returns dict with title, author, subject, keywords, etc.
    """
    doc = fitz.open(pdf_path)
    try:
        return doc.metadata
    finally:
        doc.close()


def extract_page_content(page) -> List[Dict[str, Any]]:
    """
    Extract all content from a PDF page (text blocks and images).
    Returns a list of dictionaries with type, bbox, and content.
    """
    elements = []
    
    # استخراج النصوص
    text_dict = page.get_text("dict")
    for block in text_dict.get("blocks", []):
        if "lines" in block:  # text block
            text = ""
            font_info = {"font": "Arial", "size": 12}
            for line in block["lines"]:
                for span in line.get("spans", []):
                    text += span.get("text", "")
                    if "font" in span:
                        font_info["font"] = span.get("font", "Arial")
                    if "size" in span:
                        font_info["size"] = span.get("size", 12)
            if text.strip():
                elements.append({
                    "type": "text",
                    "text": text,
                    "bbox": block.get("bbox", [0, 0, 100, 20]),
                    "font": font_info["font"],
                    "size": font_info["size"],
                })
    
    # استخراج الصور
    image_list = page.get_images()
    for img_index, img in enumerate(image_list):
        xref = img[0]
        try:
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            bbox = page.get_image_bbox(img)
            elements.append({
                "type": "image",
                "xref": xref,
                "bbox": list(bbox),
                "ext": base_image.get("ext", "png"),
                "image_bytes": image_bytes,
            })
        except:
            pass
    
    return elements


def save_edited_content(
    pdf_path: str,
    output_path: str,
    page_index: int,
    elements: List[Dict[str, Any]]
) -> None:
    """
    Save edited page content to a new PDF.
    elements: List of content elements (text, images) with modifications.
    """
    doc = fitz.open(pdf_path)
    try:
        if 0 <= page_index < doc.page_count:
            page = doc.load_page(page_index)
            
            # إضافة العناصر الجديدة والمعدلة
            for elem in elements:
                if elem.get("new", False):  # عنصر جديد
                    if elem["type"] == "text":
                        text = elem.get("text", "")
                        bbox = elem.get("bbox", [50, 50, 200, 70])
                        page.insert_text(
                            (bbox[0], bbox[1]),
                            text,
                            fontsize=elem.get("size", 12),
                            fontname=elem.get("font", "helv"),
                        )
                    elif elem["type"] == "image":
                        # إضافة صورة جديدة
                        if "path" in elem:
                            rect = fitz.Rect(elem.get("bbox", [50, 100, 150, 200]))
                            page.insert_image(rect, filename=elem["path"])
                elif elem.get("deleted", False):  # عنصر محذوف
                    # حذف العنصر (يتطلب معرفة xref للصور)
                    if elem["type"] == "image" and "xref" in elem:
                        try:
                            # حذف الصورة من الصفحة
                            page.delete_image(elem["xref"])
                        except:
                            pass
            
        doc.save(output_path)
    finally:
        doc.close()
