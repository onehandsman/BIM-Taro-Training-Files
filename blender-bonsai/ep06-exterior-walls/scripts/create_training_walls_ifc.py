from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.api.attribute
import ifcopenshell.api.context
import ifcopenshell.api.geometry
import ifcopenshell.api.material
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.api.type
import numpy as np


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE_ROOT / "start" / "bonsai_intro03_t200.ifc"


def first_or_none(items):
    return items[0] if items else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add four training walls to the Bonsai IFC floor model")
    parser.add_argument("--thickness-mm", type=float, default=200.0, help="Wall thickness in millimetres")
    parser.add_argument("--height-mm", type=float, default=3000.0, help="Wall height in millimetres")
    parser.add_argument(
        "--output",
        type=Path,
        default=PACKAGE_ROOT / "generated" / "bonsai_intro04.ifc",
        help="Output IFC path",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def main(thickness_mm: float, height_mm: float, output: Path) -> None:
    if thickness_mm <= 0 or height_mm <= 0:
        raise ValueError("wall thickness and height must be greater than zero")

    model = ifcopenshell.open(SOURCE)
    if model.by_type("IfcWall"):
        raise RuntimeError("source model already contains IfcWall elements; refusing to duplicate them")

    model_context = first_or_none(
        [c for c in model.by_type("IfcGeometricRepresentationContext", include_subtypes=False) if c.ContextType == "Model"]
    )
    if model_context is None:
        model_context = ifcopenshell.api.context.add_context(model, context_type="Model")

    body_context = first_or_none(
        [
            c
            for c in model.by_type("IfcGeometricRepresentationSubContext")
            if c.ContextIdentifier == "Body" and c.ContextType == "Model"
        ]
    )
    if body_context is None:
        body_context = ifcopenshell.api.context.add_context(
            model,
            context_type="Model",
            context_identifier="Body",
            target_view="MODEL_VIEW",
            parent=model_context,
        )

    axis_context = first_or_none(
        [
            c
            for c in model.by_type("IfcGeometricRepresentationSubContext")
            if c.ContextIdentifier == "Axis" and c.ContextType == "Model"
        ]
    )
    if axis_context is None:
        axis_context = ifcopenshell.api.context.add_context(
            model,
            context_type="Model",
            context_identifier="Axis",
            target_view="GRAPH_VIEW",
            parent=model_context,
        )

    thickness_label = f"{thickness_mm:g}"
    height_label = f"{height_mm:g}"
    type_name = f"外壁 t{thickness_label}"

    wall_type = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcWallType",
        predefined_type="STANDARD",
        name=type_name,
    )
    concrete = ifcopenshell.api.material.add_material(
        model,
        name="鉄筋コンクリート",
        category="concrete",
        description="研修用の単層外壁材料",
    )
    layer_set = ifcopenshell.api.material.add_material_set(
        model,
        name=type_name,
        set_type="IfcMaterialLayerSet",
    )
    layer = ifcopenshell.api.material.add_layer(
        model,
        layer_set=layer_set,
        material=concrete,
        name=f"鉄筋コンクリート{thickness_label}",
    )
    ifcopenshell.api.material.edit_layer(
        model,
        layer=layer,
        attributes={"LayerThickness": thickness_mm, "Name": f"鉄筋コンクリート{thickness_label}"},
    )
    ifcopenshell.api.material.assign_material(
        model,
        products=[wall_type],
        type="IfcMaterialLayerSet",
        material=layer_set,
    )

    storey = model.by_type("IfcBuildingStorey")[0]
    # Reference lines run clockwise on the 6000 x 4000 mm slab boundary.
    # add_wall_representation extrudes toward local +Y, so this direction keeps
    # every 200 mm wall inside the slab perimeter.
    walls = [
        ("外壁 南", 6.0, (0.0, 0.0), 0.0),
        ("外壁 東", 4.0, (6.0, 0.0), math.pi / 2),
        ("外壁 北", 6.0, (6.0, 4.0), math.pi),
        ("外壁 西", 4.0, (0.0, 4.0), -math.pi / 2),
    ]

    for name, length_m, (x_m, y_m), angle in walls:
        wall = ifcopenshell.api.root.create_entity(
            model,
            ifc_class="IfcWall",
            predefined_type="STANDARD",
            name=name,
        )
        ifcopenshell.api.type.assign_type(model, related_objects=[wall], relating_type=wall_type)
        ifcopenshell.api.material.assign_material(model, products=[wall], type="IfcMaterialLayerSetUsage")
        ifcopenshell.api.spatial.assign_container(model, products=[wall], relating_structure=storey)

        placement = np.eye(4)
        placement[0, 0] = math.cos(angle)
        placement[0, 1] = -math.sin(angle)
        placement[1, 0] = math.sin(angle)
        placement[1, 1] = math.cos(angle)
        placement[0, 3] = x_m
        placement[1, 3] = y_m
        ifcopenshell.api.geometry.edit_object_placement(model, product=wall, matrix=placement, is_si=True)

        axis = ifcopenshell.api.geometry.add_axis_representation(
            model,
            context=axis_context,
            axis=[(0.0, 0.0, 0.0), (length_m, 0.0, 0.0)],
        )
        body = ifcopenshell.api.geometry.add_wall_representation(
            model,
            context=body_context,
            length=length_m,
            height=height_mm / 1000.0,
            thickness=thickness_mm / 1000.0,
        )
        ifcopenshell.api.geometry.assign_representation(model, product=wall, representation=axis)
        ifcopenshell.api.geometry.assign_representation(model, product=wall, representation=body)
        ifcopenshell.api.attribute.edit_attributes(
            model,
            product=wall,
            attributes={
                "Description": (
                    f"設備室の研修用外周壁 長さ{length_m * 1000:g} mm、"
                    f"高さ{height_label} mm、厚さ{thickness_label} mm"
                )
            },
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(output)
    print(f"WROTE {output}")


if __name__ == "__main__":
    args = parse_args()
    main(args.thickness_mm, args.height_mm, args.output)
