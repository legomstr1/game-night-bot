from __future__ import print_function
import base64
import re
import os.path
import order_parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        # Get the list of all emails
        results = service.users().messages().list(userId='me', q="from:orders@eat.grubhub.com").execute()
        messages = results.get('messages', [])

        if not messages:
            print('No new emails.')
        else:
            print('Emails:')
            message = messages[0]  # Get the first (most recent) email
            msg = service.users().messages().get(userId='me', id=message['id']).execute()  # Fetch the message using the API
            payload = msg['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            print('Latest email from github.com')
            print('Subject: ', subject)
            print('Sender: ', sender)

            body = payload.get('body', {}).get('data')
            if body is not None:
                text = base64.urlsafe_b64decode(body).decode()
                #print('Message: ', text)
            else:
                print("No body in the email's payload.")
            print()
            print()
            order_parser.parse_order(text)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()