from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.api.attribute
import ifcopenshell.api.feature
import ifcopenshell.api.geometry
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.api.type
import numpy as np


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE_ROOT / "start" / "bonsai_intro04.ifc"


def first_or_none(items):
    return items[0] if items else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add a door, a window, and semantic openings to the training room IFC")
    parser.add_argument("--output", type=Path, default=PACKAGE_ROOT / "generated" / "bonsai_intro05.ifc")
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else None
    return parser.parse_args(argv)


def placement(angle: float, x: float, y: float, z: float) -> np.ndarray:
    matrix = np.eye(4)
    matrix[0, 0] = math.cos(angle)
    matrix[0, 1] = -math.sin(angle)
    matrix[1, 0] = math.sin(angle)
    matrix[1, 1] = math.cos(angle)
    matrix[0, 3] = x
    matrix[1, 3] = y
    matrix[2, 3] = z
    return matrix


def main(output: Path) -> None:
    model = ifcopenshell.open(SOURCE)
    if model.by_type("IfcDoor") or model.by_type("IfcWindow") or model.by_type("IfcOpeningElement"):
        raise RuntimeError("source model already contains a door, window, or opening; refusing to duplicate them")

    model_context = first_or_none(
        [c for c in model.by_type("IfcGeometricRepresentationContext", include_subtypes=False) if c.ContextType == "Model"]
    )
    if model_context is None:
        raise RuntimeError("source IFC has no Model context")
    body_context = first_or_none(
        [
            c
            for c in model.by_type("IfcGeometricRepresentationSubContext")
            if c.ContextIdentifier == "Body" and c.ContextType == "Model"
        ]
    )
    if body_context is None:
        raise RuntimeError("source IFC has no Model/Body context")

    walls = {wall.Name: wall for wall in model.by_type("IfcWall")}
    south_wall = walls.get("外壁 南")
    north_wall = walls.get("外壁 北")
    if south_wall is None or north_wall is None:
        raise RuntimeError("外壁 南 / 外壁 北 not found in source model")
    storey = model.by_type("IfcBuildingStorey")[0]

    # Training dimensions. Actual projects must confirm equipment access,
    # fire protection, acoustics, ventilation, and structural requirements.
    door_width_mm = 1500.0
    door_height_mm = 2100.0
    door_offset_m = 0.75
    window_width_mm = 1200.0
    window_height_mm = 900.0
    window_sill_mm = 1200.0
    window_offset_m = 2.4

    door_type = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcDoorType",
        predefined_type="DOOR",
        name="設備搬入用扉 W1500×H2100",
    )
    door_type.OperationType = "DOUBLE_DOOR_SINGLE_SWING"
    door_type.ParameterTakesPrecedence = True

    door = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcDoor",
        predefined_type="DOOR",
        name="設備搬入用扉 南",
    )
    ifcopenshell.api.attribute.edit_attributes(
        model,
        product=door,
        attributes={
            "OverallWidth": door_width_mm,
            "OverallHeight": door_height_mm,
            "Description": (
                "研修用の両開き搬入用扉 W1500×H2100 mm。"
                "実案件では搬入物、防火、避難、遮音等を確認する。"
            ),
        },
    )
    ifcopenshell.api.type.assign_type(model, related_objects=[door], relating_type=door_type)
    ifcopenshell.api.spatial.assign_container(model, products=[door], relating_structure=storey)
    door_matrix = placement(0.0, door_offset_m, 0.075, 0.0)
    ifcopenshell.api.geometry.edit_object_placement(model, product=door, matrix=door_matrix, is_si=True)
    door_representation = ifcopenshell.api.geometry.add_door_representation(
        model,
        context=body_context,
        overall_width=door_width_mm,
        overall_height=door_height_mm,
        operation_type="DOUBLE_DOOR_SINGLE_SWING",
        lining_properties={"LiningDepth": 200.0, "LiningOffset": 0.0},
    )
    ifcopenshell.api.geometry.assign_representation(model, product=door, representation=door_representation)

    door_opening = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcOpeningElement",
        predefined_type="OPENING",
        name="開口 設備搬入用扉 南",
    )
    door_opening_matrix = placement(0.0, door_offset_m, -0.1, 0.0)
    ifcopenshell.api.geometry.edit_object_placement(model, product=door_opening, matrix=door_opening_matrix, is_si=True)
    door_opening_representation = ifcopenshell.api.geometry.add_wall_representation(
        model,
        context=body_context,
        length=door_width_mm / 1000.0,
        height=door_height_mm / 1000.0,
        thickness=0.4,
    )
    ifcopenshell.api.geometry.assign_representation(
        model, product=door_opening, representation=door_opening_representation
    )
    ifcopenshell.api.feature.add_feature(model, feature=door_opening, element=south_wall)
    ifcopenshell.api.feature.add_filling(model, opening=door_opening, element=door)

    window_type = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcWindowType",
        predefined_type="WINDOW",
        name="設備室窓 W1200×H900",
    )
    window_type.PartitioningType = "SINGLE_PANEL"
    window_type.ParameterTakesPrecedence = True

    window = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcWindow",
        predefined_type="WINDOW",
        name="設備室窓 北",
    )
    ifcopenshell.api.attribute.edit_attributes(
        model,
        product=window,
        attributes={
            "OverallWidth": window_width_mm,
            "OverallHeight": window_height_mm,
            "Description": (
                "研修用の単窓 W1200×H900 mm、腰高1200 mm。"
                "実案件では防火、換気、遮音、結露、外壁条件等を確認する。"
            ),
        },
    )
    ifcopenshell.api.type.assign_type(model, related_objects=[window], relating_type=window_type)
    ifcopenshell.api.spatial.assign_container(model, products=[window], relating_structure=storey)
    # North wall local +X points west and local +Y points into the room.
    window_matrix = placement(math.pi, 3.6, 3.925, window_sill_mm / 1000.0)
    ifcopenshell.api.geometry.edit_object_placement(model, product=window, matrix=window_matrix, is_si=True)
    window_representation = ifcopenshell.api.geometry.add_window_representation(
        model,
        context=body_context,
        overall_width=window_width_mm,
        overall_height=window_height_mm,
        partition_type="SINGLE_PANEL",
        lining_properties={"LiningDepth": 200.0, "LiningOffset": 0.0},
    )
    ifcopenshell.api.geometry.assign_representation(model, product=window, representation=window_representation)

    window_opening = ifcopenshell.api.root.create_entity(
        model,
        ifc_class="IfcOpeningElement",
        predefined_type="OPENING",
        name="開口 設備室窓 北",
    )
    window_opening_matrix = placement(math.pi, 3.6, 4.1, window_sill_mm / 1000.0)
    ifcopenshell.api.geometry.edit_object_placement(model, product=window_opening, matrix=window_opening_matrix, is_si=True)
    window_opening_representation = ifcopenshell.api.geometry.add_wall_representation(
        model,
        context=body_context,
        length=window_width_mm / 1000.0,
        height=window_height_mm / 1000.0,
        thickness=0.4,
    )
    ifcopenshell.api.geometry.assign_representation(
        model, product=window_opening, representation=window_opening_representation
    )
    ifcopenshell.api.feature.add_feature(model, feature=window_opening, element=north_wall)
    ifcopenshell.api.feature.add_filling(model, opening=window_opening, element=window)

    output.parent.mkdir(parents=True, exist_ok=True)
    model.write(output)
    print(f"WROTE {output}")


if __name__ == "__main__":
    args = parse_args()
    main(args.output)
