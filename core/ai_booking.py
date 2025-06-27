import os
import datetime
from twilio.rest import Client
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

# Initialize clients
twilio_client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
openai_client = OpenAI(api_key=config.OPENAI_KEY)

def handle_sms(from_number, message):
    """Process incoming SMS messages"""
    # Log interaction
    log_interaction(from_number, message)
    
    # Generate AI response
    ai_response = generate_ai_response(message)
    
    # Send response
    send_sms(from_number, ai_response)
    
    # Check for booking keywords
    if "book" in message.lower() or "schedule" in message.lower():
        process_booking(from_number, message)

def generate_ai_response(message):
    """Generate AI response using OpenAI"""
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": config.AI_SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def process_booking(phone, message):
    """Process booking requests"""
    # Extract details using AI
    booking_details = extract_booking_details(message)
    
    # Save to Google Sheets
    save_to_sheet(phone, booking_details)
    
    # Alert agent if high-value
    if booking_details.get('priority', 0) > 7:
        alert_agent(phone, booking_details)

def log_interaction(phone, message):
    """Log interaction to Google Sheets"""
    try:
        sheet = get_sheet()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, phone, message])
    except Exception as e:
        print(f"Error logging interaction: {e}")

def get_sheet():
    """Access Google Sheet"""
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        config.GOOGLE_CREDS_JSON, 
        ['https://www.googleapis.com/auth/spreadsheets']
    )
    gc = gspread.authorize(creds)
    return gc.open(config.SPREADSHEET_NAME).sheet1

# Additional helper functions would go here...
