from flask import Flask, request
from core.ai_booking import handle_sms
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "AI Booking Agency is running!"

@app.route('/sms', methods=['POST'])
def sms_handler():
    from_number = request.form.get('From')
    message_body = request.form.get('Body')
    
    if not from_number or not message_body:
        return "Invalid request", 400
        
    handle_sms(from_number, message_body)
    return "", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
