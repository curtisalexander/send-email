#!/usr/bin/env python

# from https://docs.python.org/3/library/email-examples.html

# standard lib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import click
import smtplib
import yaml

@click.command()
@click.option('--config', required=True, type=click.Path(), help='file path to yaml configuration file')

def main(config):
    with open(config, 'r') as f:
        email_yaml = yaml.load(f)

    send_email(email_yaml['sender'],
               email_yaml['recipient'],
               email_yaml['subject'],
               email_yaml['msg_text'],
               email_yaml['email_server'])


def create_email(sender,
                 recipient_addresses,
                 subject,
                 priority,
                 ms_priority,
                 msg_text,
                 msg_html):
    """
    Create a mail message with text and html formats
    """

    # Message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['X-Priority'] = priority
    msg['X-MSMail-Priority'] = ms_priority
    msg['From'] = sender
    msg['To'] = ', '.join([formataddr(r) for r in recipient_addresses])

    # Record the MIME types of both parts - text/plain and text/html
    part1 = MIMEText(msg_text, 'plain')
    part2 = MIMEText(msg_html, 'html')

    # Attach parts into message container
    # According to RFC 2046, the last part of a multipart message
    #   is preferred
    msg.attach(part1)
    msg.attach(part2)

    return msg

def send_email(sender,
               recipient,
               subject,
               msg_text,
               email_server):
    """
    Send a mail message with text and html formats
    """

    # Sender
    sender_send = formataddr((sender['pretty_name'], sender['email_address']))

    # Recipient addresses
    recipients = zip(recipient['pretty_name'], recipient['email_address'])
    recipient_header = [x for x in recipients]
    
    # To send to the recipient, only need the username@domain.com entry
    recipient_send = [address[1] for address in recipient_header]

    # Priority 
    priority = '3'
    ms_priority = 'Normal'

    # Create the body as HTML
    msg_html = """\
    <html>
        <head>
            <style>
                mark {{
                    background-color: lightgray;
                    color: black;
                }}
                body {{
                    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif
                }}
            </style>
        </head>
        <body>
            <p>{_msg_text}</p>
        </body>
    </html>
    """.format(_msg_text = msg_text)

    # Create email msg
    msg = create_email(sender_send,
                       recipient_header,
                       subject, priority,
                       ms_priority,
                       msg_text,
                       msg_html)

    # Send email
    s = smtplib.SMTP(email_server)
    try:
        s.sendmail(sender_send, recipient_send, msg.as_string())
    finally:
        s.quit()

if __name__ == '__main__':
    main()
