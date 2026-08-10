# BIM太郎 研修用データ

YouTube／note「BIM太郎」のBIM・CAD初心者向け動画を、見た直後に自分のPCで再現するための教材データです。

Blender＋Bonsai IFC入門の開始モデル、完成例、再生成・検証スクリプトを、エピソード単位で収録しています。

## 教材一覧

| 教材 | 内容 | 動画 |
|---|---|---|
| [Blender＋Bonsai 第5回：設備室の床スラブ](blender-bonsai/ep05-floor-slab/README.md) | IFC4開始モデル、150 mm履歴版、200 mm継続版、生成スクリプト | [YouTube](https://youtu.be/Leuoe1HfsAY) |
| [Blender＋Bonsai 第6回：設備室の外周壁](blender-bonsai/ep06-exterior-walls/README.md) | 200 mm床の開始モデル、外周壁4本の完成例、生成・検証スクリプト | 公開URLを追記予定 |

## まず試す

1. GitHubのReleasesからZIPをダウンロードして展開します。
2. Blender 5.2 LTSとBonsai 0.8.5、または互換性のある新しい版を用意します。
3. 学習するエピソードのREADMEを開き、指定された `start` IFCをBonsaiの `Open IFC Project` から開きます。
4. READMEと動画を見ながら操作します。
5. 完成後、`completed` または推奨継続版のIFCと比較します。

制作時の検証環境はBlender 5.2.0 LTS、Bonsai 0.8.5、IFC4、長さの入力単位はミリメートルです。新しい版では画面配置やボタン名が変わる場合があります。

## ライセンス

- Pythonスクリプト：MIT License
- IFCモデル、README、教材文書：Creative Commons Attribution 4.0 International（CC BY 4.0）

詳しくは[ライセンス案内](LICENSE.md)を参照してください。

## 注意

本教材の寸法・名称・構成は、操作学習用の仮設定です。実案件の設計値、構造安全性、法令適合性を保証するものではありません。床厚は、荷重、振動、スパン、支持条件、開口、アンカー等を踏まえて構造設計者が決定してください。

English instructions: [README_EN.md](README_EN.md)
