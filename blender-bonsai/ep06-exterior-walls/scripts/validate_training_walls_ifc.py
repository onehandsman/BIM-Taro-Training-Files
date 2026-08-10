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
    parser = argparse.ArgumentParser(description="Validate the Episode 6 wall training IFC")
    parser.add_argument(
        "ifc",
        type=Path,
        nargs="?",
        default=PACKAGE_ROOT / "completed" / "bonsai_intro04.ifc",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def main(path: Path) -> None:
    model = ifcopenshell.open(path)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    checks: list[dict] = []
    expected = {
        "外壁 南": (0.0, 0.0, 0.0, 6.0, 0.2, 3.0),
        "外壁 東": (5.8, 0.0, 0.0, 6.0, 4.0, 3.0),
        "外壁 北": (0.0, 3.8, 0.0, 6.0, 4.0, 3.0),
        "外壁 西": (0.0, 0.0, 0.0, 0.2, 4.0, 3.0),
    }
    walls = model.by_type("IfcWall")
    if len(walls) != 4:
        raise AssertionError(f"expected 4 IfcWall elements, got {len(walls)}")
    if len(model.by_type("IfcSlab")) != 1:
        raise AssertionError("expected exactly 1 IfcSlab")

    for wall in walls:
        shape = ifcopenshell.geom.create_shape(settings, wall)
        vertices = shape.geometry.verts
        xs, ys, zs = vertices[0::3], vertices[1::3], vertices[2::3]
        bbox = tuple(round(value, 3) for value in (min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)))
        container = ifcopenshell.util.element.get_container(wall)
        wall_type = ifcopenshell.util.element.get_type(wall)
        if wall.Name not in expected:
            raise AssertionError(f"unexpected wall name: {wall.Name}")
        if bbox != expected[wall.Name]:
            raise AssertionError(f"{wall.Name} bbox {bbox} != {expected[wall.Name]}")
        if not container or container.Name != "1階":
            raise AssertionError(f"{wall.Name} is not contained in 1階")
        if not wall_type or wall_type.Name != "外壁 t200":
            raise AssertionError(f"{wall.Name} type mismatch")
        checks.append(
            {
                "name": wall.Name,
                "type": wall_type.Name,
                "container": container.Name,
                "bbox_m": bbox,
            }
        )

    layer_thicknesses = sorted(
        float(layer.LayerThickness) for layer in model.by_type("IfcMaterialLayer") if layer.LayerThickness is not None
    )
    if 200.0 not in layer_thicknesses:
        raise AssertionError(f"200 mm wall material layer missing: {layer_thicknesses}")

    result = {
        "valid": True,
        "schema": model.schema,
        "unit_scale_m_per_project_unit": ifcopenshell.util.unit.calculate_unit_scale(model),
        "slab_count": len(model.by_type("IfcSlab")),
        "wall_count": len(walls),
        "wall_type": "外壁 t200",
        "wall_thickness_mm": 200,
        "wall_height_mm": 3000,
        "spatial_container": "1階",
        "walls": checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = parse_args()
    main(args.ifc)
