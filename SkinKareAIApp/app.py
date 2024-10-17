from flask import Flask, request, jsonify, render_template, redirect
import base64
import requests
from PIL import Image
import io
import os
import numpy as np
from datetime import datetime
import sqlite3

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def is_skin_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    img_array = np.array(image)
    avg_color = np.mean(img_array, axis=(0, 1))
    skin_lower = np.array([120, 80, 60])
    skin_upper = np.array([240, 200, 180])
    return np.all(avg_color >= skin_lower) and np.all(avg_color <= skin_upper)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def result():
    return render_template('results.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' in request.files:
        file = request.files['image']
        image = Image.open(file)
    else:
        # Decode image from base64 string sent from JavaScript
        img_data = request.form.get('image_base64').split(",")[1]
        image = Image.open(io.BytesIO(base64.b64decode(img_data)))

    if not is_skin_image(image):
        return jsonify({"error": "The uploaded image is not a skin image."}), 400

    image_base64 = encode_image_to_base64(image)

    prompt = """
    You are a professional dermatologist. Analyze this skin image and provide:
    1. The name of the skin condition
    2. A description
    3. Suggested remedies or treatments
    """

    result = call_openrouter_api(image_base64, prompt)
    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    analysis = result['choices'][0]['message']['content']
    condition_name = analysis.split('.')[0]
    treatment = "Moisturizers and corticosteroid creams"  
    date = datetime.now().strftime('%m/%d/%Y')

    save_analysis(condition_name, treatment, date)

    response_data = {
        "condition": condition_name,
        "analysis": analysis,
        "imageBase64": image_base64
    }

    return jsonify(response_data)

def call_openrouter_api(image_base64, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}", "Content-Type": "application/json"}
    payload = {
        "model": "meta-llama/llama-3.2-11b-vision-instruct:free",
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": image_base64}}]}]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def save_analysis(diagnosis, treatment, date):
    conn = sqlite3.connect('skin_kare.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO analyses (diagnosis, treatment, date) VALUES (?, ?, ?)', (diagnosis, treatment, date))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
