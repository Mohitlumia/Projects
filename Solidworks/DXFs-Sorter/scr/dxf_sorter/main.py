import os
from excel_reader import load_thickness_mapping
from file_sorter import segregate_dxf_files
from dxf_to_png import save_dxf_as_png
from insert_png2excel import insert_png_to_excel



if __name__ == "__main__":

    # input paths
    all_dxfs = "D:\DXF Location\DXFs"
    excel_path = "D:\Solidworks\Bunker\Bunker BOM\Bunker BOM r2.xlsx"

    # output paths
    sorted_dxfs = "D:\Solidworks\Bunker\Bunker BOM\Bunker_DXFs"
    all_pngs = "D:\Solidworks\Bunker\Bunker BOM\Bunker_DXFs_PNGs"
    thumb_excel_path = "example\DXFs_List_Thumb.xlsx"


    mapping = load_thickness_mapping(excel_path)
    counter_ = 0
    # Process each DXF file
    for file in os.listdir(all_dxfs):
        counter_ += 1
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
            """insert_png_to_excel(
                    png_path=os.path.join(all_pngs, f"{file_name}.png"),
                    counter=counter_)  # +1 to account for header row"""
            
    print("DXF segregation completed successfully!")