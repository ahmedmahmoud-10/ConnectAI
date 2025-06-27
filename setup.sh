#!/bin/bash

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please update with your credentials."
fi

# Create Google Sheet if needed
echo "Please create a Google Sheet named 'AI_Booking_System' and share with your service account email"
