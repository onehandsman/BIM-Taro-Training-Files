# Blender＋Bonsai IFC入門 第7回：開口・ドア・窓

この教材では、床1枚と外周壁4本を設定済みの設備室へ、設備搬入用の両開き扉と窓を配置します。初心者が動画と同じ操作を再現し、壁・開口・建具のIFC関係まで完成例と比較できる構成です。

- 動画：公開後に追記
- note記事：公開後に追記

## ファイル

| パス | 用途 |
|---|---|
| `start/bonsai_intro04.ifc` | 操作開始用。床1枚と外周壁4本を設定済み |
| `completed/bonsai_intro05.ifc` | 完成例。開口2、ドア1、窓1を追加済み |
| `scripts/create_training_openings_ifc.py` | 開始モデルから開口・ドア・窓を再生成 |
| `scripts/validate_training_openings_ifc.py` | IFCクラス、タイプ、寸法、開口関係、所属先を検証 |
| `SHA256SUMS.txt` | 配布ファイルが壊れていないか確認するハッシュ値 |

## 動画と同じ操作

1. Bonsaiの `Open IFC Project` で `start/bonsai_intro04.ifc` を開きます。
2. Object ModeでDoor Toolを選び、`設備搬入用扉 W1500×H2100` のIfcDoorTypeを準備します。
3. Overall Width 1500 mm、Overall Height 2100 mm、`DOUBLE_DOOR_SINGLE_SWING`、Predefined Type `DOOR` を設定します。
4. 南壁へスナップし、西端から750 mmの位置へ配置します。下端はRL1＝0 mmです。
5. Window Toolへ切り替え、`設備室窓 W1200×H900` のIfcWindowTypeを準備します。
6. Overall Width 1200 mm、Overall Height 900 mm、`SINGLE_PANEL`、Predefined Type `WINDOW`、RL2＝1200 mmを設定します。
7. 北壁へスナップして配置します。
8. IfcOpeningElement 2件、IfcRelVoidsElement 2件、IfcRelFillsElement 2件を確認します。
9. ドアと窓のSpatial Containerが `1階` であることを確認します。
10. `Save IFC Project As…` で `bonsai_intro05.ifc` として保存し、完成例と比較します。

## スクリプトで再生成

リポジトリのルートでPowerShellを開き、次を実行します。

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep07-openings-doors-windows\scripts\create_training_openings_ifc.py" --
```

完成例を検証する場合：

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep07-openings-doors-windows\scripts\validate_training_openings_ifc.py" -- ".\blender-bonsai\ep07-openings-doors-windows\completed\bonsai_intro05.ifc"
```

Blender／Bonsaiのインストール場所が異なる場合は、先頭の実行ファイルパスを変更してください。

## IFCとしての完成条件

- IFC4、入力単位ミリメートル
- IfcSlab 1件、IfcWall 4件
- IfcOpeningElement 2件、IfcDoor 1件、IfcWindow 1件
- IfcRelVoidsElement 2件、IfcRelFillsElement 2件
- ドア：W1500×H2100 mm、DOUBLE_DOOR_SINGLE_SWING
- 窓：W1200×H900 mm、腰高1200 mm、SINGLE_PANEL
- ドアと窓のSpatial Container：`1階`

## 寸法について

この寸法は操作学習用の仮設定です。実案件では、機器の搬入・更新経路、有効開口、防火、遮音、換気、結露、構造、法令などの条件に応じて設計してください。表示形状の枠・額縁は、建具の呼び寸法より少し外へ張り出す場合があります。

English: [README_EN.md](README_EN.md)
