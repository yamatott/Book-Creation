# Google Gemini Image API 使用ガイド

このファイルは、Google Gemini API（画像生成モデル）の使用方法と、本番環境で必要な堅牢な実装例を示します。

---

## 基本情報

- **API名**: Google Gemini API
- **モデル**: `gemini-2.5-flash-image-preview`
- **公式ドキュメント**: https://ai.google.dev/
- **APIキー取得**: https://aistudio.google.com/

---

## 最小限の実装例

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
response = model.generate_content("宇宙を飛ぶ犬")

# ⚠️ これは動作しない可能性があります（parts[0]に画像があるとは限らない）
# image_data = response.candidates[0].content.parts[0].inline_data.data
```

---

## 本番環境向け堅牢な実装

### 完全なコード例

```python
import base64
import os
import time
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# 設定
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_image(prompt: str, output_path: str, retry=3) -> bool:
    """
    堅牢な画像生成関数

    Args:
        prompt: 画像生成プロンプト
        output_path: 保存先パス
        retry: リトライ回数

    Returns:
        成功時True、失敗時False
    """
    model = genai.GenerativeModel("gemini-2.5-flash-image-preview")

    for attempt in range(retry):
        try:
            response = model.generate_content(prompt)

            # レスポンスの検証
            if not response.candidates or not response.candidates[0].content.parts:
                print(f"⚠️ 空のレスポンス（試行 {attempt+1}/{retry}）")
                time.sleep(2)
                continue

            # 全partsからinline_dataを探す
            image_part = None
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_part = part
                    break

            if not image_part:
                print(f"⚠️ inline_dataが見つかりません（試行 {attempt+1}/{retry}）")
                time.sleep(2)
                continue

            # データ形式の判定と変換
            data = image_part.inline_data.data
            if isinstance(data, bytes):
                image_bytes = data
            else:
                image_bytes = base64.b64decode(data)

            # 画像保存
            image = Image.open(BytesIO(image_bytes))
            image.save(output_path)

            print(f"✓ {output_path} を生成しました")
            return True

        except Exception as e:
            print(f"✗ エラー: {e}（試行 {attempt+1}/{retry}）")
            if attempt < retry - 1:
                time.sleep(2)
            continue

    return False

# 使用例
if __name__ == "__main__":
    success = generate_image(
        prompt="宇宙を飛ぶ犬のイラスト",
        output_path="img/dog-in-space.png"
    )

    if not success:
        print("✗ 画像生成に失敗しました")
```

---

## レスポンス構造の理解

### 典型的なレスポンス構造

```python
response = model.generate_content("犬のイラスト")

# レスポンスの構造:
response.candidates[0].content.parts = [
    Part(text="画像を生成しました"),      # parts[0]: テキスト応答
    Part(inline_data=InlineData(...)),    # parts[1]: 画像データ
]

# または:
response.candidates[0].content.parts = [
    Part(inline_data=InlineData(...)),    # parts[0]: 画像データのみ
]
```

### 重要なポイント

1. **partsの順序は不定**: parts[0]に画像があるとは限らない
2. **データ形式は可変**: `bytes` または `base64エンコード文字列`
3. **テキストと画像の混在**: 画像の前後にテキストパートが含まれることがある

---

## エラーハンドリング

### よくあるエラー

#### 1. `AttributeError: 'Part' object has no attribute 'inline_data'`

**原因**: 画像データがないpartにアクセス

**対処**:
```python
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        # このpartに画像データがある
```

#### 2. `429 Resource exhausted`

**原因**: APIクォータ超過

**対処**:
- Google AI Studioで有料プランに切り替え
- レート制限を守る（リクエスト間に1.5秒待機）

#### 3. `PIL.UnidentifiedImageError: cannot identify image file`

**原因**: データ形式の誤判定

**対処**:
```python
if isinstance(data, bytes):
    image_bytes = data
else:
    image_bytes = base64.b64decode(data)
```

---

## レート制限とベストプラクティス

### レート制限
- **推奨**: リクエスト間に1.5秒の待機
- **理由**: APIサーバーへの負荷軽減、429エラー回避

### 実装例
```python
import time

for i, prompt in enumerate(prompts):
    generate_image(prompt, f"img/image-{i}.png")
    if i < len(prompts) - 1:
        time.sleep(1.5)  # 次のリクエストまで待機
```

### バッチ処理
- ❌ **Batch API**: 画像生成モデルは非対応
- ✅ **標準リクエスト**: ループで順次実行

---

## コスト見積もり

### 料金体系（2025年10月時点）
- **標準リクエスト**: 約$0.039/画像
- **無料プラン**: 不十分（50-100画像で枯渇）
- **有料プラン**: 必須（大規模プロジェクト）

### 見積もり計算
```python
def estimate_cost(image_count: int, price_per_image: float = 0.039) -> float:
    return image_count * price_per_image

print(f"160枚: ${estimate_cost(160):.2f}")  # 出力: 160枚: $6.24
```

---

## まとめ

### 必須の実装ポイント
1. ✅ 全partsをループして inline_data を探す
2. ✅ データ形式を判定（bytes vs base64）
3. ✅ エラーハンドリングとリトライロジック
4. ✅ レート制限の遵守（1.5秒待機）
5. ✅ 有料プランの使用（大規模プロジェクト）

### 避けるべき実装
- ❌ parts[0]への直接アクセス
- ❌ base64デコード決め打ち
- ❌ エラー時のリトライなし
- ❌ 無料プランでの大量生成

---

## 参考リンク
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [本プロジェクトの実装例](generate_images.py)
