from pypdf import PdfReader, PdfWriter

input_path = r"C:\Users\Dell\Downloads\لغتي سادس مادتي 1447.pdf"
output_path = r"C:\Users\Dell\Downloads\لغتي سادس  1447.pdf"

reader = PdfReader(input_path)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open(output_path, "wb") as f:
    writer.write(f)

print("تم بنجاح")
