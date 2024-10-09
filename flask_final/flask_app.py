from flask import Flask, request, jsonify, render_template
import base64
import requests
from PIL import Image
import io
import os
from config import Config

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

# Load the configuration
app = Flask(__name__)
app.config.from_object('config.Config')  # Load the config from config.py

# Function to encode image to base64
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def call_openrouter_api(image_base64, prompt):
    """Call OpenRouter API to analyze the skin image."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {app.config['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3.2-11b-vision-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_base64}}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for 4xx or 5xx responses
        return response.json()  # Returns JSON response directly
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    file = request.files['image']
    print(file)
    image = Image.open(file)

    # Encode the image to base64
    image_base64 = encode_image_to_base64(image)

    # Prepare the prompt for the OpenRouter API
    prompt = """You are a professional dermatologist and a skin care specialist.
    Analyze this skin image and provide:
    1. A possible condition description
    2. Common remedies or treatments

    What skin condition do you observe in this image?
    Structure your response in a single detailed paragraph that's suitable for Text-to-Speech conversion.
    """

    # Call the OpenRouter API
    result = call_openrouter_api(image_base64, prompt)

    # Process the result and return the response
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    
    # Extract the analysis from the result
    analysis = result['choices'][0]['message']['content']

    # Create a response dictionary
    response_data = {
        "condition": "Skin Condition Observed",  # You can adjust this based on the analysis content
        "analysis": analysis,
        "imageBase64": image_base64
    }
    print(analysis)
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)