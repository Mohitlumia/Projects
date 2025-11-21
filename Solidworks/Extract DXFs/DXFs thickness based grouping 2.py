"""
copy_dxf_by_thickness_v2.py

Reads Excel with 'Sheet Metal Thickness' and 'PART NUMBER' columns.
Copies matching DXF files (case-insensitive) into subfolders per thickness.

Adjustments:
 - Treats tab characters in part numbers as spaces.
 - Case-insensitive everything (columns, values, filenames, etc.).
 - Skips blank thickness; logs missing part numbers or DXFs.
"""

import pandas as pd
import shutil
from pathlib import Path
import logging
from datetime import datetime
import re

# ----- CONFIG -----
excel_path = r"D:\Solidworks\Cleat-Web Tensioner\Cleat-Web Tensioner DXFs List.xlsx"
source_dxf_dir = Path(r"D:\DXF Location\DXFs")
dest_root_dir = Path(r"D:\Solidworks\Cleat-Web Tensioner")
log_filename = "sheet_metal_thickness_copy_log.txt"
# -------------------

# Invalid Windows characters for folder names
_INVALID_FOLDER_CHARS = r'<>:"/\\|?*'
_invalid_folder_re = re.compile(r'[<>:"/\\|?*]')

def sanitize_folder_name(name: str) -> str:
    """Clean folder names for Windows."""
    if name is None:
        return "UNKNOWN"
    s = str(name).strip()
    s = _invalid_folder_re.sub("_", s)
    if len(s) == 0:
        return "UNKNOWN"
    return s

def build_dxf_lookup(src_dir: Path):
    """Create case-insensitive lookup dict for DXF filenames."""
    lookup = {}
    duplicates = {}
    if not src_dir.exists():
        raise FileNotFoundError(f"Source DXF directory not found: {src_dir}")
    for p in src_dir.iterdir():
        if p.is_file() and p.suffix.lower() == ".dxf":
            stem_l = p.stem.lower()
            if stem_l in lookup:
                duplicates.setdefault(stem_l, []).append(p)
            lookup[stem_l] = p
    return lookup, duplicates

def find_case_insensitive_column(df, name):
    """Find a column in DataFrame case-insensitively."""
    lower_cols = {c.lower(): c for c in df.columns}
    return lower_cols.get(name.lower())

def main():
    dest_root_dir.mkdir(parents=True, exist_ok=True)
    log_path = dest_root_dir / log_filename

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info("=== DXF copy process started ===")

    # Build lookup of DXF files
    dxf_lookup, duplicates = build_dxf_lookup(source_dxf_dir)
    logging.info(f"Found {len(dxf_lookup)} DXFs in {source_dxf_dir}")

    # Read Excel
    try:
        df = pd.read_excel(excel_path, sheet_name=0, dtype=str)
    except Exception as e:
        logging.exception(f"Failed to read Excel file: {excel_path}")
        return

    # Find correct columns (case-insensitive)
    thickness_col = find_case_insensitive_column(df, "Sheet Metal Thickness")
    part_col = find_case_insensitive_column(df, "PART NUMBER")

    if not thickness_col or not part_col:
        logging.error(
            f"Excel missing required columns. Found: {list(df.columns)}"
        )
        return

    total_rows = len(df)
    copied_count = 0
    missing_dxf = []
    missing_part_numbers = []
    skipped_blank_thickness = 0
    already_existing_skips = 0

    for idx, row in df.iterrows():
        thickness_raw = row.get(thickness_col)
        part_raw = row.get(part_col)

        # normalize and clean values
        thickness = str(thickness_raw).strip().lower() if pd.notna(thickness_raw) else ""
        part = str(part_raw).replace("\t", " ").strip().lower() if pd.notna(part_raw) else ""

        if not thickness:
            skipped_blank_thickness += 1
            continue

        if not part:
            missing_part_numbers.append((idx + 2, thickness))
            continue

        # lookup file
        part_stem = Path(part).stem.lower()
        src_file = dxf_lookup.get(part_stem)

        if not src_file:
            missing_dxf.append((idx + 2, part, thickness))
            continue

        # create thickness folder
        folder_name = sanitize_folder_name(thickness)
        dest_folder = dest_root_dir / folder_name
        dest_folder.mkdir(parents=True, exist_ok=True)

        dest_file = dest_folder / src_file.name

        if dest_file.exists():
            already_existing_skips += 1
            continue

        try:
            shutil.copy2(src_file, dest_file)
            copied_count += 1
        except Exception as e:
            logging.exception(f"Failed to copy '{src_file}' -> '{dest_file}'")

    # --- Summary ---
    logging.info("=== SUMMARY ===")
    logging.info(f"Total rows processed: {total_rows}")
    logging.info(f"Files copied: {copied_count}")
    logging.info(f"Blank thickness skipped: {skipped_blank_thickness}")
    logging.info(f"Already existing skipped: {already_existing_skips}")
    logging.info(f"Missing PART NUMBER entries: {len(missing_part_numbers)}")
    logging.info(f"Missing DXF files: {len(missing_dxf)}")

    if missing_part_numbers:
        logging.info("Missing PART NUMBER rows (row, thickness):")
        for rr in missing_part_numbers:
            logging.info(f"  {rr}")

    if missing_dxf:
        logging.info("Missing DXF entries (row, part, thickness):")
        for rr in missing_dxf:
            logging.info(f"  {rr}")

    logging.info(f"Log saved to: {log_path}")
    logging.info("=== DXF copy process finished ===")

if __name__ == "__main__":
    main()
