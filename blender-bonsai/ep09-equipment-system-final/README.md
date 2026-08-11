# Blender＋Bonsai IFC入門 第9回：設備要素と最終確認

この教材では、設備機械室 `MR-01` に空調機と100A冷水往還管を配置し、空間所属と冷水配管系統を設定します。見た目だけでなく、クラス、Tag、Container、Systemを確認して機械室IFCを完成させます。

- 動画：https://youtu.be/DlsK0wesJJk
- note記事：https://note.com/real_finch7263/n/ne380d0bf8def

## ファイル

| パス | 用途 |
|---|---|
| `start/bonsai_intro06.ifc` | 操作開始用。設備機械室 `MR-01` まで設定済み |
| `completed/bonsai_intro07.ifc` | 完成例。空調機・冷水往還管・CHW-01系統を追加済み |
| `generated/bonsai_intro07.ifc` | スクリプト再生成時の比較用完成モデル |
| `scripts/create_training_equipment_ifc.py` | 設備要素、空間所属、設備系統を再生成 |
| `scripts/validate_training_equipment_ifc.py` | IFCクラス、タイプ、Tag、Container、Systemを検証 |
| `SHA256SUMS.txt` | 配布ファイルが壊れていないか確認するハッシュ値 |

## 動画と同じ操作

1. `start/bonsai_intro06.ifc` を開き、`MR-01 設備機械室` をActive Containerにします。
2. `IfcUnitaryEquipmentType`／`AIRHANDLER` の空調機タイプを作ります。
3. NameとTagを `AHU-01`、外形を1800×800×1200 mmとして床へ配置します。
4. 搬入扉の動線を避け、EquipmentID、Service、DataStatusを確認します。
5. `IfcPipeSegmentType`／`RIGIDSEGMENT`／100Aの配管タイプを作ります。
6. 往管 `CHWS-01` をRL2400、長さ5200 mmで作成します。
7. 還管 `CHWR-01` を平行に作成します。
8. `IfcDistributionSystem`／`CHILLEDWATER` の `CHW-01` を作り、3要素を割り当てます。
9. 3要素すべてのSpatial Containerが `MR-01` であることを確認します。
10. 形・クラス・Tag・Container・Systemを確認し、`bonsai_intro07.ifc` として保存・再読込します。

## スクリプトで再生成

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep09-equipment-system-final\scripts\create_training_equipment_ifc.py" --
```

完成例を検証する場合：

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep09-equipment-system-final\scripts\validate_training_equipment_ifc.py" -- ".\blender-bonsai\ep09-equipment-system-final\completed\bonsai_intro07.ifc"
```

## IFCとしての完成条件

- IfcUnitaryEquipment 1件：`空調機 AHU-01`、Tag `AHU-01`
- IfcPipeSegment 2件：`CHWS-01`、`CHWR-01`、100A
- IfcDistributionSystem 1件：`CHW-01`、PredefinedType `CHILLEDWATER`
- 3要素すべてのSpatial Container：`MR-01`
- 3要素すべてが `CHW-01` に割当済み
- 保存後の再読込でクラス・Tag・Container・Systemを保持

## 注意

能力、寸法、口径、配置、保守空間は操作学習用の仮設定です。実案件では、熱負荷、流量、圧力損失、勾配、支持、搬入・更新経路、保守性、構造、法令などを担当者が確認してください。

English: [README_EN.md](README_EN.md)
