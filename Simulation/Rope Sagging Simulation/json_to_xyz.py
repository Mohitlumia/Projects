#!/usr/bin/env python3
"""
json_to_xy_with_z_and_circles.py

Reads a simulation JSON (mm units) and writes:
 - rope coordinates: x<TAB>y<TAB>z (z = 0.0) by default to a text file
 - circle coordinates: x<TAB>y<TAB>z<TAB>radius_mm to a separate text file

Defaults:
  input:  simulation_save_mm.json
  rope output: rope_xyz.txt
  circles output: circles_xyzr.txt

Usage:
  python json_to_xy_with_z_and_circles.py
  python json_to_xy_with_z_and_circles.py -i sim.json -o rope_xyz.txt --circles-out circles.txt --format txt
  python json_to_xy_with_z_and_circles.py -i sim.json -o rope.csv --circles-out circles.csv --format csv

Options:
  --input / -i        Input JSON (default: simulation_save_mm.json)
  --output / -o       Rope output file (default: rope_xyz.txt)
  --circles-out / -c  Circles output file (default: circles_xyzr.txt)
  --rope-index / -r   If JSON contains multiple ropes, which to export (default: 0)
  --format / -f       'txt' (TAB-separated) or 'csv' (comma separated with header). Default: txt
  --z-value / -z      Z value to write (default 0.0 mm)
"""

import argparse
import json
import sys
from pathlib import Path


def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


def _extract_rope_nodes_from_object(r):
    # look for common node keys
    nodes = r.get("nodes_mm") or r.get("nodes") or r.get("nodes_mm")
    if nodes is None:
        return None
    # nodes may be list of [x,y] or list of {x:..,y:..}
    result = []
    for p in nodes:
        if isinstance(p, dict):
            x = float(p.get("x", p.get("0", 0)))
            y = float(p.get("y", p.get("1", 0)))
            result.append((x, y))
        else:
            # assume sequence like [x,y]
            result.append((float(p[0]), float(p[1])))
    return result


def extract_nodes(data, rope_index=0):
    # Accept multiple formats
    if "rope" in data:
        nodes = _extract_rope_nodes_from_object(data["rope"])
        if nodes is None:
            raise ValueError("No 'nodes' or 'nodes_mm' found under 'rope'.")
        return nodes

    if "ropes" in data:
        ropes = data["ropes"]
        if not isinstance(ropes, list) or len(ropes) == 0:
            raise ValueError("'ropes' is empty or not a list.")
        if rope_index < 0 or rope_index >= len(ropes):
            raise IndexError(f"rope_index {rope_index} out of range (0..{len(ropes)-1}).")
        nodes = _extract_rope_nodes_from_object(ropes[rope_index])
        if nodes is None:
            raise ValueError(f"No 'nodes' or 'nodes_mm' found in ropes[{rope_index}].")
        return nodes

    # fallback top-level keys
    if "nodes_mm" in data:
        raw = data["nodes_mm"]
        return [(float(p[0]), float(p[1])) for p in raw]

    if "nodes" in data:
        raw = data["nodes"]
        return [(float(p[0]), float(p[1])) for p in raw]

    raise ValueError("Could not find rope node array in JSON. Expected 'rope', 'ropes', 'nodes' or 'nodes_mm'.")


def extract_circles(data):
    # Accept variety of circle formats
    # try common keys: 'circles' -> list of {pos_mm: [x,y], radius_mm: r} OR {pos: [x,y], radius: r}
    out = []
    candidates = []
    if "circles" in data:
        candidates = data["circles"]
    elif "circle" in data:
        candidates = data["circle"] if isinstance(data["circle"], list) else [data["circle"]]
    else:
        # try to find top-level list of circles if any key looks like circle
        for k, v in data.items():
            if isinstance(v, list) and len(v) and isinstance(v[0], dict):
                # heuristic - skip
                pass

    for c in candidates:
        # pos might be under 'pos_mm', 'pos', 'position', or as dict with x,y
        pos = None
        if isinstance(c, dict):
            pos = c.get("pos_mm") or c.get("pos") or c.get("position") or c.get("center") or c.get("center_mm")
            radius = c.get("radius_mm") or c.get("radius") or c.get("r") or c.get("radius_px")
            # if pos is dict {x:..., y:...}
            if isinstance(pos, dict):
                x = float(pos.get("x", pos.get("X", 0)))
                y = float(pos.get("y", pos.get("Y", 0)))
                pos = [x, y]
        else:
            continue

        if pos is None:
            # try to detect 'x' and 'y' fields in c directly
            if "x" in c and "y" in c:
                pos = [c["x"], c["y"]]

        if pos is None:
            # skip if no pos found
            continue

        try:
            x = float(pos[0])
            y = float(pos[1])
        except Exception:
            continue

        # radius fallback default
        r = float(radius) if radius is not None else 0.0
        out.append((x, y, r))
    return out


def write_rope_xyz(nodes_xy, outpath: Path, fmt="txt", z_value=0.0):
    if fmt == "csv":
        with open(outpath, "w", newline="") as f:
            f.write("x_mm,y_mm,z_mm\n")
            for x, y in nodes_xy:
                f.write(f"{x:.6f},{y:.6f},{z_value:.6f}\n")
    else:
        # tab-separated, no header (SolidWorks-friendly)
        with open(outpath, "w", newline="") as f:
            for x, y in nodes_xy:
                f.write(f"{x:.6f}\t{y:.6f}\t{z_value:.6f}\n")


def write_circles_xyzr(circles, outpath: Path, fmt="txt", z_value=0.0):
    if fmt == "csv":
        with open(outpath, "w", newline="") as f:
            f.write("x_mm,y_mm,z_mm,radius_mm\n")
            for x, y, r in circles:
                f.write(f"{x:.6f},{y:.6f},{z_value:.6f},{r:.6f}\n")
    else:
        with open(outpath, "w", newline="") as f:
            for x, y, r in circles:
                f.write(f"{x:.6f}\t{y:.6f}\t{z_value:.6f}\t{r:.6f}\n")


def main():
    parser = argparse.ArgumentParser(description="Convert rope JSON to X Y Z (mm) text and export circles.")
    parser.add_argument("--input", "-i", default="simulation_save_mm.json", help="Input JSON (default simulation_save_mm.json)")
    parser.add_argument("--output", "-o", default="rope_xyz.txt", help="Rope output file (default rope_xyz.txt)")
    parser.add_argument("--circles-out", "-c", default="circles_xyzr.txt", help="Circles output file (default circles_xyzr.txt)")
    parser.add_argument("--rope-index", "-r", type=int, default=0, help="Index if JSON contains multiple ropes")
    parser.add_argument("--format", "-f", choices=["txt", "csv"], default="txt", help="Output format (txt=TAB, csv=comma)")
    parser.add_argument("--z-value", "-z", type=float, default=0.0, help="Z value to write in mm (default 0.0)")
    args = parser.parse_args()

    infile = Path(args.input)
    if not infile.exists():
        print(f"Input file not found: {infile}", file=sys.stderr)
        sys.exit(2)

    try:
        data = load_json(infile)
    except Exception as e:
        print("Failed to read JSON:", e, file=sys.stderr)
        sys.exit(2)

    try:
        nodes = extract_nodes(data, rope_index=args.rope_index)
    except Exception as e:
        print("Failed to extract rope nodes:", e, file=sys.stderr)
        sys.exit(2)

    circles = extract_circles(data)

    try:
        write_rope_xyz(nodes, Path(args.output), fmt=args.format, z_value=args.z_value)
    except Exception as e:
        print("Failed to write rope output:", e, file=sys.stderr)
        sys.exit(2)

    try:
        write_circles_xyzr(circles, Path(args.circles_out), fmt=args.format, z_value=args.z_value)
    except Exception as e:
        print("Failed to write circles output:", e, file=sys.stderr)
        sys.exit(2)

    print(f"Wrote {len(nodes)} rope nodes to {args.output} ({args.format})")
    print(f"Wrote {len(circles)} circles to {args.circles_out} ({args.format})")


if __name__ == "__main__":
    main()
