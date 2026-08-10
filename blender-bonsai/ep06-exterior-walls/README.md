# Blender＋Bonsai IFC入門 第6回：設備室の外周壁

この教材では、6000×4000×200 mmの床スラブを設定済みの開始モデルから、厚さ200 mm・高さ3000 mmの外周壁を4本作ります。初心者が動画と同じ操作を再現し、完成IFCと比較できる構成です。

- 動画：公開URLを追記予定
- 解説記事：公開URLを追記予定

## ファイル

| パス | 用途 |
|---|---|
| `start/bonsai_intro03_t200.ifc` | 操作開始用。1階に6000×4000×200 mmの床を設定済み |
| `completed/bonsai_intro04.ifc` | 完成例。床1枚と外周壁4本を収録 |
| `scripts/create_training_walls_ifc.py` | 開始モデルから指定厚さ・高さの外周壁を再生成 |
| `scripts/validate_training_walls_ifc.py` | IFCクラス、タイプ、寸法、配置、所属先を検証 |
| `SHA256SUMS.txt` | 配布ファイルが壊れていないか確認するハッシュ値 |

## 動画と同じ操作

1. Bonsaiの `Open IFC Project` で `start/bonsai_intro03_t200.ifc` を開きます。
2. Spatial DecompositionでActive Containerを `1階` にします。
3. Object ModeでWall Toolを選び、`外壁 t200` のIfcWallTypeを準備します。
4. Material Layerの厚さを200 mm、Heightを3000 mmにします。
5. 南西角を始点に、南6000、東4000、北6000、西4000 mmの順で壁を作ります。
6. 各辺で端点スナップ、90度回転、壁厚が内側へ出る向きを確認します。
7. 必要ならMitreで四隅を整えます。
8. IfcWall 4件、Type `外壁 t200`、Spatial Container `1階` を確認します。
9. `Save IFC Project As…` で `bonsai_intro04.ifc` として保存し、完成例と比較します。

## スクリプトで再生成

リポジトリのルートでPowerShellを開き、次を実行します。

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep06-exterior-walls\scripts\create_training_walls_ifc.py" -- --thickness-mm 200 --height-mm 3000 --output ".\generated\bonsai_intro04.ifc"
```

完成例を検証する場合：

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep06-exterior-walls\scripts\validate_training_walls_ifc.py" -- ".\blender-bonsai\ep06-exterior-walls\completed\bonsai_intro04.ifc"
```

Blender／Bonsaiのインストール場所が異なる場合は、先頭の実行ファイルパスを変更してください。

## 寸法について

壁厚200 mm、壁高3000 mm、床外形6000×4000 mmは操作学習用の仮設定です。実案件では構造、仕上げ、設備、耐火・遮音、防水、法令などの条件に応じて設計してください。この教材の値をそのまま転用しないでください。

English: [README_EN.md](README_EN.md)
