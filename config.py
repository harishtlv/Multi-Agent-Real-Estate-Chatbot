# config.py - Configuration settings

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys (set these in your .env file)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")
    AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
    AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
    
    # App settings
    APP_NAME = "Multi-Agent Real Estate Assistant"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Image processing limits
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_IMAGE_DIMENSIONS = (2048, 2048)
    SUPPORTED_IMAGE_FORMATS = ['PNG', 'JPEG', 'JPG', 'GIF', 'BMP']
    
    # Agent settings
    AGENT_CONFIDENCE_THRESHOLD = 0.6
    MAX_RESPONSE_LENGTH = 2000
    CONVERSATION_HISTORY_LIMIT = 50
    
    # AI Model settings
    OPENAI_MODEL = "gpt-4-vision-preview"
    OPENAI_MAX_TOKENS = 1500
    OPENAI_TEMPERATURE = 0.7
    
    # Database settings (for future use)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///real_estate_bot.db")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "logs/app.log"
    
    @classmethod
    def validate_config(cls):
        """Validate essential configuration"""
        required_keys = ["OPENAI_API_KEY"]
        missing_keys = [key for key in required_keys if not getattr(cls, key)]
        
        if missing_keys:
            raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")
        
        return True

# =========================================
# .env.example - Environment variables template

# Copy this file to .env and fill in your actual API keys

# OpenAI API Key (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Google Vision API Key (Optional - for enhanced image analysis)
GOOGLE_VISION_API_KEY=your_google_vision_api_key_here

# Azure Cognitive Services (Optional - for enhanced image analysis)
AZURE_VISION_KEY=your_azure_vision_key_here
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint_here

# Application settings
DEBUG=False
LOG_LEVEL=INFO

# Database (for future persistence features)
DATABASE_URL=sqlite:///real_estate_bot.db

# =========================================
# setup.py - Package installation script

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="multi-agent-real-estate-chatbot",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Multi-Agent Real Estate Chatbot with Image Analysis and Tenancy Guidance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/multi-agent-real-estate-chatbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "pytest-cov>=4.1.0",
        ],
        "cloud": [
            "google-cloud-vision>=3.4.5",
            "azure-cognitiveservices-vision-computervision>=0.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "real-estate-bot=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
)

# =========================================
# run.py - Application runner script

import streamlit as st
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import configuration
from config import Config

def main():
    """Main application runner"""
    
    try:
        # Validate configuration
        Config.validate_config()
        
        # Set page config
        st.set_page_config(
            page_title=Config.APP_NAME,
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Import and run the main app
        from main import RealEstateChatbotApp
        
        app = RealEstateChatbotApp()
        app.run()
        
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please check your .env file and ensure all required API keys are set.")
        
    except ImportError as e:
        st.error(f"Import Error: {e}")
        st.info("Please ensure all required packages are installed: `pip install -r requirements.txt`")
        
    except Exception as e:
        st.error(f"Application Error: {e}")
        if Config.DEBUG:
            st.exception(e)

if __name__ == "__main__":
    main()

# =========================================
# Dockerfile - For containerized deployment

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "run.py", "--server.port=8501", "--server.address=0.0.0.0"]

# =========================================
# docker-compose.yml - For local development

version: '3.8'

services:
  real-estate-bot:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GOOGLE_VISION_API_KEY=${GOOGLE_VISION_API_KEY}
      - AZURE_VISION_KEY=${AZURE_VISION_KEY}
      - AZURE_VISION_ENDPOINT=${AZURE_VISION_ENDPOINT}
      - DEBUG=True
    volumes:
      - ./logs:/app/logs
      - ./.env:/app/.env
    restart: unless-stopped
    
  # Future: Add database service
  # postgres:
  #   image: postgres:15
  #   environment:
  #     POSTGRES_DB: real_estate_bot
  #     POSTGRES_USER: bot_user
  #     POSTGRES_PASSWORD: bot_password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

# volumes:
#   postgres_data:

# =========================================
# .gitignore - Git ignore file

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# Streamlit
.streamlit/secrets.toml

# Images (uploaded by users during testing)
uploads/
temp_images/

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Documentation
docs/_build/