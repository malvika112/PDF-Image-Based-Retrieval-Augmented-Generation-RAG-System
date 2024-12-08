import os
import fitz  # PyMuPDF

def pdf_to_images(pdf_path, output_dir):
    """
    Convert each page of a PDF to an image.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Directory to save the images.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    for page_num in range(len(pdf_document)):
        # Select a page
        page = pdf_document[page_num]
        
        # Render the page to an image (pixmap)
        pix = page.get_pixmap()
        
        # Save the image as PNG
        image_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(image_path)
        print(f"Saved: {image_path}")

    # Close the PDF
    pdf_document.close()
    print("PDF to images conversion complete!")


pdf_path = "/Users/malvika/Downloads/Satellogic Investor Presentation_November 2024.pdf"
output_dir = "output_images"
pdf_to_images(pdf_path, output_dir)
