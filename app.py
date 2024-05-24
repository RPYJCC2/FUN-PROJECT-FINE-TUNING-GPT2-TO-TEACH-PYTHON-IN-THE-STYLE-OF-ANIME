from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template, Response
import requests
from io import BytesIO
from transformers import pipeline

# Load the API token from the .env file
load_dotenv()
api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# Set the full Hugging Face model identifier
model_identifier = 'btbeck/animegirlteachesyoucs'  # Correct path to your model
api_url = f"https://api-inference.huggingface.co/models/{model_identifier}"

# Define headers including the Authorization token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Set the full Hugging Face model identifier
tts_model_identifier = 'suno/bark-small'

# Initialize the translation pipeline
#translation_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-en-jap")


def chat(input_text):
    prompt = (
        "You are an anime school girl named Yumi.\n"
        "You love teaching about python the coding language.\n"
        "You say UWU and use Japanese a lot.\n"
        "Now, please answer the question: {input_text}Yumi:"
        ).format(input_text=input_text)

    data = {
        "inputs": prompt,
        "parameters": {
            "max_length": 50
        }
    }

    # Make a POST request to the API
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text']
            if 'Yumi:' in generated_text:
                generated_text = generated_text.split('Yumi:', 1)[1].strip()
            return generated_text
        else:
            return "Unexpected response format from the model."
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

#def translate_text(text, target_language="ja"):
#    translation = translation_pipeline(text)
#    return translation[0]['translation_text']
headers2 = {"Authorization": f"Bearer {api_token}"}
def generate_audio_bark(text):
    try:
        api_url2 = f"https://api-inference.huggingface.co/models/{tts_model_identifier}"
        headers2 = {"Authorization": f"Bearer {api_token}"}
        payload = {"inputs": text}

        response = requests.post(api_url2, headers=headers2, json=payload)
        response.raise_for_status()

        audio_content = response.content
        
        audio_stream = BytesIO(audio_content)
        audio_stream.seek(0)

        print(f"Audio Stream: {audio_stream.getvalue()[:100]}...")  # Print first 100 bytes of the audio stream for debug

        return audio_stream
    except Exception as e:
        print(f"Error during audio generation: {e}")
        return None
    


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    user_input = request.json.get("input")
    text_response = chat(user_input)
    
    # Translate text response to Japanese
    #translated_text = translate_text(text_response)
    
    return jsonify({"response": text_response, "audio_text": text_response})

@app.route("/audio")
def audio():
    user_input = request.args.get("input")
    audio_io = generate_audio_bark(user_input)
    if audio_io is None:
        return "Audio generation failed", 500
    return Response(audio_io, mimetype="audio/flac")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
