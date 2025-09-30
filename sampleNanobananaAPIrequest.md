import base64
import google.generativeai as genai
from PIL import Image
from io import BytesIO

genai.configure(api_key="取得したAPIキー")
model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
prompt = "宇宙を飛ぶ犬のイラストを生成してください"
response = model.generate_content(prompt)
# Base64文字列をデコードしてファイル保存
image_bytes = base64.b64decode(response.candidates[0].content.parts[0].inline_data.data)
Image.open(BytesIO(image_bytes)).save("dog_in_space.png")
