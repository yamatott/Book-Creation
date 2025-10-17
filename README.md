# Book Creation Agent

**Status**: ✅ Fully Implemented (2025-10-17)

このリポジトリは、与えられた指示と情報から書籍を生成する完全実装済みシステムです。ドラフト作成、画像生成、清書の3フェーズで構成され、Google Gemini APIを用いた画像生成を組み込みます。

**実績**: 「家庭でできる肉の発酵・熟成」(17章、159画像、200MB PDF) を生成済み

## 主な機能
- 入力された指示・情報の確認と補足依頼
- 章構成案の作成と章ごとのMarkdownドラフト生成
- 画像プレースホルダーの設置とGemini APIを介した画像生成（タイプ別最適化）
- ドラフトの統合、デザイン調整、PDFへの変換

## ワークフロー概要
1. 指示・情報を受け取り、内容が十分かを確認
2. 章構成案を作成し、ユーザ承認後にドラフト用フォルダと章ごとのMarkdownファイルを用意
3. ドラフト内容のレビュー（専門性・正確性の確認）
4. 画像プレースホルダーをもとにGoogle Gemini APIで画像を生成し、`img/`に保存
5. 生成物を統合して最終Markdownを作成し、PDFに変換して納品

詳細なフローや要件は `objectives.md` および `CLAUDE.md` に整理されています。

## ディレクトリ構成
```
├── objectives.md                  # プロジェクト仕様（日本語）
├── CLAUDE.md                      # エージェント向けガイダンス
├── sampleGeminiImageAPI.md        # Gemini API の使用例
├── .env.example                   # APIキーの設定例
├── generate_images.py             # 画像生成スクリプト（v2.0）
├── test_generate_10.py            # テスト用スクリプト
├── create_print_ready_html.py     # 印刷用HTML生成
├── draft/                         # ドラフト章 (処理中に生成)
├── img/                           # 生成画像 (処理中に生成)
└── final/                         # 清書版ファイル (処理中に生成)
```

## セットアップ

### 1. Python依存関係
```bash
pip3 install google-generativeai Pillow python-dotenv
```

### 2. システムツール
```bash
# macOS (Homebrew)
brew install pandoc
brew install --cask google-chrome
```

### 3. API設定
1. `.env.example` をコピーして `.env` を作成
2. Google AI Studio (https://aistudio.google.com) でAPIキーを取得
3. `.env` に `GOOGLE_API_KEY=your_key_here` を設定
4. **重要**: 大量画像生成には有料プラン必須

### 4. 動作確認
```bash
# 最初の10枚でテスト
python3 test_generate_10.py

# 問題なければ全画像生成
python3 generate_images.py --auto
```

## 画像生成サンプル

### 堅牢な実装例
```python
import base64
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# モデル初期化
model = genai.GenerativeModel("gemini-2.5-flash-image-preview")

# 画像生成
prompt = "宇宙を飛ぶ犬のイラストを生成してください"
response = model.generate_content(prompt)

# 堅牢なレスポンス処理
if response.candidates and response.candidates[0].content.parts:
    # 全partsからinline_dataを探す
    image_part = None
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            image_part = part
            break

    if image_part:
        data = image_part.inline_data.data

        # bytes または base64 の判定
        if isinstance(data, bytes):
            image_bytes = data
        else:
            image_bytes = base64.b64decode(data)

        # 画像保存
        image = Image.open(BytesIO(image_bytes))
        image.save("dog_in_space.png")
        print("✓ 画像生成成功")
    else:
        print("✗ inline_dataが見つかりません")
else:
    print("✗ レスポンスが空です")
```

### よくあるエラーと対処法

**エラー1**: `AttributeError: 'Part' object has no attribute 'inline_data'`
- **原因**: parts[0]に画像データがない
- **対処**: 全partsをループして探す（上記コード参照）

**エラー2**: `429 Resource exhausted (quota)`
- **原因**: 無料プランのクォータ超過
- **対処**: Google AI Studioで有料プランに切り替え

**エラー3**: `PIL.UnidentifiedImageError`
- **原因**: base64デコードが必要なのにbytesとして扱った
- **対処**: `isinstance(data, bytes)` で判定（上記コード参照）

## 使用方法

### 完全ワークフロー

#### 1. ドラフト作成
（手動または別ツールで章ごとのmarkdownファイルを作成）

#### 2. 画像生成
```bash
# テスト（最初の10枚）
python3 test_generate_10.py

# 全画像生成
python3 generate_images.py --auto
```

#### 3. PDF生成
```bash
# Step 1: Markdown統合
cat draft/*.md > final/完成版_書籍名.md

# Step 2: HTML生成
pandoc final/完成版_書籍名.md \
  -o final/完成版_書籍名.html \
  --standalone \
  --metadata title="書籍名"

# Step 3: 印刷用HTML作成
python3 create_print_ready_html.py

# Step 4: PDF変換
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --disable-gpu \
  --print-to-pdf="final/完成版_書籍名.pdf" \
  --no-pdf-header-footer \
  "file://$(pwd)/final/完成版_書籍名_印刷用.html"
```

### コスト見積もり
- **API料金**: 160枚 × $0.039 ≒ $6-7
- **所要時間**: 画像生成 30分、PDF生成 30秒

## 改善版の特徴（v2.0）

### 画像生成の改善
- ✅ 画像タイプの自動分類（9カテゴリー）
- ✅ タイプ別最適化プロンプト
- ✅ 書籍文脈の統合
- ✅ スタイルガイド準拠

### 画像タイプ分布
```
illustration   : 116枚 (71.2%)
process        :  17枚 (10.4%)
graph          :   8枚 ( 4.9%)
photo          :   7枚 ( 4.3%)
concept        :   6枚 ( 3.7%)
cross_section  :   5枚 ( 3.1%)
table          :   2枚 ( 1.2%)
icon           :   1枚 ( 0.6%)
flowchart      :   1枚 ( 0.6%)
```

## トラブルシューティング
詳細は以下のドキュメントを参照：
- `PROJECT_RETROSPECTIVE.md`: プロジェクト全体の振り返り
- `IMAGE_GENERATION_RETROSPECTIVE.md`: 画像生成の詳細分析
- `USER_PREFERENCES.md`: 作業スタイルガイド
- `IMPROVEMENT_APPLIED.md`: 改善版適用報告

このREADMEはプロジェクト概要と使用手順をまとめたもので、実装済みシステムのリファレンスとして活用してください。
