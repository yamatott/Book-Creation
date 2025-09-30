# Book Creation Agent

このリポジトリは、与えられた指示と情報から書籍を生成するエージェントのための仕様・計画書です。ドラフト作成、画像生成、清書の3フェーズで構成され、Google nanobanana APIを用いた画像生成を組み込みます。

## 主な機能
- 入力された指示・情報の確認と補足依頼
- 章構成案の作成と章ごとのMarkdownドラフト生成
- 画像プレースホルダーの設置とnanobanana APIを介した画像生成
- ドラフトの統合、デザイン調整、PDFへの変換

## ワークフロー概要
1. 指示・情報を受け取り、内容が十分かを確認
2. 章構成案を作成し、ユーザ承認後にドラフト用フォルダと章ごとのMarkdownファイルを用意
3. 画像プレースホルダーをもとにGoogle nanobanana APIで画像を生成し、`img/`に保存
4. 生成物を統合して最終Markdownを作成し、PDFに変換して納品

詳細なフローや要件は `objectives.md` および `CLAUDE.md` に整理されています。

## ディレクトリ構成
```
├── objectives.md                  # プロジェクト仕様（日本語）
├── CLAUDE.md                      # エージェント向けガイダンス
├── sampleNanobananaAPIrequest.md  # nanobanana API の使用例
├── .env.example                   # APIキーの設定例
├── draft/                         # ドラフト章 (処理中に生成)
├── img/                           # 生成画像 (処理中に生成)
└── final/                         # 清書版ファイル (処理中に生成)
```

## セットアップ
1. `.env.example` をコピーして `.env` を作成し、Google nanobanana APIキーを設定します。
2. Python環境を整え、`google-generativeai` や `Pillow` など必要な依存関係をインストールします。
3. `sampleNanobananaAPIrequest.md` を参考にAPI呼び出し実装を行います。

## 画像生成サンプル
```python
import google.generativeai as genai
from PIL import Image
from io import BytesIO

genai.configure(api_key="取得したAPIキー")
model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
prompt = "宇宙を飛ぶ犬のイラストを生成してください"
response = model.generate_content(prompt)
image_data = BytesIO(response.candidates[0].content.parts[1].inline_data.data)
Image.open(image_data).save("dog_in_space.png")
```

## 今後の課題
- 各フェーズを自動化するエージェントの実装
- エラーハンドリングや再試行戦略の設計
- PDF変換およびレイアウト調整フローの具体化

このREADMEはプロジェクト概要と開始手順をまとめたもので、実装時のリファレンスとして活用してください。
