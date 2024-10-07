# SkinKare

A web application that analyzes skin conditions using AI vision models through the OpenRouter API. The application provides detailed analysis and maintains a history of previous analyses.

## 🌟 Features

- Upload and analyze skin condition images
- Get AI-powered dermatological analysis
- View analysis history

## 📋 Prerequisites

- Python 3.7+
- OpenRouter API key ([Get it here](https://openrouter.ai/))

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/oseiagm/skinkare.git
cd skinkare
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install streamlit requests Pillow
```

## 🔑 Configuration

1. Create a `.streamlit` directory in your project root:
```bash
mkdir .streamlit
```

2. Create a `secrets.toml` file inside the `.streamlit` directory:
```bash
touch .streamlit/secrets.toml
```

3. Add your OpenRouter API key to `secrets.toml`:
```toml
OPENROUTER_API_KEY = "your_api_key_here"
```

## 🚀 Running the Application

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

## 💡 Usage

1. Upload an image of the skin condition using the file uploader
2. Click the "Analyze Image" button
3. View the analysis results in the right column
4. Previous analyses are stored and can be viewed in the "Previous Analyses" section

## ⚠️ Disclaimer

This application is for educational purposes only and should not replace professional medical advice. Always consult with a healthcare provider for proper diagnosis and treatment of skin conditions.

## 🔒 Security Notes

- Never commit your `secrets.toml` file to version control
- Add `.streamlit/secrets.toml` to your `.gitignore` file
- Keep your API keys confidential

## 🛠️ Dependencies

- `streamlit`: Web application framework
- `requests`: HTTP library for API calls
- `Pillow`: Python Imaging Library for image processing
- `python-base64`: For image encoding
- `datetime`: For timestamp management
