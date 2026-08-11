from __future__ import annotations

import argparse
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.api.attribute
import ifcopenshell.api.geometry
import ifcopenshell.api.owner
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.api.system
import ifcopenshell.api.type
import ifcopenshell.guid
import numpy as np


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "bonsai_intro06.ifc"


def first_or_none(items):
    return items[0] if items else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add equipment, pipes, and a chilled-water system to the training room")
    parser.add_argument("--output", type=Path, default=ROOT / "source" / "bonsai_intro07.ifc")
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def set_placement(model, product, x_m: float, y_m: float, z_m: float) -> None:
    matrix = np.eye(4)
    matrix[0, 3] = x_m
    matrix[1, 3] = y_m
    matrix[2, 3] = z_m
    ifcopenshell.api.geometry.edit_object_placement(model, product=product, matrix=matrix, is_si=True)


def add_training_pset(model, product, values: dict) -> None:
    pset = ifcopenshell.api.pset.add_pset(model, product=product, name="BIMTaro_TrainingData")
    ifcopenshell.api.pset.edit_pset(model, pset=pset, properties=values)


def main(output: Path) -> None:
    model = ifcopenshell.open(SOURCE)
    if model.by_type("IfcUnitaryEquipment") or model.by_type("IfcPipeSegment"):
        raise RuntimeError("source model already contains training equipment or pipes; refusing to duplicate them")

    body_context = first_or_none(
        [
            context
            for context in model.by_type("IfcGeometricRepresentationSubContext")
            if context.ContextIdentifier == "Body" and context.ContextType == "Model"
        ]
    )
    if body_context is None:
        raise RuntimeError("source IFC has no Model/Body context")
    space = model.by_type("IfcSpace")[0]
    building = model.by_type("IfcBuilding")[0]

    # Training-only dimensions. Actual equipment and pipe sizes must come
    # from the design criteria and manufacturer data.
    ahu_length_mm = 1800.0
    ahu_width_mm = 800.0
    ahu_height_mm = 1200.0
    pipe_length_m = 5.2
    pipe_diameter_mm = 100.0

    equipment_type = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcUnitaryEquipmentType",
        predefined_type="AIRHANDLER",
        name="空調機 1800×800×1200",
    )
    equipment = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcUnitaryEquipment",
        predefined_type="AIRHANDLER",
        name="空調機 AHU-01",
    )
    equipment.Tag = "AHU-01"
    ifcopenshell.api.attribute.edit_attributes(
        model,
        product=equipment,
        attributes={
            "Description": (
                "BIM太郎研修用の空調機。外形1800×800×1200 mm。"
                "実案件の能力、電源、点検空間、接続口はメーカー資料で確認する。"
            )
        },
    )
    ifcopenshell.api.type.assign_type(model, related_objects=[equipment], relating_type=equipment_type)
    ifcopenshell.api.spatial.assign_container(model, products=[equipment], relating_structure=space)
    set_placement(model, equipment, 3.5, 0.8, 0.0)
    equipment_body = ifcopenshell.api.geometry.add_wall_representation(
        model,
        context=body_context,
        length=ahu_length_mm / 1000.0,
        height=ahu_height_mm / 1000.0,
        thickness=ahu_width_mm / 1000.0,
    )
    ifcopenshell.api.geometry.assign_representation(model, product=equipment, representation=equipment_body)
    add_training_pset(
        model,
        equipment,
        {
            "EquipmentID": "AHU-01",
            "Service": "空調",
            "OverallLength": model.createIfcLengthMeasure(ahu_length_mm),
            "OverallWidth": model.createIfcLengthMeasure(ahu_width_mm),
            "OverallHeight": model.createIfcLengthMeasure(ahu_height_mm),
            "DataStatus": "研修用仮設定",
        },
    )

    pipe_type = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcPipeSegmentType",
        predefined_type="RIGIDSEGMENT",
        name="冷水配管 100A",
    )
    circle = model.createIfcCircleProfileDef("AREA", "冷水管100A", None, pipe_diameter_mm / 2.0)
    pipes = []
    for name, tag, y_m, abbreviation, flow in [
        ("冷水往管 CHWS-01", "CHWS-01", 2.75, "CHWS", "往"),
        ("冷水還管 CHWR-01", "CHWR-01", 3.20, "CHWR", "還"),
    ]:
        pipe = ifcopenshell.api.root.create_entity(
            model,
            ifc_class="IfcPipeSegment",
            predefined_type="RIGIDSEGMENT",
            name=name,
        )
        pipe.Tag = tag
        ifcopenshell.api.type.assign_type(model, related_objects=[pipe], relating_type=pipe_type)
        ifcopenshell.api.spatial.assign_container(model, products=[pipe], relating_structure=space)
        set_placement(model, pipe, 0.4, y_m, 2.4)
        pipe_body = ifcopenshell.api.geometry.add_profile_representation(
            model,
            context=body_context,
            profile=circle,
            depth=pipe_length_m,
            cardinal_point=None,
            placement_zx_axes=((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        )
        ifcopenshell.api.geometry.assign_representation(model, product=pipe, representation=pipe_body)
        add_training_pset(
            model,
            pipe,
            {
                "SystemAbbreviation": abbreviation,
                "Service": "冷水",
                "FlowDirection": flow,
                "NominalDiameter": model.createIfcLengthMeasure(pipe_diameter_mm),
                "DataStatus": "研修用仮設定",
            },
        )
        pipes.append(pipe)

    system = ifcopenshell.api.system.add_system(model, ifc_class="IfcDistributionSystem")
    system.Name = "冷水配管系統 CHW-01"
    system.LongName = "機械室 冷水往還系統"
    system.PredefinedType = "CHILLEDWATER"
    system.Description = "空調機と冷水往管・還管をまとめた研修用設備系統"
    ifcopenshell.api.system.assign_system(model, products=[equipment, *pipes], system=system)
    model.create_entity(
        "IfcRelServicesBuildings",
        GlobalId=ifcopenshell.guid.new(),
        OwnerHistory=ifcopenshell.api.owner.create_owner_history(model),
        Name="CHW-01 serves 設備研修棟",
        Description=None,
        RelatingSystem=system,
        RelatedBuildings=[building],
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(output)
    print(f"WROTE {output}")


if __name__ == "__main__":
    args = parse_args()
    main(args.output)
