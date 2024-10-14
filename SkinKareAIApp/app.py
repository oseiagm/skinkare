from flask import Flask, request, jsonify, render_template, redirect
import base64
import requests
from PIL import Image
import io
import os
from config import Config
from datetime import datetime
import sqlite3

from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
app.config.from_object('config.Config')  


def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def call_openrouter_api(image_base64, prompt):
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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# Function to save analysis in the database
def save_analysis(diagnosis, treatment, date):
    conn = sqlite3.connect('skin_kare.db')
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO analyses (diagnosis, treatment, date) VALUES (?, ?, ?)',
        (diagnosis, treatment, date)
    )
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    conn = sqlite3.connect('skin_kare.db')
    cursor = conn.cursor()

    cursor.execute('SELECT diagnosis, treatment, date FROM analyses')
    analyses = cursor.fetchall()
    conn.close()

    return render_template('historyPage.html', analyses=analyses)

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    file = request.files['image']
    image = Image.open(file)

   
    image_base64 = encode_image_to_base64(image)

    
    prompt = """You are a professional dermatologist and a skin care specialist.
    Analyze this skin image and provide:
    1. The name of the skin condition
    2. A possible condition description
    3. Common remedies or treatments

    What skin condition do you observe in this image?
    Structure your response in a single detailed paragraph that's suitable for Text-to-Speech conversion.
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

if __name__ == "__main__":
    app.run(debug=True)
