# Import necessary modules
from __future__ import print_function
import base64
import os.path

# Google auth related imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the email addresses to search for as a constant at the top
EMAIL_ADDRESSES = ["orders@eat.grubhub.com", "orders@doordash.com", "orders@ubereats.com"]

# Gmail API scope. Modify this and delete 'token.json' if scope changes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_user_creds():
    """Returns user credentials for the Gmail API. 
    If no credentials are available, it will guide the user to log in."""

    creds = None
    if os.path.exists('token.json'):  # Check if 'token.json' exists which holds the user credentials
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
    """Fetches the most recent order from specified email addresses. 
    Returns a dictionary with the subject, sender, and body of the message."""

    creds = get_user_creds()  # Get user credentials

    try:
        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=creds)

        # Create the query to get emails from the specified email addresses
        query = " OR ".join(f"from:{email}" for email in EMAIL_ADDRESSES)

        # List all the emails matching the query
        results = service.users().messages().list(userId='me', q=query).execute()

        messages = results.get('messages', [])
        if not messages:
            return None
        else:
            # Get the most recent email
            message = messages[0]
            # Fetch the message using the API
            msg = service.users().messages().get(userId='me', id=message['id']).execute() 
            payload = msg['payload']
            headers = payload['headers']

            subject = ""
            sender = ""
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'Date':
                    date = d['value']
            
            body = payload.get('body', {}).get('data')
            text = base64.urlsafe_b64decode(body).decode() if body else None

            message_dict = {'subject':subject, 'sender':sender, 'date':date, 'body':text}
            return message_dict
    
    except HttpError as error:
        print(f'An error occurred: {error}')  # TODO: Handle errors properly
