from __future__ import annotations

import argparse
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


EPISODE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = EPISODE_DIR / "start" / "bonsai_intro02.ifc"
DEFAULT_OUTPUT = EPISODE_DIR / "generated" / "bonsai_intro03_t200.ifc"


def first_or_none(items):
    return items[0] if items else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the BIM Taro training IfcSlab model from the Episode 5 start file."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Source IFC path (default: episode start/bonsai_intro02.ifc)",
    )
    parser.add_argument(
        "--thickness-mm",
        type=float,
        default=200.0,
        help="Slab thickness in millimetres (default: 200)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output IFC path (default: episode generated/bonsai_intro03_t200.ifc)",
    )
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def main(source: Path, thickness_mm: float, output: Path) -> None:
    if thickness_mm <= 0:
        raise ValueError("--thickness-mm must be greater than zero")
    if not source.is_file():
        raise FileNotFoundError(f"Source IFC not found: {source}")

    model = ifcopenshell.open(source)
    if model.schema != "IFC4":
        raise RuntimeError(f"Expected IFC4 source model, received {model.schema}")

    thickness_label = f"{thickness_mm:g}"
    type_name = f"設備室床 t{thickness_label}"
    layer_name = f"コンクリート{thickness_label}"

    if model.by_type("IfcSlab"):
        raise RuntimeError("The source IFC already contains an IfcSlab; refusing to duplicate it")

    model_context = first_or_none(
        [
            context
            for context in model.by_type("IfcGeometricRepresentationContext", include_subtypes=False)
            if context.ContextType == "Model"
        ]
    )
    if model_context is None:
        model_context = ifcopenshell.api.context.add_context(model, context_type="Model")

    body_context = first_or_none(
        [
            context
            for context in model.by_type("IfcGeometricRepresentationSubContext")
            if context.ContextIdentifier == "Body" and context.ContextType == "Model"
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

    slab_type = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcSlabType",
        predefined_type="FLOOR",
        name=type_name,
    )
    concrete = ifcopenshell.api.material.add_material(
        model,
        name="コンクリート",
        category="concrete",
        description="研修用の単層床スラブ材料",
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
        name=layer_name,
    )
    ifcopenshell.api.material.edit_layer(
        model,
        layer=layer,
        attributes={"LayerThickness": thickness_mm, "Name": layer_name},
    )
    ifcopenshell.api.material.assign_material(
        model,
        products=[slab_type],
        type="IfcMaterialLayerSet",
        material=layer_set,
    )

    slab = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcSlab",
        predefined_type="FLOOR",
        name="設備室床",
    )
    ifcopenshell.api.type.assign_type(model, related_objects=[slab], relating_type=slab_type)

    storeys = model.by_type("IfcBuildingStorey")
    if len(storeys) != 1:
        raise RuntimeError(f"Expected exactly one IfcBuildingStorey, received {len(storeys)}")
    ifcopenshell.api.spatial.assign_container(model, products=[slab], relating_structure=storeys[0])

    placement = np.eye(4)
    ifcopenshell.api.geometry.edit_object_placement(model, product=slab, matrix=placement, is_si=True)
    representation = ifcopenshell.api.geometry.add_slab_representation(
        model,
        context=body_context,
        depth=thickness_mm / 1000.0,
        polyline=[(0.0, 0.0), (6.0, 0.0), (6.0, 4.0), (0.0, 4.0), (0.0, 0.0)],
    )
    ifcopenshell.api.geometry.assign_representation(model, product=slab, representation=representation)

    ifcopenshell.api.attribute.edit_attributes(
        model,
        product=slab,
        attributes={"Description": f"設備室の研修用床スラブ 6000×4000×{thickness_label} mm"},
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(output)
    print(f"WROTE {output}")


if __name__ == "__main__":
    arguments = parse_args()
    main(arguments.source, arguments.thickness_mm, arguments.output)
