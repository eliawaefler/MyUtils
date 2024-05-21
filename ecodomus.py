import os

import requests

# Replace '<YOUR_CLIENT_ID>' and '<YOUR_CLIENT_SECRET>' with your actual credentials
CLIENT_ID = 'Siemens.Advanta'
CLIENT_SECRET = os.environ["SIEMENS_API_KEY"]

# Define the URL and the payload
url = 'https://siemens-bt-015.eu.auth0.com/oauth/token'
payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "cient_name": "si_ch_be_3010_bern_inselspital_bb12_test",
    "audience": "https://horizon.siemens.com",
    "grant_type": "client_credentials"
}

# Set header for the request
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Token received successfully")
    print(response.json())  # This will print the token and other returned info
else:
    print(f"Failed to retrieve token. Status code: {response.status_code}")
    print(response.text)  # This will print error message if any
