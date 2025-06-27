import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

def generate_daily_report():
    """Generate and send daily performance report"""
    try:
        # Get data from sheet
        sheet = get_sheet()
        records = sheet.get_all_records()
        
        # Calculate metrics
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        daily_leads = sum(1 for r in records if r['Timestamp'].startswith(today))
        bookings = sum(1 for r in records if "book" in r['Message'].lower())
        
        # Generate HTML report
        html_content = f"""
        <html>
        <body>
            <h2>📊 Daily AI Booking Report</h2>
            <p>Date: {today}</p>
            <table border="1">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Leads Processed</td><td>{len(records)}</td></tr>
                <tr><td>Today's Leads</td><td>{daily_leads}</td></tr>
                <tr><td>Bookings Made</td><td>{bookings}</td></tr>
                <tr><td>Estimated Revenue</td><td>${bookings * 2500}</td></tr>
            </table>
        </body>
        </html>
        """
        
        # Send email
        send_email("Daily AI Booking Report", html_content)
        return True
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

def get_sheet():
    """Access Google Sheet"""
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        config.GOOGLE_CREDS_JSON, 
        ['https://www.googleapis.com/auth/spreadsheets']
    )
    gc = gspread.authorize(creds)
    return gc.open(config.SPREADSHEET_NAME).sheet1

def send_email(subject, html_content):
    """Send email with report"""
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = config.EMAIL_USER
    msg['To'] = config.CLIENT_EMAIL
    
    msg.attach(MIMEText(html_content, "html"))
    
    with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_USER, config.CLIENT_EMAIL, msg.as_string())
