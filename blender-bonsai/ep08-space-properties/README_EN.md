# Blender + Bonsai IFC Basics Episode 8: Space and Properties

This package adds an `IfcSpace` to the equipment room created in the previous lessons. It gives the room an identifier, purpose, planned area, and volume so beginners can reproduce the lesson and compare their IFC with a validated completed model.

- Video: https://youtu.be/rGZRIptOo3c
- Japanese article: https://note.com/real_finch7263/n/n560758df124e

## Files

| Path | Purpose |
|---|---|
| `start/bonsai_intro05.ifc` | Start model with slab, walls, openings, door, and window |
| `completed/bonsai_intro06.ifc` | Completed model with equipment-room space `MR-01` |
| `generated/bonsai_intro06.ifc` | Script-generated completed model for comparison |
| `scripts/create_training_space_ifc.py` | Rebuilds the space, properties, and quantities |
| `scripts/validate_training_space_ifc.py` | Verifies the space class, dimensions, properties, quantities, and hierarchy |
| `SHA256SUMS.txt` | SHA-256 hashes for integrity checks |

## Reproduce the video operation

1. Open `start/bonsai_intro05.ifc` with Bonsai's `Open IFC Project`.
2. Confirm `1階` (Level 1) in Spatial Decomposition and make it the working container.
3. Choose Space Tool and set Name to `MR-01`, Long Name to `設備機械室` (Equipment Room), and Type to `INTERNAL`.
4. Snap the four internal wall corners to create a 5600 × 3600 mm clear area.
5. Set Height to 3000 mm.
6. Enter use information in `Pset_SpaceCommon`.
7. Verify Gross and Net Planned Area as 20.16 m².
8. Verify Height 3000 mm, Net Floor Area 20.16 m², and Net Volume 60.48 m³.
9. Verify that `MR-01` is aggregated below Level 1.
10. Save as `bonsai_intro06.ifc` and reopen it in a new session.

## Rebuild with the script

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep08-space-properties\scripts\create_training_space_ifc.py" --
```

Validate the completed model:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep08-space-properties\scripts\validate_training_space_ifc.py" -- ".\blender-bonsai\ep08-space-properties\completed\bonsai_intro06.ifc"
```

## IFC completion criteria

- IFC4 with millimetre-based input
- One IfcSpace: Name `MR-01`, LongName `設備機械室`
- 5600 × 3600 mm clear area, 3000 mm height
- Net Floor Area 20.16 m² and Net Volume 60.48 m³
- `Pset_SpaceCommon` and quantity set retained
- `MR-01` aggregated under Level 1 by IfcRelAggregates

## Notice

Dimensions, identifiers, and use classifications are simplified assumptions for software training. A real project must define area rules, levels, zones, regulations, and facility-management requirements.

日本語: [README.md](README.md)
