# Rome-Restaurants AI Chatbot System

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-00A67E?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rome-ai-chatbot.streamlit.app/)
[![Gmail_API](https://img.shields.io/badge/Gmail_API-EA4335?logo=gmail&logoColor=white)](https://developers.google.com/gmail/api)

An intelligent chatbot system for Rome-Restaurants e-commerce platform, featuring multiple interfaces (CLI, web, and email auto-responder) powered by Google Gemini AI.

## Features

- **Multi-interface Support**:
  - Interactive CLI chatbot
  - [Streamlit web interface](https://rome-ai-chatbot.streamlit.app/) (live deployment)
  - Gmail auto-responder service
- **AI-Powered Responses** using Google Gemini 1.5 Flash
- **FAQ Knowledge Base** integration
- **Automated Email Processing** with intelligent routing
- **Store Information Context** for personalized responses

## Technologies Used

- **Core AI**:
  - Google Gemini API (`gemini-1.5-flash` model)
  - LangChain framework for AI orchestration
- **Backend**:
  - Python 3.9+
  - LangChain (prompt templates, chains)
  - Google APIs (Gmail integration)
- **Web Interface**:
  - Streamlit for chatbot UI
- **Data**:
  - [Ecommerce-FAQ-Chatbot-Dataset](https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset)
  - Store information context
- **Environment**:
  - dotenv for configuration
  - OAuth 2.0 for Gmail API

## Repository Structure
```
rome-restaurants-chatbot/
├── chatbot.py              # Core chatbot logic
├── chatbot_website.py      # Streamlit web interface
├── main.py                 # Email auto-responder
├── send_mail.py            # Email sending service
├── gmail_notifier.py       # Email monitoring service
├── .env.example            # Environment variables template
└── requirements.txt        # Python dependencies
```

## Prerequisites

- Python 3.9+
- Google Gemini API key
- Google Cloud Project with Gmail API enabled
- Gmail account for email services

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/rome-restaurants-chatbot.git
   cd rome-restaurants-chatbot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
3. Set up environment variables:
   - Create `.env` file from `.env.example`
   - Add your Gemini API key and Gmail credentials

## Deployment

A live version of the web interface is available on Streamlit Cloud:

[Try the Rome Restaurant Chatbot Live](https://rome-ai-chatbot.streamlit.app/)

## Usage

1. CLI Chatbot:
   ```
   python chatbot.py
   ```
   
2. Web Interface:
   ```
   streamlit run chatbot_website.py
   ```

3. Email Auto-responder:
   ```
   python main.py
   ```

## Dataset
The system uses the [Ecommerce-FAQ-Chatbot-Dataset](https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset) , enhanced with custom store-specific information.
