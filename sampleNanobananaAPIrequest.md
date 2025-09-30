import google.generativeai as genai
from PIL import Image
from io import BytesIO

genai.configure(api_key="取得したAPIキー")
model = genai.GenerativeModel("gemini-2.5-flash-image-preview")
prompt = "宇宙を飛ぶ犬のイラストを生成してください"
response = model.generate_content(prompt)
# レスポンスから画像データを取り出してファイル保存
image_data = BytesIO(response.candidates[0].content.parts[1].inline_data.data)
Image.open(image_data).save("dog_in_space.png")
