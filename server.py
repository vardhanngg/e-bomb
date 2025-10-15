from flask import Flask
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
import os

app = Flask(__name__)

# Load from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

def send_email(to_email, subject, message):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return "Error: SENDER_EMAIL and SENDER_PASSWORD env vars not set"
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        return "Sent"
    except Exception as e:
        print(f"Email send error: {e}")
        return f"Error: {str(e)}"

@app.route('/bomb/<path:to>/<path:sub>/<path:msg>', methods=['GET'])
def bomb(to, sub, msg):
    to = urllib.parse.unquote(to)
    sub = urllib.parse.unquote(sub)
    msg = urllib.parse.unquote(msg)
    result = send_email(to, sub, msg)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
