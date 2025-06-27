import os
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Twilio Configuration
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')

# OpenAI Configuration
OPENAI_KEY = os.getenv('OPENAI_KEY')
AI_SYSTEM_PROMPT = os.getenv('AI_SYSTEM_PROMPT', "You are a helpful booking assistant. Respond professionally to inquiries.")

# Google Sheets Configuration
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME', "AI_Booking_System")
GOOGLE_CREDS_JSON = json.loads(os.getenv('GOOGLE_CREDS_JSON', '{}'))

# Email Configuration
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
CLIENT_EMAIL = os.getenv('CLIENT_EMAIL')
SMTP_SERVER = os.getenv('SMTP_SERVER', "smtp.gmail.com")
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

# Business Configuration
AGENT_PHONE = os.getenv('AGENT_PHONE')
