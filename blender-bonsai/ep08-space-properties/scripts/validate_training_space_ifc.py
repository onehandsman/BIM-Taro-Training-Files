from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.unit


ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the Episode 8 IfcSpace training model")
    parser.add_argument("ifc", type=Path, nargs="?", default=ROOT / "source" / "bonsai_intro06.ifc")
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

    spaces = model.by_type("IfcSpace")
    if len(spaces) != 1:
        raise AssertionError(f"IfcSpace: expected 1, got {len(spaces)}")
    space = spaces[0]

    expected_attributes = {
        "Name": "MR-01",
        "LongName": "設備機械室",
        "ObjectType": "機械室",
        "PredefinedType": "INTERNAL",
        "CompositionType": "ELEMENT",
    }
    for attribute, expected in expected_attributes.items():
        actual = getattr(space, attribute)
        if actual != expected:
            raise AssertionError(f"{attribute}: expected {expected!r}, got {actual!r}")

    decomposes = [rel for rel in space.Decomposes if rel.is_a("IfcRelAggregates")]
    if len(decomposes) != 1 or decomposes[0].RelatingObject.Name != "1階":
        raise AssertionError("IfcSpace is not aggregated beneath the 1階 storey")

    actual_box = bbox(settings, space)
    expected_box = (0.2, 0.2, 0.0, 5.8, 3.8, 3.0)
    if actual_box != expected_box:
        raise AssertionError(f"space bounding box mismatch: expected {expected_box}, got {actual_box}")

    psets = ifcopenshell.util.element.get_psets(space, psets_only=True)
    qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
    common = psets.get("Pset_SpaceCommon", {})
    quantities = qtos.get("Qto_SpaceBaseQuantities", {})
    expected_common = {
        "Reference": "MR-01",
        "IsExternal": False,
        "OccupancyType": "設備機械室",
        "GrossPlannedArea": 20.16,
        "NetPlannedArea": 20.16,
    }
    for key, expected in expected_common.items():
        if common.get(key) != expected:
            raise AssertionError(f"Pset_SpaceCommon.{key}: expected {expected!r}, got {common.get(key)!r}")
    expected_quantities = {"Height": 3000.0, "NetFloorArea": 20.16, "NetVolume": 60.48}
    for key, expected in expected_quantities.items():
        if quantities.get(key) != expected:
            raise AssertionError(f"Qto_SpaceBaseQuantities.{key}: expected {expected!r}, got {quantities.get(key)!r}")

    result = {
        "valid": True,
        "schema": model.schema,
        "unit_scale_m_per_project_length_unit": ifcopenshell.util.unit.calculate_unit_scale(model),
        "space": {
            "name": space.Name,
            "long_name": space.LongName,
            "predefined_type": space.PredefinedType,
            "composition_type": space.CompositionType,
            "parent_storey": decomposes[0].RelatingObject.Name,
            "bbox_m": actual_box,
            "properties": expected_common,
            "quantities": expected_quantities,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = parse_args()
    main(args.ifc)
