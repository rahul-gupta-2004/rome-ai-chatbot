from dotenv import load_dotenv
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Configuration
CLIENT_SECRET_FILE = 'client_secret.json'  # You'll need to get this from Google Cloud Console
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.json'

def get_gmail_service():
    """Initialize and return Gmail API service with send permissions"""
    creds = None
    
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print(f"Message sent with ID: {message['id']}")
        return True
    except HttpError as error:
        print(f"An error occurred while sending email: {error}")
        return False

def main():
    # Get the Gmail service
    service = get_gmail_service()
    
    # Email details from environment variables
    sender_email = os.getenv('ROME_PROJECT_EMAIL')
    recipient_email = "rahul.gupta2223@xaviers.edu.in"
    email_subject = "Test Email from Gmail API"
    email_body = """
    Hello Rahul,

    This is a test email sent using the Gmail API from Python.

    Best regards,
    Rome Project Team
    """
    
    # Create and send the email
    message = create_message(sender_email, recipient_email, email_subject, email_body)
    send_message(service, "me", message)
    print("Email sent successfully!")

if __name__ == '__main__':
    main()