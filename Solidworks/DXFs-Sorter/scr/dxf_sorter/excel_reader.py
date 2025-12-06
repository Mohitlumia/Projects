import pandas

def load_thickness_mapping(excel_path, part_number_col = "PART NUMBER", thickness_col = "Sheet Metal Thickness"):
    df = pandas.read_excel(excel_path)

    # columns: "Sheet Metal Thickness" and "PART NUMBER"
    mapping = dict(zip(df[part_number_col], df[thickness_col]))

    return mapping