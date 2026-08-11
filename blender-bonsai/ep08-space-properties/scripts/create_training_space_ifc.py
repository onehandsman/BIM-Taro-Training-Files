from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.attribute
import ifcopenshell.api.geometry
import ifcopenshell.api.pset
import ifcopenshell.api.root
import numpy as np


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "bonsai_intro05.ifc"


def first_or_none(items):
    return items[0] if items else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add an IfcSpace with properties and quantities to the training room")
    parser.add_argument("--output", type=Path, default=ROOT / "source" / "bonsai_intro06.ifc")
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def main(output: Path) -> None:
    model = ifcopenshell.open(SOURCE)
    if model.by_type("IfcSpace"):
        raise RuntimeError("source model already contains IfcSpace; refusing to duplicate it")

    body_context = first_or_none(
        [
            context
            for context in model.by_type("IfcGeometricRepresentationSubContext")
            if context.ContextIdentifier == "Body" and context.ContextType == "Model"
        ]
    )
    if body_context is None:
        raise RuntimeError("source IFC has no Model/Body context")

    storey = model.by_type("IfcBuildingStorey")[0]

    # The room is 6000 x 4000 mm outside the walls. Four 200 mm walls leave
    # a clear space of 5600 x 3600 mm. The 3000 mm height is a training value.
    clear_width_mm = 5600.0
    clear_depth_mm = 3600.0
    clear_height_mm = 3000.0
    net_floor_area_m2 = 20.16
    net_volume_m3 = 60.48

    space = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcSpace",
        predefined_type="INTERNAL",
        name="MR-01",
    )
    space.CompositionType = "ELEMENT"
    ifcopenshell.api.attribute.edit_attributes(
        model,
        product=space,
        attributes={
            "LongName": "設備機械室",
            "ObjectType": "機械室",
            "Description": (
                "BIM太郎研修用の内部空間。内法5600×3600、高さ3000 mm。"
                "実案件では法令、保守、搬入、換気、防火、騒音などの条件を確認する。"
            ),
            "ElevationWithFlooring": 0.0,
        },
    )
    # edit_attributes applies generic ObjectType/PredefinedType consistency.
    # IfcSpace explicitly permits a functional ObjectType alongside INTERNAL,
    # so restore the intended standard enumeration after setting ObjectType.
    space.PredefinedType = "INTERNAL"

    # IfcSpace is part of the spatial hierarchy, so it is aggregated beneath
    # the storey. It is not spatially contained like a physical element.
    ifcopenshell.api.aggregate.assign_object(model, products=[space], relating_object=storey)

    placement = np.eye(4)
    placement[0, 3] = 3.0
    placement[1, 3] = 2.0
    ifcopenshell.api.geometry.edit_object_placement(model, product=space, matrix=placement, is_si=True)

    profile_position = model.createIfcAxis2Placement2D(model.createIfcCartesianPoint((0.0, 0.0)))
    profile = model.createIfcRectangleProfileDef(
        "AREA",
        "設備機械室 内法",
        profile_position,
        clear_width_mm,
        clear_depth_mm,
    )
    representation = ifcopenshell.api.geometry.add_profile_representation(
        model,
        context=body_context,
        profile=profile,
        depth=clear_height_mm / 1000.0,
        cardinal_point=None,
    )
    ifcopenshell.api.geometry.assign_representation(model, product=space, representation=representation)

    common = ifcopenshell.api.pset.add_pset(model, product=space, name="Pset_SpaceCommon")
    ifcopenshell.api.pset.edit_pset(
        model,
        pset=common,
        properties={
            "Reference": "MR-01",
            "IsExternal": False,
            "OccupancyType": "設備機械室",
            "GrossPlannedArea": model.createIfcAreaMeasure(net_floor_area_m2),
            "NetPlannedArea": model.createIfcAreaMeasure(net_floor_area_m2),
        },
    )

    quantities = ifcopenshell.api.pset.add_qto(model, product=space, name="Qto_SpaceBaseQuantities")
    ifcopenshell.api.pset.edit_qto(
        model,
        qto=quantities,
        properties={
            "Height": model.createIfcLengthMeasure(clear_height_mm),
            "NetFloorArea": model.createIfcAreaMeasure(net_floor_area_m2),
            "NetVolume": model.createIfcVolumeMeasure(net_volume_m3),
        },
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(output)
    print(f"WROTE {output}")


if __name__ == "__main__":
    args = parse_args()
    main(args.output)
