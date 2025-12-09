import os
import shutil
from dxf_to_png import save_dxf_as_png

def segregate_dxf_files(file_name, thk, dxf_folder, output_folder):

    dest_path = os.path.join(output_folder, f"{thk}mm")
    os.makedirs(dest_path, exist_ok=True)

    shutil.copy(
        os.path.join(dxf_folder, f"{file_name}.dxf"),
        os.path.join(dest_path, f"{file_name}.dxf")
    )

