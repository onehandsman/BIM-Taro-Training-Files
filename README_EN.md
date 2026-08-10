# BIM Taro Training Files

These files accompany the beginner-friendly BIM/CAD videos published by BIM Taro on YouTube and note. The goal is to let viewers reproduce each operation immediately after watching it.

This trial release contains the start model, completed examples, and a reproducible generator script for Blender + Bonsai IFC Basics Episode 5: Equipment Room Floor Slab.

## Available training package

| Package | Contents | Video |
|---|---|---|
| [Blender + Bonsai Episode 5: Equipment Room Floor Slab](blender-bonsai/ep05-floor-slab/README_EN.md) | IFC4 start model, archived 150 mm version, recommended 200 mm continuation, generator script | [YouTube](https://youtu.be/Leuoe1HfsAY) |

## Quick start

1. Download and extract the ZIP from GitHub Releases.
2. Install Blender 5.2 LTS with Bonsai 0.8.5, or a compatible newer version.
3. In Bonsai, use `Open IFC Project` to open `start/bonsai_intro02.ifc`.
4. Follow the [Episode 5 instructions](blender-bonsai/ep05-floor-slab/README_EN.md) together with the video.
5. Compare your result with either the archived 150 mm video version or the recommended 200 mm continuation.

The package was validated with Blender 5.2.0 LTS, Bonsai 0.8.5, IFC4, and millimetre-based input. Newer versions may have different screen layouts or command names.

## License

- Python scripts: MIT License
- IFC models, README files, and training documentation: Creative Commons Attribution 4.0 International (CC BY 4.0)

See [LICENSE.md](LICENSE.md) for details.

## Important notice

All dimensions, names, and assemblies are simplified assumptions for software training. They are not project-specific design values and do not certify structural safety or code compliance. Slab thickness must be decided by the responsible structural engineer after considering loads, vibration, spans, supports, openings, anchors, and other project conditions.

日本語: [README.md](README.md)
