# Blender + Bonsai IFC Basics Episode 9: Equipment and System Final Check

This package places an air-handling unit and two 100A chilled-water pipes in equipment room `MR-01`, then assigns both spatial containment and a chilled-water distribution system. The final check covers shape, IFC class, Tag, Container, and System.

- Video: https://youtu.be/DlsK0wesJJk
- Japanese article: https://note.com/real_finch7263/n/ne380d0bf8def

## Files

| Path | Purpose |
|---|---|
| `start/bonsai_intro06.ifc` | Start model with equipment-room space `MR-01` |
| `completed/bonsai_intro07.ifc` | Completed model with AHU, supply/return pipes, and system CHW-01 |
| `generated/bonsai_intro07.ifc` | Script-generated completed model for comparison |
| `scripts/create_training_equipment_ifc.py` | Rebuilds equipment, spatial containment, and distribution system |
| `scripts/validate_training_equipment_ifc.py` | Verifies IFC classes, types, Tags, Containers, and System assignments |
| `SHA256SUMS.txt` | SHA-256 hashes for integrity checks |

## Reproduce the video operation

1. Open `start/bonsai_intro06.ifc` and set `MR-01` Equipment Room as the Active Container.
2. Create an `IfcUnitaryEquipmentType` with predefined type `AIRHANDLER`.
3. Set Name and Tag to `AHU-01`, use a training envelope of 1800 × 800 × 1200 mm, and place it on the floor.
4. Keep the delivery-door route clear and check EquipmentID, Service, and DataStatus.
5. Create a 100A `IfcPipeSegmentType` with predefined type `RIGIDSEGMENT`.
6. Create supply pipe `CHWS-01` at RL 2400 with a 5200 mm length.
7. Create return pipe `CHWR-01` parallel to it.
8. Create `IfcDistributionSystem` `CHW-01` with predefined type `CHILLEDWATER`, then assign all three elements.
9. Verify that all three elements have spatial container `MR-01`.
10. Check shape, class, Tag, Container, and System; save as `bonsai_intro07.ifc` and reopen it.

## Rebuild with the script

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep09-equipment-system-final\scripts\create_training_equipment_ifc.py" --
```

Validate the completed model:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep09-equipment-system-final\scripts\validate_training_equipment_ifc.py" -- ".\blender-bonsai\ep09-equipment-system-final\completed\bonsai_intro07.ifc"
```

## IFC completion criteria

- One IfcUnitaryEquipment: `空調機 AHU-01`, Tag `AHU-01`
- Two IfcPipeSegment: `CHWS-01` and `CHWR-01`, nominal 100 mm
- One IfcDistributionSystem: `CHW-01`, predefined type `CHILLEDWATER`
- Spatial container for all three elements: `MR-01`
- All three elements assigned to system `CHW-01`
- Class, Tag, Container, and System retained after reopening

## Notice

Capacity, dimensions, nominal diameter, placement, and maintenance clearances are simplified assumptions for software training. Real projects require engineering checks for load, flow, pressure loss, supports, access, maintainability, structure, and regulations.

日本語: [README.md](README.md)
