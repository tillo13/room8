import os
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv()

# Retrieve Gmail credentials from environment variables
GMAIL_USER = os.environ.get('ROOM8_GMAIL_USERNAME')
GMAIL_PASSWORD = os.environ.get('ROOM8_GMAIL_APP_PASSWORD')

# Function to send plain text emails
def send_email(subject, body, to_emails, attachment_paths=None):
    # Setup email headers and recipients
    message = MIMEMultipart()
    message['From'] = 'Room8 <{}>'.format(GMAIL_USER)
    message['To'] = ', '.join(to_emails)
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Process attachments if provided
    if attachment_paths:
        for attachment_path in attachment_paths:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=os.path.basename(attachment_path)
            )
            message.attach(part)

    # Connect to Gmail SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.set_debuglevel(0)  # change to 1 to see SMTP debug output
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(message)
        print('Email sent successfully')

# Function to send HTML emails
def send_html_email(subject, html_body, to_emails, attachment_paths=None, bcc_emails=None):
    """
    Sends an HTML email to the specified recipients.

    :param subject: Email subject.
    :param html_body: HTML content of the email.
    :param to_emails: List of recipient email addresses.
    :param attachment_paths: List of file paths for attachments.
    :param bcc_emails: List of BCC email addresses.
    """
    message = MIMEMultipart("alternative")
    message['From'] = 'Room8 <{}>'.format(GMAIL_USER)
    message['To'] = ', '.join(to_emails)
    message['Subject'] = subject

    # Attach HTML body
    message.attach(MIMEText(html_body, 'html'))
    
    # Process attachments if provided
    if attachment_paths:
        for attachment_path in attachment_paths:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=os.path.basename(attachment_path)
            )
            message.attach(part)

    # Combine recipients and optionally BCC emails
    all_recipients = to_emails + (bcc_emails if bcc_emails else [])

    # Connect to Gmail SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.set_debuglevel(0)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(message, to_addrs=all_recipients)
        print('HTML Email sent successfully')

# Function to create a sample text file with provided content
def create_sample_text_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Created file {filename} with content: {content}")

# Function to reply to an email (for demonstration purposes)
def reply_to_email(original_email, body):
    reply = MIMEMultipart()
    reply['From'] = 'Room8 <{}>'.format(GMAIL_USER)
    reply['To'] = original_email['From']
    reply['Subject'] = 'Re: ' + original_email['Subject']
    reply['In-Reply-To'] = original_email['Message-ID']
    reply['References'] = original_email['Message-ID']
    reply.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(reply)
        print(f'Replied to {original_email["From"]} with subject "{reply["Subject"]}"')

# Function to read emails from the inbox
def read_emails():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    emails = []
    for email_id in email_ids:
        result, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        msg = email.message_from_bytes(raw_email)
        emails.append(msg)

    mail.logout()
    return emails

# Test the functionalities (for development testing purposes only)
if __name__ == '__main__':
    # Create a sample text file
    filename = 'sample.txt'
    content = 'hello_world'
    create_sample_text_file(filename, content)

    # Sample usage: sending a test email with attachment
    subject = 'Test Email with Attachment from Room8'
    body = 'This email contains an attachment sent from the Room8 email utility.'
    to_emails = ['andytillo@gmail.com']  # replace with desired test recipient

    attachment_path = os.path.join(os.getcwd(), filename)
    send_email(subject, body, to_emails, [attachment_path])