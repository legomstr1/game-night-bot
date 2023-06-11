from __future__ import print_function
import base64
import re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Constants
EMAIL_ADRESSES = ["orders@eat.grubhub.com", "orders@doordash.com", "orders@ubereats.com"]

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_user_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_order():
    creds = get_user_creds()
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        # Get the list of all emails
        query = " OR ".join(f"from:{email}" for email in EMAIL_ADRESSES)
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        if not messages:
            return None
        else:
            message = messages[2]  # Get the first (most recent) email
            msg = service.users().messages().get(userId='me', id=message['id']).execute()  # Fetch the message using the API
            payload = msg['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
            
            body = payload.get('body', {}).get('data')
            if body is not None:
                text = base64.urlsafe_b64decode(body).decode()
            else:
                text = None

            message_dict = {'subject':subject, 'sender':sender, 'body':text}
            return message_dict
    
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')