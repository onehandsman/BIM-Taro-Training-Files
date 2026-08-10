# Blender + Bonsai IFC Basics Episode 6: Equipment Room Exterior Walls

This package starts with a 6000 × 4000 × 200 mm floor slab and adds four exterior walls with a 200 mm material-layer thickness and a 3000 mm height. It is designed for beginners to reproduce the lesson and compare their result with a validated IFC file.

- Video: https://youtu.be/EwG2iRX-rX0
- Japanese article: https://note.com/real_finch7263/n/n413bb6487b65

## Files

| Path | Purpose |
|---|---|
| `start/bonsai_intro03_t200.ifc` | Start model with one 6000 × 4000 × 200 mm slab on Level 1 |
| `completed/bonsai_intro04.ifc` | Completed example with one slab and four exterior walls |
| `scripts/create_training_walls_ifc.py` | Rebuilds the walls with configurable thickness and height |
| `scripts/validate_training_walls_ifc.py` | Verifies IFC class, type, dimensions, placement, and spatial container |
| `SHA256SUMS.txt` | SHA-256 hashes for integrity checks |

## Reproduce the video operation

1. In Bonsai, use `Open IFC Project` to open `start/bonsai_intro03_t200.ifc`.
2. In Spatial Decomposition, set the active container to `1階` (Level 1).
3. In Object Mode, activate Wall Tool and prepare an `外壁 t200` IfcWallType.
4. Set the material-layer thickness to 200 mm and Height to 3000 mm.
5. Starting at the southwest corner, create walls in this order: south 6000, east 4000, north 6000, and west 4000 mm.
6. Check endpoint snapping, 90-degree rotation, and the inward thickness direction for every segment.
7. Use Mitre to clean up corner joints if necessary.
8. Verify four IfcWall elements, Type `外壁 t200`, and Spatial Container `1階`.
9. Use `Save IFC Project As…` to save `bonsai_intro04.ifc`, then compare it with the completed example.

## Rebuild with the script

Open PowerShell at the repository root and run:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep06-exterior-walls\scripts\create_training_walls_ifc.py" -- --thickness-mm 200 --height-mm 3000 --output ".\generated\bonsai_intro04.ifc"
```

To validate the completed example:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep06-exterior-walls\scripts\validate_training_walls_ifc.py" -- ".\blender-bonsai\ep06-exterior-walls\completed\bonsai_intro04.ifc"
```

Adjust the Blender executable path if your installation is elsewhere.

## Dimension notice

The 200 mm wall thickness, 3000 mm height, and 6000 × 4000 mm floor outline are simplified assumptions for software training. Actual values must be selected for the project’s structural, finish, MEP, fire, acoustic, waterproofing, and regulatory requirements. Do not copy these values directly into a real project.

日本語: [README.md](README.md)
