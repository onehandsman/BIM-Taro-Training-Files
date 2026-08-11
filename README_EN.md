# BIM Taro Training Files

These files accompany the beginner-friendly BIM/CAD videos published by BIM Taro on YouTube and note. The goal is to let viewers reproduce each operation immediately after watching it.

The repository contains start models, completed examples, and reproducible generator and validation scripts for each Blender + Bonsai IFC Basics episode.

## Available training package

| Package | Contents | Video |
|---|---|---|
| [Blender + Bonsai Episode 5: Equipment Room Floor Slab](blender-bonsai/ep05-floor-slab/README_EN.md) | IFC4 start model, archived 150 mm version, recommended 200 mm continuation, generator script | [YouTube](https://youtu.be/Leuoe1HfsAY) |
| [Blender + Bonsai Episode 6: Equipment Room Exterior Walls](blender-bonsai/ep06-exterior-walls/README_EN.md) | Start model with a 200 mm slab, completed four-wall model, generator and validator scripts | [YouTube](https://youtu.be/EwG2iRX-rX0) |
| [Blender + Bonsai Episode 7: Openings, Doors, and Windows](blender-bonsai/ep07-openings-doors-windows/README_EN.md) | Exterior-wall start model, completed model with two openings, one door and one window, generator and validator scripts | Preparing publication |

## Quick start

1. Download and extract the ZIP from GitHub Releases.
2. Install Blender 5.2 LTS with Bonsai 0.8.5, or a compatible newer version.
3. Open the README for the episode you want to study, then use `Open IFC Project` for its specified start IFC.
4. Follow the README together with the video.
5. Compare your result with the completed or recommended continuation IFC.

The package was validated with Blender 5.2.0 LTS, Bonsai 0.8.5, IFC4, and millimetre-based input. Newer versions may have different screen layouts or command names.

## License

- Python scripts: MIT License
- IFC models, README files, and training documentation: Creative Commons Attribution 4.0 International (CC BY 4.0)

See [LICENSE.md](LICENSE.md) for details.

## Important notice

All dimensions, names, and assemblies are simplified assumptions for software training. They are not project-specific design values and do not certify structural safety or code compliance. Slab thickness must be decided by the responsible structural engineer after considering loads, vibration, spans, supports, openings, anchors, and other project conditions.

日本語: [README.md](README.md)
