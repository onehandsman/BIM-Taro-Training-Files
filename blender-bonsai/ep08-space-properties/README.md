# Blender＋Bonsai IFC入門 第8回：空間と属性

この教材では、開口・ドア・窓まで設定済みの設備室に `IfcSpace` を追加し、部屋番号、用途、面積、体積を持たせます。初心者が動画と同じ操作を再現し、完成例と比較できる構成です。

- 動画：https://youtu.be/rGZRIptOo3c
- note記事：https://note.com/real_finch7263/n/n560758df124e

## ファイル

| パス | 用途 |
|---|---|
| `start/bonsai_intro05.ifc` | 操作開始用。床・壁・開口・ドア・窓を設定済み |
| `completed/bonsai_intro06.ifc` | 完成例。設備機械室 `MR-01` を追加済み |
| `generated/bonsai_intro06.ifc` | スクリプト再生成時の比較用完成モデル |
| `scripts/create_training_space_ifc.py` | 開始モデルから空間・属性・数量を再生成 |
| `scripts/validate_training_space_ifc.py` | 空間のクラス、寸法、属性、数量、階層を検証 |
| `SHA256SUMS.txt` | 配布ファイルが壊れていないか確認するハッシュ値 |

## 動画と同じ操作

1. Bonsaiの `Open IFC Project` で `start/bonsai_intro05.ifc` を開きます。
2. Spatial Decompositionで `1階` を確認し、作業先にします。
3. Space Toolを選び、Nameを `MR-01`、Long Nameを `設備機械室`、Typeを `INTERNAL` にします。
4. 壁の内側4点を順にスナップし、内法5600×3600 mmの範囲を作ります。
5. Heightを3000 mmにします。
6. `Pset_SpaceCommon` にReference、Occupancy Typeなどの用途情報を入れます。
7. Gross／Net Planned Areaを20.16 m²として確認します。
8. Height 3000 mm、Net Floor Area 20.16 m²、Net Volume 60.48 m³を確認します。
9. `MR-01` が `1階` の下に集約されていることを確認します。
10. `bonsai_intro06.ifc` として保存し、新規セッションで再読込します。

## スクリプトで再生成

リポジトリのルートでPowerShellを開き、次を実行します。

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep08-space-properties\scripts\create_training_space_ifc.py" --
```

完成例を検証する場合：

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep08-space-properties\scripts\validate_training_space_ifc.py" -- ".\blender-bonsai\ep08-space-properties\completed\bonsai_intro06.ifc"
```

## IFCとしての完成条件

- IFC4、入力単位ミリメートル
- IfcSpace 1件：Name `MR-01`、LongName `設備機械室`
- 内法5600×3600 mm、高さ3000 mm
- Net Floor Area 20.16 m²、Net Volume 60.48 m³
- `Pset_SpaceCommon` と数量セットを保持
- `MR-01` がIfcRelAggregatesで `1階` の下に所属

## 注意

寸法、名称、用途は操作学習用の仮設定です。実案件では、面積区分、天井・床の基準、ゾーン、法令、維持管理ルールなどを担当者が確認してください。

English: [README_EN.md](README_EN.md)
