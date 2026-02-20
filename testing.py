import google.generativeai as genai

genai.configure(api_key="AIzaSyBUcrxlWOtltFtjT96-WY7iO9pK4DRFBQU")

models = genai.list_models()

for m in models:
    print(m.name)
