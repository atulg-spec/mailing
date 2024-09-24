from django.template.loader import render_to_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from mail.models import EmailAccounts,EmailAudience
import time

def send_user_email(subject, content, sender_email, sender_password,receiver_email_list):
    smtp_server = 'mail.rbugtiger.com'
    smtp_port = 587
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email_list)

    # Attach HTML content
    html_content = render_to_string('send_user_email.html', context={'content': content})
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email_list, msg.as_string())




def send_bulk_emails(user,message_id,tag,customer_count):
    from dashboard.models import Messages,sent_message_history
    cred = EmailAccounts.objects.filter(user=user,is_active=True)
    message = Messages.objects.get(id=message_id)
    clients = EmailAudience.objects.filter(user=user).filter(tag=tag)[:int(customer_count)]
    emails = [x.email for x in clients]
    newlist = []
    emailslistlength =  emails.__len__()
    a = 0
    b = 0
    sent_message_history(user,message,clients.__len__(),'Email')
    total_sent = 0
    all_sent = False
    for x in cred:
        if all_sent:
            break
        for i in emails:
            b = a + 10
            if int(emailslistlength / 10) == 0:
                b = emailslistlength
                newlist = emails[a:b]
                total_sent = total_sent + newlist.__len__()
                try:
                    send_user_email(message.subject,message.content,x.email,x.apppassword,newlist)
                except:
                    pass
                all_sent = True
                break
            else:
                newlist = emails[a:b]
                total_sent = total_sent + newlist.__len__()
                try:
                    send_user_email(message.subject,message.content,x.email,x.apppassword,newlist)
                except:
                    pass
                time.sleep(2)
            a = b
            if total_sent >= 1000:
                total_sent = 0
                break