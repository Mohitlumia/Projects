
from excel_reader import load_thickness_mapping
from file_sorter import segregate_dxf_files


if __name__ == "__main__":
    mapping = load_thickness_mapping("example\DXFs List.xlsx")
    segregate_dxf_files("example\All DXFs", mapping, "example\sorted_output")

    print("DXF segregation completed successfully!")