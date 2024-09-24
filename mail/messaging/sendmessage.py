from django.template.loader import render_to_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mail.models import EmailAccounts,EmailAudience
import time

def send_user_email(subject, content, sender_email, sender_password,receiver_email,smtp_server,smtp_port):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Attach HTML content
    html_content = render_to_string('send_user_email.html', context={'content': content})
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())




def send_bulk_emails(user,message_id,tag,customer_count):
    from dashboard.models import Messages, messages_sent
    cred = EmailAccounts.objects.filter(user=user,is_active=True)
    message = Messages.objects.get(id=message_id)
    clients = EmailAudience.objects.filter(user=user).filter(tag=tag)[:int(customer_count)]
    emails = [x.email for x in clients]
    for x in emails:
        temp = 1
        for y in cred:
            temp = temp + 1
            if temp >= 1000:
                break
            send_user_email(message.subject,message.content,y.email,y.apppassword,x,y.smtp_server,y.smtp_port)
            messages_sent.objects.create(user=message.user,sent_from=y.email,sent_to=x)