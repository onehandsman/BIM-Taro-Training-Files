# Blender＋Bonsai IFC入門 第5回：設備室の床スラブ

この教材では、IFCの空間階層を設定済みの開始モデルから、設備室の床スラブを1枚作ります。初心者が動画と同じ操作を再現し、完成モデルと比較できる構成です。

- 動画：[Blender＋Bonsai IFC入門 5｜設備室の床スラブ](https://youtu.be/Leuoe1HfsAY)
- 解説記事：[note](https://note.com/real_finch7263/n/nbbdb4139ec00)

## ファイル

| パス | 用途 |
|---|---|
| `start/bonsai_intro02.ifc` | 操作開始用。Project／Site／Building／1階まで設定済み |
| `published-video-version/bonsai_intro03_t150.ifc` | 公開動画と一致する150 mmの履歴版 |
| `recommended-next-version/bonsai_intro03_t200.ifc` | 第6回以降で使用する200 mmの継続版 |
| `scripts/create_training_slab_ifc.py` | 開始モデルから指定厚さの床スラブを再生成するスクリプト |
| `SHA256SUMS.txt` | 配布ファイルが壊れていないか確認するハッシュ値 |

## 動画と同じ操作

1. Bonsaiの `Open IFC Project` で `start/bonsai_intro02.ifc` を開きます。
2. 空間コンテナが `1階` であることを確認します。
3. Object ModeでSlab Toolを選び、床タイプを準備します。
4. 動画再現時は床厚を150 mm、継続学習時は200 mmに設定します。
5. X方向6000 mm、Y方向4000 mmの閉じた輪郭を作成します。
6. IfcSlabのPredefined Typeが `FLOOR`、Spatial Containerが `1階` であることを確認します。
7. `Save IFC Project As…` で別名保存し、完成例と比較します。

## スクリプトで再生成

リポジトリのルートでPowerShellを開き、次を実行します。

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python ".\blender-bonsai\ep05-floor-slab\scripts\create_training_slab_ifc.py" -- --thickness-mm 200 --output ".\generated\bonsai_intro03_t200.ifc"
```

150 mmの動画再現版を作る場合は、`--thickness-mm 150` に変更します。Blender／Bonsaiのインストール場所が異なる場合は、先頭の実行ファイルパスを変更してください。

## 寸法について

150 mm、200 mmとも操作学習用の仮設定です。実際の設備室床の厚さは、荷重、動荷重、振動、スパン、支持条件、開口、アンカー、耐火・遮音条件等を踏まえて構造設計者が決定します。この教材の値を実案件へそのまま転用しないでください。

English: [README_EN.md](README_EN.md)
