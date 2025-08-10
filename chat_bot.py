from google.auth.transport.requests import Request
from google.oauth2 import service_account
import google.auth.transport.requests
import requests
import json

SERVICE_ACCOUNT_FILE = "api_file.json"

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

auth_req = google.auth.transport.requests.Request()
credentials.refresh(auth_req)
access_token = credentials.token

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

payload = {
    "messages": [
        {"role": "system", "content": "You are ProfAI, an AI professor with emotional intelligence."},
        {"role": "user", "content": "Hello from ProfAI!"}
    ]
}

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateMessage"

response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
print(response.json())





