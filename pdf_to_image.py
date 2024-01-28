import pypdfium2 as pdfium
import os
pdf = pdfium.PdfDocument("fin_irjmets1648020477.pdf")
n_pages = len(pdf)

for page_number in range(n_pages):
    page = pdf.get_page(page_number)
    pil_image = page.render(scale = 300/72).to_pil()
    """
    pil_image = page.render(
        scale=1,
        rotation=0,
        crop=(0, 0, 0, 0),
        colour=(255, 255, 255, 255),
        annotations=True,
        greyscale=False
    ).to_pil() """
    image_folder = "pdf_images"
    save_path = os.path.join(image_folder, f"image_{page_number+1}.png")
    pil_image.save(save_path)