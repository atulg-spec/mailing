from django.db import models, transaction
from django.contrib.auth.models import User
import csv
import pandas as pd
from threading import Thread


class EmailAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50, default="")
    apppassword = models.CharField(max_length=255, default="", unique=True)  # Ensure uniqueness here
    is_active = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email Account"
        verbose_name_plural = "Email Accounts"
    def save(self, *args, **kwargs):
        first = False
        if not self.pk:
            first = True            
        if first:  # Check if the object is being created for the first time
            from mail.messaging.sendmessage import send_user_email
            try:
                send_user_email(
                    subject=f'E-mail logged in successfully !',
                    content=f'Your email {self.email} has logged in successfully to startmarket.in for marketing.',
                    sender_email=self.email,
                    sender_password=self.apppassword,
                    receiver_email_list=[self.user.email]
                )
                super().save(*args, **kwargs)
            except Exception as e:
                print('Email error -=-=-=-=-=-=')
                print(e)
        else:
            super().save(*args, **kwargs)

class EmailAudience(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    email = models.CharField(max_length=255,default="")
    tag = models.CharField(max_length=30,default="")
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Audiences"
        unique_together = ('user', 'email')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class EmailClientDataUpload(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(default="")
    tag = models.CharField(max_length=30, default="")

    class Meta:
        verbose_name = "Email Client Data"
        verbose_name_plural = "Upload Data"

    def __str__(self):
        return f"Email Data Uploaded"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Split the data field into individual email addresses
        email_list = self.data.splitlines()
        for email in email_list:
            email = email.strip()  # Clean up any extra spaces
            if email:  # Check if the email is not empty
                # Create an EmailAudience entry for each email
                EmailAudience.objects.get_or_create(
                    user=self.user,
                    email=email,
                    tag=self.tag
                )


class EmailClientData(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    csv_file = models.FileField(upload_to='email_data/')
    tag = models.CharField(max_length=30,default="")
    is_valid = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Email Client Data"
        verbose_name_plural = "Client's Data"
    def __str__(self):
        return f"EmailClientData , File: {self.csv_file.name}"
    
    def clean(self):
        if not self.csv_file.name.endswith('.csv'):
            pass

        try:
            decoded_file = self.csv_file.read().decode('utf-8')
            csv_reader = csv.DictReader(decoded_file.splitlines())
            if 'email' not in csv_reader.fieldnames:
                pass
        except Exception as e:
            pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        thread = Thread(target=self.add_data)
        thread.start()

    def add_data(self):
        print('Adding Email Data')
        df = pd.read_csv(self.csv_file)
        emails = df['email'].tolist()
        print(emails)
        with transaction.atomic():
            for email in emails:
                try:
                    print('success')
                    print(email)
                    if not EmailAudience.objects.filter(user=self.user, email=email, tag=self.tag).exists():
                        try:
                            EmailAudience.objects.create(user=self.user, email=email,tag=self.tag)
                        except:
                            pass
                except:
                    pass


