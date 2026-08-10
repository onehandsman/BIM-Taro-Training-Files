# BIM太郎 研修用データ

YouTube／note「BIM太郎」のBIM・CAD初心者向け動画を、見た直後に自分のPCで再現するための教材データです。

試験公開の第1弾として、Blender＋Bonsai IFC入門 第5回「設備室の床スラブ」の開始モデル、完成例、再生成スクリプトを収録しています。

## 教材一覧

| 教材 | 内容 | 動画 |
|---|---|---|
| [Blender＋Bonsai 第5回：設備室の床スラブ](blender-bonsai/ep05-floor-slab/README.md) | IFC4開始モデル、150 mm履歴版、200 mm継続版、生成スクリプト | [YouTube](https://youtu.be/Leuoe1HfsAY) |

## まず試す

1. GitHubのReleasesからZIPをダウンロードして展開します。
2. Blender 5.2 LTSとBonsai 0.8.5、または互換性のある新しい版を用意します。
3. Bonsaiの `Open IFC Project` から `start/bonsai_intro02.ifc` を開きます。
4. [第5回の手順書](blender-bonsai/ep05-floor-slab/README.md)と動画を見ながら床スラブを作成します。
5. 完成後、150 mmの動画再現版または200 mmの継続版と比較します。

制作時の検証環境はBlender 5.2.0 LTS、Bonsai 0.8.5、IFC4、長さの入力単位はミリメートルです。新しい版では画面配置やボタン名が変わる場合があります。

## ライセンス

- Pythonスクリプト：MIT License
- IFCモデル、README、教材文書：Creative Commons Attribution 4.0 International（CC BY 4.0）

詳しくは[ライセンス案内](LICENSE.md)を参照してください。

## 注意

本教材の寸法・名称・構成は、操作学習用の仮設定です。実案件の設計値、構造安全性、法令適合性を保証するものではありません。床厚は、荷重、振動、スパン、支持条件、開口、アンカー等を踏まえて構造設計者が決定してください。

English instructions: [README_EN.md](README_EN.md)
