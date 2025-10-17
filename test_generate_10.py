#!/usr/bin/env python3
"""
テスト画像生成スクリプト - 最初の10枚
"""

import os
import sys
import base64
import time
from pathlib import Path
from io import BytesIO
from dotenv import load_dotenv

print("=" * 60)
print("テスト: 最初の10枚の画像を生成")
print("=" * 60)

# 環境変数の読み込み
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

print(f"APIキー確認: {'設定済み' if API_KEY and API_KEY != 'your_google_api_key_here' else '未設定'}")

try:
    import google.generativeai as genai
    from PIL import Image
    print("ライブラリ: OK")
except ImportError as e:
    print(f"ライブラリエラー: {e}")
    sys.exit(1)

# API設定
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-image-preview")

# imgディレクトリ作成
IMG_DIR = Path("img")
IMG_DIR.mkdir(exist_ok=True)

# 画像リストから最初の10枚を読み込み
IMAGE_LIST_FILE = "/tmp/image_list.txt"
test_images = []

with open(IMAGE_LIST_FILE, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 10:
            break
        line = line.strip()
        if line:
            parts = line.split('|', 1)
            if len(parts) == 2:
                filename, description = parts
                test_images.append((filename, description))

print(f"\n{len(test_images)}枚の画像を生成します...\n")

success_count = 0
fail_count = 0

for i, (filename, description) in enumerate(test_images, 1):
    output_path = IMG_DIR / filename

    if output_path.exists():
        print(f"[{i}/10] スキップ: {filename} (既存)")
        success_count += 1
        continue

    print(f"[{i}/10] 生成中: {description}")

    prompt = f"""
書籍の挿絵として使用する図やイラストを生成してください。

説明: {description}

要件:
- プロフェッショナルで教育的なスタイル
- 情報を明確に視覚化
- 書籍に適した品質
"""

    try:
        response = model.generate_content(prompt)

        if response.candidates and response.candidates[0].content.parts:
            # すべてのパーツから画像データを探す
            image_part = None
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_part = part
                    break

            if image_part:
                # inline_data.data は既にバイナリの場合とbase64文字列の場合がある
                data = image_part.inline_data.data

                if isinstance(data, bytes):
                    # 既にバイナリ
                    image_bytes = data
                else:
                    # Base64文字列
                    image_bytes = base64.b64decode(data)

                image = Image.open(BytesIO(image_bytes))
                image.save(output_path)
                print(f"  ✓ 成功: {filename}")
                success_count += 1
            else:
                print(f"  ✗ エラー: inline_dataがありません")
                fail_count += 1
        else:
            print(f"  ✗ エラー: 有効なレスポンスがありません")
            fail_count += 1

    except Exception as e:
        print(f"  ✗ エラー: {e}")
        fail_count += 1

    # レート制限を考慮して待機
    if i < len(test_images):
        time.sleep(2)

print("\n" + "=" * 60)
print("テスト完了")
print("=" * 60)
print(f"成功: {success_count}枚")
print(f"失敗: {fail_count}枚")
print(f"合計: {len(test_images)}枚")
print(f"保存先: {IMG_DIR.absolute()}")
print("=" * 60)

if success_count == len(test_images):
    print("\n✓ すべて成功しました！")
    print("全画像を生成するには:")
    print("  python3 generate_images.py --auto")
elif success_count > 0:
    print(f"\n⚠ 一部成功 ({success_count}/{len(test_images)})")
else:
    print("\n✗ 生成に失敗しました。APIキーと設定を確認してください。")
