import requests
import json
import datetime
import base64
import os

# Zoom OAuth credentials
CLIENT_ID = 'TCIPe9UJSQiwCGSFU7vEzg'
CLIENT_SECRET = 'i55SqNTDdwVeSmKDeDqCciE2sEoEluiI'
REDIRECT_URI = 'https://go.pixeltests.com/'

TOKEN_FILE = 'zoom_tokens.json'

# Helper function to load tokens from a file
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    return {}

# Helper function to save tokens to a file
def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)

# Step 1: Get Authorization URL
def get_authorization_url():
    auth_url = (
        f"https://zoom.us/oauth/authorize?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return auth_url

# Step 2: Exchange Authorization Code for Access Token
def get_access_token(authorization_code):
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response_data = response.json()
    if 'access_token' in response_data:
        save_tokens(response_data)
    return response_data.get("access_token")

# Step 3: Refresh Access Token
def refresh_access_token(refresh_token):
    token_url = "https://zoom.us/oauth/token"
    headers = {
        "Authorization": f"Basic {base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response_data = response.json()
    if 'access_token' in response_data:
        save_tokens(response_data)
    return response_data.get("access_token")

# Step 4: Schedule a Webinar
def schedule_webinar(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    webinar_details = {
        "topic": "Automated Webinar",
        "type": 5,  # Scheduled Webinar
        "start_time": "2024-06-01T10:00:00Z",  # Webinar start time in ISO 8601 format
        "duration": 60,  # Duration in minutes
        "timezone": "UTC",
        "agenda": "This is an automated webinar",
        "settings": {
            "host_video": True,
            "panelists_video": True,
            "practice_session": True,
            "hd_video": True,
            "approval_type": 0,  # Automatically approve
            "registration_type": 1,  # Attendees register once and can attend any of the occurrences
            "audio": "both",  # Both telephony and VoIP
            "auto_recording": "cloud"
        }
    }
    
    user_id = 'me'  # Use 'me' for the authenticated user, or replace with a specific user ID
    response = requests.post(f'https://api.zoom.us/v2/users/{user_id}/webinars', headers=headers, json=webinar_details)
    
    if response.status_code == 201:
        print("Webinar scheduled successfully!")
        print("Webinar details:", response.json())
    else:
        print("Failed to schedule webinar.")
        print("Response:", response.json())

# Main flow
if __name__ == "__main__":
    tokens = load_tokens()
    
    if 'access_token' in tokens and 'refresh_token' in tokens:
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        
        # Check if the access token is expired and refresh it if necessary
        try:
            schedule_webinar(access_token)
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 401:  # Unauthorized, likely due to expired token
                access_token = refresh_access_token(refresh_token)
                if access_token:
                    schedule_webinar(access_token)
                else:
                    print("Failed to refresh access token.")
    else:
        print("Go to the following URL to authorize the app:")
        print(get_authorization_url())
        
        # After user authorizes the app, they will be redirected to your redirect URI with a code parameter
        authorization_code = input("Enter the authorization code: ")
        
        # Get access token using the authorization code
        access_token = get_access_token(authorization_code)
        
        if access_token:
            schedule_webinar(access_token)
        else:
            print("Failed to obtain access token.")
