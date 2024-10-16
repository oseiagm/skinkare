import streamlit as st
import requests
import json
from PIL import Image
import io
import base64
from datetime import datetime
import numpy as np

def encode_image_to_base64(image):
    # Convert PIL Image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def is_skin_image(image):
    """
    Check if the image is likely to be a skin image based on color.
    """
    # Ensure image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Calculate the average color
    avg_color = np.mean(img_array, axis=(0, 1))
    
    # Define a range of skin-like colors in RGB
    skin_lower = np.array([120, 80, 60])  # Adjust these values as needed
    skin_upper = np.array([240, 200, 180])  # Adjust these values as needed
    
    # Check if the average color falls within the skin color range
    return np.all(avg_color >= skin_lower) and np.all(avg_color <= skin_upper)

def analyze_skin_condition(image):
    """Analyze skin condition using OpenRouter API"""
    try:
        # Convert image to base64
        image_base64 = encode_image_to_base64(image)
        
        # Prepare the prompt
        prompt = """You are a professional dermatologist and a skin care specialist.
        Analyze this skin image and provide:
        1. A possible condition description
        2. Common remedies or treatments

        What skin condition do you observe in this image?
        Structure your response in a single detailed paragraph.
        """

        # Prepare the API request
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
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
        return analysis
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {str(e)}")
        if response := getattr(e, 'response', None):
            st.error(f"API Response: {response.text}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def check_configuration():
    """Check if all necessary configurations are in place"""
    try:
        _ = st.secrets["OPENROUTER_API_KEY"]
        return True
    except KeyError:
        st.error("""
        ## Configuration Error
        The application is not configured correctly.
        """)
        return False

def main():
    
    st.set_page_config(layout="wide")
    st.subheader("🔍 Skin Condition Analyzer")
    
    if not check_configuration():
        return
    
    st.markdown("""
        Upload a photo of your skin condition for analysis.
        Please ensure the image is clear and well-lit for the best results.
        
        ⚠️ **Disclaimer**: This tool is for educational purposes only and should not replace professional medical advice.
    """)
    
    # Initialize session state for history
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    col1, col2 = st.columns(2)
    
    if uploaded_file is not None:
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
            if st.button("Analyze Image"):
                with st.spinner('Analyzing image...'):
                    if is_skin_image(image):
                        # Get analysis from OpenRouter
                        analysis_result = analyze_skin_condition(image)
                        
                        if analysis_result:
                            # Save to history
                            st.session_state.analysis_history.append({
                                'timestamp': datetime.now(),
                                'image': image,
                                'analysis': analysis_result
                            })
                            
                            with col2:
                                st.subheader("Analysis Results")
                                st.markdown(analysis_result)
                    else:
                        with col2:
                            st.subheader("Image Validation")
                            st.warning("The uploaded image doesn't appear to be a skin image. Please upload a clear image of the skin condition you want to analyze.")
    
    # Display history
    if st.session_state.analysis_history:
        st.markdown("---")
        st.subheader("Previous Analyses")
        for idx, analysis in enumerate(reversed(st.session_state.analysis_history)):
            with st.expander(f"Analysis {len(st.session_state.analysis_history) - idx}"):
                col3, col4 = st.columns(2)
                with col3:
                    st.image(analysis['image'], use_column_width=True)
                with col4:
                    st.write(f"Timestamp: {analysis['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown(analysis['analysis'])

if __name__ == "__main__":
    main()