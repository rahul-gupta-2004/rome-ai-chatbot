import os
from dotenv import load_dotenv
from gmail_notifier import get_gmail_service, load_processed_ids, save_processed_ids, get_email_details
from chatbot import STORE_INFO, initialize_model, create_prompt_template, load_faq_data
from send_mail import get_gmail_service as get_send_service, create_message, send_message
import time

# Load environment variables
load_dotenv()

# Configuration
POLL_INTERVAL = 10  # Check every 10 seconds
MAX_RESULTS = 10  # Max emails to check per poll
PROCESSED_IDS_FILE = 'processed_ids.pickle'

# Initialize chatbot components
faq_data = load_faq_data("Ecommerce_FAQ_Chatbot_dataset.json")
llm = initialize_model()
prompt_template = create_prompt_template(faq_data)

def create_email_response(sender_email, original_subject, chatbot_response):
    subject = f"Re: {original_subject}"
    body = f"""Dear Customer,

Thank you for contacting {STORE_INFO['name']}. Here's the response to your inquiry:

{chatbot_response}

Best regards,
{STORE_INFO['name']} Support Team
"""
    return subject, body

def process_email(service, email):
    print(f"\nNew email received from: {email['sender']}")
    print(f"Subject: {email['subject']}")
    
    # Get email content and format as question
    email_content = f"Email Subject: {email['subject']}\n\nEmail Content: {email['snippet']}"
    
    # Get chatbot response
    response = llm.invoke(prompt_template.format(question=email_content))
    
    # Initialize Gmail send service
    send_service = get_send_service()
    
    # Check if response indicates need for human support
    if "Please contact our customer support team for further assistance." in response.content:
        # Forward to support email
        print("Forwarding to support team...")
        support_subject = f"Forwarded: {email['subject']}"
        support_body = f"""This email requires human support attention.

Original From: {email['sender']}
Original Subject: {email['subject']}
Original Content:
{email['snippet']}
"""
        message = create_message(
            os.getenv("ROME_PROJECT_EMAIL"),
            os.getenv("ROME_SUPPORT_EMAIL"),
            support_subject,
            support_body
        )
        send_message(send_service, "me", message)
        print(f"Email forwarded to support team\n")
    else:
        # Send response to original sender
        print("Generating response...")
        subject, body = create_email_response(email['sender'], email['subject'], response.content)
        
        # Extract email address from sender string (might be "Name <email@example.com>")
        sender_email = email['sender'].split('<')[-1].split('>')[0].strip() if '<' in email['sender'] else email['sender']
        
        message = create_message(
            os.getenv("ROME_PROJECT_EMAIL"),
            sender_email,
            subject,
            body
        )
        send_message(send_service, "me", message)
        print(f"Response sent to: {sender_email}\n")

def main():
    # Initialize services
    receive_service = get_gmail_service()  # For reading emails
    processed_ids = load_processed_ids()
    print("Email monitoring service started. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            # Check for new emails
            result = receive_service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=MAX_RESULTS,
                q='is:unread'
            ).execute()
            
            for msg in result.get('messages', []):
                if msg['id'] not in processed_ids:
                    email = get_email_details(receive_service, msg['id'])
                    process_email(receive_service, email)
                    processed_ids.add(msg['id'])
            
            # Save processed IDs periodically
            save_processed_ids(processed_ids)
            time.sleep(POLL_INTERVAL)
    
    except KeyboardInterrupt:
        print("\nStopping email monitoring service...")
        save_processed_ids(processed_ids)

if __name__ == '__main__':
    main()