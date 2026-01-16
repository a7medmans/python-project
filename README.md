# PDFPageRemover 🗂️✂️

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-latest-green.svg)](https://pymupdf.readthedocs.io/)

## Overview
**PDFPageRemover** is a powerful Python CLI tool for PDF manipulation. Core: remove specific pages. Plus compression, PDF↔Images conversion, and security features. Ideal for educators preparing materials or developers automating workflows.[web:17][web:23]

## ✨ Features
- **Page Removal**: Delete by page numbers/ranges (e.g., 1,3-5)
- **Compression**: Shrink file size with garbage collection
- **PDF → Images**: Export to PNG/JPG (custom DPI/quality)
- **Images → PDF**: Merge images into PDF
- **Security**: Add/remove passwords

## 🛠️ Tech Stack
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) [web:17][web:20]
- [Pillow](https://pillow.readthedocs.io/)
- Python 3.8+

## 🚀 Quick Start
```bash
git clone https://github.com/[yourusername]/PDFPageRemover.git
cd PDFPageRemover
pip install -r requirements.txt
python PDFPageRemover.py --help
