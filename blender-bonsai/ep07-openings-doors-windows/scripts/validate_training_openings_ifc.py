from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.unit


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the Episode 7 opening, door, and window training IFC")
    parser.add_argument("ifc", type=Path, nargs="?", default=PACKAGE_ROOT / "completed" / "bonsai_intro05.ifc")
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def bbox(settings: ifcopenshell.geom.settings, element) -> tuple[float, float, float, float, float, float]:
    shape = ifcopenshell.geom.create_shape(settings, element)
    vertices = shape.geometry.verts
    xs, ys, zs = vertices[0::3], vertices[1::3], vertices[2::3]
    return tuple(round(value, 3) for value in (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)))


def main(path: Path) -> None:
    model = ifcopenshell.open(path)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    slabs = model.by_type("IfcSlab")
    walls = model.by_type("IfcWall")
    openings = model.by_type("IfcOpeningElement")
    doors = model.by_type("IfcDoor")
    windows = model.by_type("IfcWindow")
    void_rels = model.by_type("IfcRelVoidsElement")
    fill_rels = model.by_type("IfcRelFillsElement")

    expected_counts = {
        "IfcSlab": (len(slabs), 1),
        "IfcWall": (len(walls), 4),
        "IfcOpeningElement": (len(openings), 2),
        "IfcDoor": (len(doors), 1),
        "IfcWindow": (len(windows), 1),
        "IfcRelVoidsElement": (len(void_rels), 2),
        "IfcRelFillsElement": (len(fill_rels), 2),
    }
    for label, (actual, expected) in expected_counts.items():
        if actual != expected:
            raise AssertionError(f"{label}: expected {expected}, got {actual}")

    door = doors[0]
    window = windows[0]
    if (float(door.OverallWidth), float(door.OverallHeight)) != (1500.0, 2100.0):
        raise AssertionError("door dimensions are not W1500 x H2100 mm")
    if (float(window.OverallWidth), float(window.OverallHeight)) != (1200.0, 900.0):
        raise AssertionError("window dimensions are not W1200 x H900 mm")

    door_type = ifcopenshell.util.element.get_type(door)
    window_type = ifcopenshell.util.element.get_type(window)
    if not door_type or door_type.OperationType != "DOUBLE_DOOR_SINGLE_SWING":
        raise AssertionError("door type or operation type mismatch")
    if not window_type or window_type.PartitioningType != "SINGLE_PANEL":
        raise AssertionError("window type or partitioning type mismatch")
    for element in (door, window):
        container = ifcopenshell.util.element.get_container(element)
        if not container or container.Name != "1階":
            raise AssertionError(f"{element.Name} is not contained in 1階")

    void_pairs = {
        (rel.RelatingBuildingElement.Name, rel.RelatedOpeningElement.Name)
        for rel in void_rels
    }
    expected_void_pairs = {
        ("外壁 南", "開口 設備搬入用扉 南"),
        ("外壁 北", "開口 設備室窓 北"),
    }
    if void_pairs != expected_void_pairs:
        raise AssertionError(f"void relationships mismatch: {void_pairs}")

    fill_pairs = {
        (rel.RelatingOpeningElement.Name, rel.RelatedBuildingElement.Name)
        for rel in fill_rels
    }
    expected_fill_pairs = {
        ("開口 設備搬入用扉 南", "設備搬入用扉 南"),
        ("開口 設備室窓 北", "設備室窓 北"),
    }
    if fill_pairs != expected_fill_pairs:
        raise AssertionError(f"filling relationships mismatch: {fill_pairs}")

    opening_boxes = {opening.Name: bbox(settings, opening) for opening in openings}
    expected_opening_boxes = {
        "開口 設備搬入用扉 南": (0.75, -0.1, 0.0, 2.25, 0.3, 2.1),
        "開口 設備室窓 北": (2.4, 3.7, 1.2, 3.6, 4.1, 2.1),
    }
    if opening_boxes != expected_opening_boxes:
        raise AssertionError(f"opening bounding boxes mismatch: {opening_boxes}")

    door_box = bbox(settings, door)
    window_box = bbox(settings, window)
    if not (door_box[0] >= 0.70 and door_box[3] <= 2.30 and door_box[2] >= -0.01 and door_box[5] <= 2.13):
        raise AssertionError(f"door geometry is outside the expected opening: {door_box}")
    if not (window_box[0] >= 2.35 and window_box[3] <= 3.65 and window_box[2] >= 1.19 and window_box[5] <= 2.11):
        raise AssertionError(f"window geometry is outside the expected opening: {window_box}")

    result = {
        "valid": True,
        "schema": model.schema,
        "unit_scale_m_per_project_unit": ifcopenshell.util.unit.calculate_unit_scale(model),
        "counts": {key: actual for key, (actual, _) in expected_counts.items()},
        "door": {
            "name": door.Name,
            "type": door_type.Name,
            "operation_type": door_type.OperationType,
            "width_mm": door.OverallWidth,
            "height_mm": door.OverallHeight,
            "bbox_m": door_box,
            "container": ifcopenshell.util.element.get_container(door).Name,
        },
        "window": {
            "name": window.Name,
            "type": window_type.Name,
            "partitioning_type": window_type.PartitioningType,
            "width_mm": window.OverallWidth,
            "height_mm": window.OverallHeight,
            "sill_height_mm": 1200,
            "bbox_m": window_box,
            "container": ifcopenshell.util.element.get_container(window).Name,
        },
        "opening_bounding_boxes_m": opening_boxes,
        "void_relationships": sorted(void_pairs),
        "filling_relationships": sorted(fill_pairs),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = parse_args()
    main(args.ifc)
