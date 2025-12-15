import os
from excel_reader import load_thickness_mapping
from file_sorter import segregate_dxf_files
from dxf_to_png import save_dxf_as_png
from insert_png2excel import insert_png_to_excel



if __name__ == "__main__":

    # input paths
    all_dxfs = "D:\Solidworks\HM mounting\DXFs"
    excel_path = "D:\Solidworks\HM mounting\HM Mounting BOM.xlsx"

    # output paths
    sorted_dxfs = "D:\Solidworks\HM mounting\sorted dxfs"
    all_pngs = "D:\Solidworks\HM mounting\dxfs_pngs"
    thumb_excel_path = "D:\Solidworks\HM mounting\HM Mounting BOM_pngs.xlsx"


    mapping = load_thickness_mapping(excel_path)

    # Process each DXF file
    for file in os.listdir(all_dxfs):
        file_name, _ = os.path.splitext(file)
        if file.endswith(".dxf") and file_name in mapping:

            # Segregate DXF files based on thickness
            segregate_dxf_files(file_name, mapping[file_name], all_dxfs, sorted_dxfs)

            # Convert DXF to PNG for thumbnail

            save_dxf_as_png(
                    dxf_path=os.path.join(all_dxfs, f"{file_name}.dxf"),
                    png_path=os.path.join(all_pngs, f"{file_name}.png"),
                    dpi_=50)
            
            # Insert PNG thumbnail into Excel
            insert_png_to_excel(
                    png_path=os.path.join(all_pngs, f"{file_name}.png"))
            
    print("DXF segregation completed successfully!")