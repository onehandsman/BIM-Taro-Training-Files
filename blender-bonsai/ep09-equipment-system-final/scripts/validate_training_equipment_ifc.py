from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.system
import ifcopenshell.util.unit


ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the Episode 9 equipment-room training IFC")
    parser.add_argument("ifc", type=Path, nargs="?", default=ROOT / "source" / "bonsai_intro07.ifc")
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

    equipment = model.by_type("IfcUnitaryEquipment")
    pipes = model.by_type("IfcPipeSegment")
    systems = model.by_type("IfcDistributionSystem")
    if len(equipment) != 1:
        raise AssertionError(f"IfcUnitaryEquipment: expected 1, got {len(equipment)}")
    if len(pipes) != 2:
        raise AssertionError(f"IfcPipeSegment: expected 2, got {len(pipes)}")
    if len(systems) != 1:
        raise AssertionError(f"IfcDistributionSystem: expected 1, got {len(systems)}")

    ahu = equipment[0]
    if ahu.Name != "空調機 AHU-01" or ahu.Tag != "AHU-01":
        raise AssertionError("AHU identity mismatch")
    ahu_type = ifcopenshell.util.element.get_type(ahu)
    if (
        not ahu_type
        or ahu_type.Name != "空調機 1800×800×1200"
        or ahu_type.PredefinedType != "AIRHANDLER"
    ):
        raise AssertionError("AHU type mismatch")
    ahu_box = bbox(settings, ahu)
    expected_ahu_box = (3.5, 0.8, 0.0, 5.3, 1.6, 1.2)
    if ahu_box != expected_ahu_box:
        raise AssertionError(f"AHU bounding box mismatch: expected {expected_ahu_box}, got {ahu_box}")

    expected_pipe_boxes = {
        "冷水往管 CHWS-01": (0.4, 2.7, 2.35, 5.6, 2.8, 2.45),
        "冷水還管 CHWR-01": (0.4, 3.15, 2.35, 5.6, 3.25, 2.45),
    }
    pipe_boxes = {pipe.Name: bbox(settings, pipe) for pipe in pipes}
    if pipe_boxes != expected_pipe_boxes:
        raise AssertionError(f"pipe bounding boxes mismatch: {pipe_boxes}")
    for pipe in pipes:
        pipe_type = ifcopenshell.util.element.get_type(pipe)
        if not pipe_type or pipe_type.PredefinedType != "RIGIDSEGMENT":
            raise AssertionError(f"{pipe.Name} type or predefined type mismatch")

    for element in [ahu, *pipes]:
        container = ifcopenshell.util.element.get_container(element)
        if not container or container.Name != "MR-01":
            raise AssertionError(f"{element.Name} is not contained in MR-01")

    system = systems[0]
    if system.Name != "冷水配管系統 CHW-01" or system.PredefinedType != "CHILLEDWATER":
        raise AssertionError("distribution system identity or predefined type mismatch")
    assigned = {element.Name for element in ifcopenshell.util.system.get_system_elements(system)}
    expected_assigned = {"空調機 AHU-01", "冷水往管 CHWS-01", "冷水還管 CHWR-01"}
    if assigned != expected_assigned:
        raise AssertionError(f"system membership mismatch: {assigned}")
    service_rels = model.by_type("IfcRelServicesBuildings")
    if len(service_rels) != 1 or service_rels[0].RelatingSystem != system:
        raise AssertionError("CHW-01 is not related to the training building")

    ahu_pset = ifcopenshell.util.element.get_psets(ahu, psets_only=True).get("BIMTaro_TrainingData", {})
    if ahu_pset.get("EquipmentID") != "AHU-01" or ahu_pset.get("DataStatus") != "研修用仮設定":
        raise AssertionError("AHU training property set mismatch")
    pipe_data = {
        pipe.Name: ifcopenshell.util.element.get_psets(pipe, psets_only=True).get("BIMTaro_TrainingData", {})
        for pipe in pipes
    }
    for name, abbreviation in (("冷水往管 CHWS-01", "CHWS"), ("冷水還管 CHWR-01", "CHWR")):
        if pipe_data[name].get("SystemAbbreviation") != abbreviation:
            raise AssertionError(f"{name} system abbreviation mismatch")
        if pipe_data[name].get("NominalDiameter") != 100.0:
            raise AssertionError(f"{name} nominal diameter mismatch")

    result = {
        "valid": True,
        "schema": model.schema,
        "unit_scale_m_per_project_length_unit": ifcopenshell.util.unit.calculate_unit_scale(model),
        "counts": {
            "IfcSpace": len(model.by_type("IfcSpace")),
            "IfcUnitaryEquipment": len(equipment),
            "IfcPipeSegment": len(pipes),
            "IfcDistributionSystem": len(systems),
        },
        "equipment": {"name": ahu.Name, "tag": ahu.Tag, "type": ahu_type.Name, "bbox_m": ahu_box},
        "pipes": pipe_boxes,
        "spatial_container": "MR-01",
        "system": {
            "name": system.Name,
            "predefined_type": system.PredefinedType,
            "members": sorted(assigned),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = parse_args()
    main(args.ifc)
