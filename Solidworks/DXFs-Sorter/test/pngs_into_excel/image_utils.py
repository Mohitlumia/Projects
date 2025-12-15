from openpyxl.drawing.image import Image

def scale_image_proportionally(img: Image, max_width=100, max_height=100):
    """
    Scales an openpyxl Image object proportionally so that
    it fits within max_width x max_height bounding box.
    """
    original_width = img.width
    original_height = img.height

    width_ratio = max_width / original_width
    height_ratio = max_height / original_height

    # Choose the smallest ratio to keep aspect ratio
    scale_ratio = min(width_ratio, height_ratio)

    # Apply scaling
    img.width = int(original_width * scale_ratio)
    img.height = int(original_height * scale_ratio)

    return img  # return back in case needed



# Additional utility: center image in cell
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

def center_image_in_cell(ws, img: Image, col: int, row: int):
    """
    Roughly center `img` in the cell at (row, col) by
    resizing the cell to the image size and anchoring to that cell.
    """
    # 1. Figure out column letter
    col_letter = get_column_letter(col)

    # 2. Approximate conversions between Excel units and pixels
    # These factors are commonly used approximations
    def px_to_col_width(px):
        # 1 Excel column width ≈ 7 pixels (default font)
        return px / 7.0

    def px_to_row_height(px):
        # 1 point ≈ 0.75 pixel -> height(points) ≈ px * 0.75
        return px * 0.75

    # 3. Resize column & row to image size
    ws.column_dimensions[col_letter].width = px_to_col_width(img.width)
    ws.row_dimensions[row].height = px_to_row_height(img.height)

    # 4. Anchor image to that cell
    cell_address = f"{col_letter}{row}"
    img.anchor = cell_address
    ws.add_image(img)

