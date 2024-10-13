import os

class Config:
    """Configuration class for Flask app."""
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')  # You can set a default key for local testing

# You can also add more configuration options as needed
