from dotenv import load_dotenv
import os
import pickle
import time
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

# Configuration
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.pickle'
PROCESSED_IDS_FILE = 'processed_ids.pickle'
POLL_INTERVAL = 10  # Check every 10 seconds
MAX_RESULTS = 10  # Max emails to check per poll

def get_gmail_service():
    """Initialize and return Gmail API service"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def load_processed_ids():
    """Load set of already processed email IDs"""
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE, 'rb') as f:
            return set(pickle.load(f))
    return set()

def save_processed_ids(email_ids):
    """Save processed email IDs to file"""
    with open(PROCESSED_IDS_FILE, 'wb') as f:
        pickle.dump(list(email_ids), f)

def get_email_details(service, msg_id):
    """Get details for a specific email"""
    msg = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='metadata'
    ).execute()
    
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    return {
        'id': msg_id,
        'subject': headers.get('Subject', 'No Subject'),
        'sender': headers.get('From', 'Unknown Sender'),
        'date': headers.get('Date', 'Unknown Date'),
        'snippet': msg.get('snippet', 'No content')
    }

def main():
    """Main monitoring function"""
    service = get_gmail_service()
    processed_ids = load_processed_ids()
    print("Gmail notifier started. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Check for new emails
            result = service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=MAX_RESULTS,
                q='is:unread'
            ).execute()
            
            new_emails = []
            for msg in result.get('messages', []):
                if msg['id'] not in processed_ids:
                    email = get_email_details(service, msg['id'])
                    new_emails.append(email)
                    processed_ids.add(msg['id'])
            
            # Display new emails
            if new_emails:
                print(f"\nFound {len(new_emails)} new emails:")
                for email in new_emails:
                    print("\n--- New Email ---")
                    print(f"From: {email['sender']}")
                    print(f"Date: {email['date']}")
                    print(f"Subject: {email['subject']}")
                    print(f"Preview: {email['snippet']}")
                
                # Update processed IDs
                save_processed_ids(processed_ids)
            
            time.sleep(POLL_INTERVAL)
    
    except KeyboardInterrupt:
        print("\nStopping notifier...")
        save_processed_ids(processed_ids)

if __name__ == '__main__':
    main()