# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("THIS IS A TEST")


# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'TEST'
msg['From'] = 'root@localhost'
msg['To'] = 'root@localhost'

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost', 25)
s.send_message(msg)
print(s.quit())
