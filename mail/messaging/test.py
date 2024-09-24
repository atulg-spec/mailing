import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = "mail.rbugtiger.com"
smtp_port = 587
username = "atul@rbugtiger.com"
password = "@Password1"

# Message details
sender_email = "atul@rbugtiger.com"
receiver_email = "atulg0736@gmail.com"
subject = "Account Created"
body = """\
Dear Atul,

Your account atul@rbugtiger.com has been setup. In your e-mail program, use:

Username:   atul@rbugtiger.com
Password:   @Password1
POP/IMAP Server:   mail.rbugtiger.com
SMTP Server:   mail.rbugtiger.com port 587

Best regards,
Support Team
"""

# Setup the MIME
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the body to the email
message.attach(MIMEText(body, "plain"))

try:
    # Connect to the server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection

    # Login to the email account
    server.login(username, password)

    # Send the email
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)

    print("Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the server connection
    server.quit()
