# Blender + Bonsai IFC Basics Episode 5: Equipment Room Floor Slab

This package starts with an IFC model whose spatial hierarchy is already configured. You will create one equipment-room floor slab, save the result, and compare it with validated examples.

- Video: [Blender + Bonsai IFC Basics 5](https://youtu.be/Leuoe1HfsAY)
- Japanese article: [note](https://note.com/real_finch7263/n/nbbdb4139ec00)

## Files

| Path | Purpose |
|---|---|
| `start/bonsai_intro02.ifc` | Start model with Project, Site, Building, and Level 1 already configured |
| `published-video-version/bonsai_intro03_t150.ifc` | Archived 150 mm model matching the published video |
| `recommended-next-version/bonsai_intro03_t200.ifc` | Recommended 200 mm continuation used from Episode 6 onward |
| `scripts/create_training_slab_ifc.py` | Rebuilds a slab of the specified thickness from the start model |
| `SHA256SUMS.txt` | SHA-256 hashes for integrity checks |

## Reproduce the video operation

1. In Bonsai, use `Open IFC Project` to open `start/bonsai_intro02.ifc`.
2. Confirm that the active spatial container is `1階` (Level 1).
3. In Object Mode, select the Slab Tool and prepare the slab type.
4. Use 150 mm to reproduce the published video, or 200 mm for the continuing series.
5. Draw a closed 6000 mm by 4000 mm outline.
6. Confirm that the object is an IfcSlab, its Predefined Type is `FLOOR`, and its Spatial Container is `1階`.
7. Use `Save IFC Project As…` and compare your saved model with the completed example.

## Rebuild with the script

Open PowerShell at the repository root and run:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep05-floor-slab\scripts\create_training_slab_ifc.py" -- --thickness-mm 200 --output ".\generated\bonsai_intro03_t200.ifc"
```

Change the value to `--thickness-mm 150` to rebuild the archived video version. If Blender is installed elsewhere, adjust the executable path.

## Dimension notice

Both 150 mm and 200 mm are simplified assumptions for software training. Actual equipment-room slab thickness must be determined by the responsible structural engineer after considering static and dynamic loads, vibration, spans, supports, openings, anchors, fire resistance, acoustics, and other project requirements. Do not copy these values directly into a real project.

日本語: [README.md](README.md)
