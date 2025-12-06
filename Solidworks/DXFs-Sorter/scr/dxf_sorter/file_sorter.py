import os
import shutil

def segregate_dxf_files(dxf_folder, mapping, output_folder="output"):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(dxf_folder):

        file_name, _ = os.path.splitext(file)
        if file.endswith(".dxf") and file_name in mapping:
            thk = str(mapping[file_name])
            dest_path = os.path.join(output_folder, f"{thk}mm")
            os.makedirs(dest_path, exist_ok=True)

            shutil.copy(
                os.path.join(dxf_folder, file),
                os.path.join(dest_path, file)
            )
