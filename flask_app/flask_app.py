from flask import Flask, request, jsonify
import base64
import requests
from PIL import Image
import io
import os

app = Flask(__name__)

# Function to encode image to base64
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

@app.route('/analyze', methods=['POST'])
def analyze_image():
    file = request.files['image']
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

    # Prepare the API request to OpenRouter
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",  # Use your OpenRouter API key
            },
            json={
                "model": "meta-llama/llama-3.2-11b-vision-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_base64
                                }
                            }
                        ]
                    }
                ]
            }
        )

        # Check if the request was successful
        response.raise_for_status()

        # Parse the response
        result = response.json()

        # Extract the analysis from the response
        analysis = result['choices'][0]['message']['content']
        
        # Create a response dictionary
        response_data = {
            "condition": "Skin Condition Observed",  # You can adjust this based on the analysis content
            "analysis": analysis,
            "imageBase64": image_base64
        }
        return jsonify(response_data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API Request Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
