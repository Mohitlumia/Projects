
from PIL import Image
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage


def insert_png_to_excel(png_path, counter):
    # ---------- CONFIG ----------
    img_path = png_path
    target_column = "H"
    target_row = counter

    # Set desired cell dimensions
    cell_width_pixels = 150   # width in pixels
    cell_height_pixels = 100  # height in pixels
    # ----------------------------

    # Convert width/height to Excel units
    # 1 Excel column width ≈ (pixel_width - 5) / 7
    column_width = (cell_width_pixels - 5) / 7
    # 1 Excel row height = pixel_height * 0.75
    row_height = cell_height_pixels * 0.75

    wb = load_workbook("example\DXFs List.xlsx")
    ws = wb.active

    # Apply cell dimensions
    ws.column_dimensions[target_column].width = column_width
    ws.row_dimensions[target_row].height = row_height

    # Load the image with Pillow
    orig_img = Image.open(img_path)
    orig_width, orig_height = orig_img.size

    # Determine scaling factor (preserve aspect ratio)
    scale = min(cell_width_pixels / orig_width, cell_height_pixels / orig_height, 1)

    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)

    # Resize WITHOUT stretching (only shrink if necessary)
    resized_img_path = "resized_temp.png"
    orig_img.resize((new_width, new_height), Image.LANCZOS).save(resized_img_path)

    # Insert into Excel
    xl_img = XLImage(resized_img_path)
    ws.add_image(xl_img, f"{target_column}{target_row}")

    wb.save("example\DXFs List.xlsx")
    print("Saved as result.xlsx")
