#!/usr/bin/env python3
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow

def authenticate():
    print(google_auth_oauthlib.flow.__file__)
    SCOPES = ['https://www.googleapis.com/auth/youtube']

    CLIENT_SECRET_FILE = 'client_secrets.json'
    TOKEN_PATH = 'token.json'

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_console()
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

    return creds

def main():
    creds = authenticate()
    youtube = build('youtube', 'v3', credentials=creds)

if __name__ == '__main__':
    main()
