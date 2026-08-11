# Blender + Bonsai IFC Basics Episode 7: Openings, Doors, and Windows

This package starts with one floor slab and four exterior walls, then adds a double-leaf equipment access door and a window. It is designed for beginners to reproduce the lesson and compare the IFC relationships between the wall, opening, and filling elements with a validated completed model.

- Video: to be added after publication
- Japanese article: to be added after publication

## Files

| Path | Purpose |
|---|---|
| `start/bonsai_intro04.ifc` | Start model with one slab and four exterior walls |
| `completed/bonsai_intro05.ifc` | Completed model with two openings, one door, and one window |
| `scripts/create_training_openings_ifc.py` | Rebuilds the openings, door, and window from the start model |
| `scripts/validate_training_openings_ifc.py` | Verifies IFC classes, types, dimensions, opening relationships, and spatial containers |
| `SHA256SUMS.txt` | SHA-256 hashes for integrity checks |

## Reproduce the video operation

1. In Bonsai, use `Open IFC Project` to open `start/bonsai_intro04.ifc`.
2. In Object Mode, activate Door Tool and prepare an `設備搬入用扉 W1500×H2100` IfcDoorType.
3. Set Overall Width to 1500 mm, Overall Height to 2100 mm, operation type to `DOUBLE_DOOR_SINGLE_SWING`, and Predefined Type to `DOOR`.
4. Snap to the south wall and place the door 750 mm from its west end at RL1 = 0 mm.
5. Activate Window Tool and prepare an `設備室窓 W1200×H900` IfcWindowType.
6. Set Overall Width to 1200 mm, Overall Height to 900 mm, partitioning type to `SINGLE_PANEL`, Predefined Type to `WINDOW`, and RL2 to 1200 mm.
7. Snap the window to the north wall and place it.
8. Verify two IfcOpeningElement, two IfcRelVoidsElement, and two IfcRelFillsElement entities.
9. Verify that both the door and window are contained in `1階` (Level 1).
10. Use `Save IFC Project As…` to save `bonsai_intro05.ifc`, then compare it with the completed model.

## Rebuild with the script

Open PowerShell at the repository root and run:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep07-openings-doors-windows\scripts\create_training_openings_ifc.py" --
```

To validate the completed model:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep07-openings-doors-windows\scripts\validate_training_openings_ifc.py" -- ".\blender-bonsai\ep07-openings-doors-windows\completed\bonsai_intro05.ifc"
```

Adjust the Blender executable path if your installation is elsewhere.

## IFC completion criteria

- IFC4 with millimetre-based input
- One IfcSlab and four IfcWall entities
- Two IfcOpeningElement, one IfcDoor, and one IfcWindow entities
- Two IfcRelVoidsElement and two IfcRelFillsElement relationships
- Door: W1500 × H2100 mm, DOUBLE_DOOR_SINGLE_SWING
- Window: W1200 × H900 mm, 1200 mm sill height, SINGLE_PANEL
- Door and window spatial container: `1階` (Level 1)

## Dimension notice

These dimensions are simplified assumptions for software training. For a real project, verify equipment delivery and replacement routes, clear opening size, fire safety, acoustics, ventilation, condensation, structure, regulations, and other project requirements. The generated frame and lining geometry may extend slightly beyond the nominal door or window dimensions.

日本語: [README.md](README.md)
