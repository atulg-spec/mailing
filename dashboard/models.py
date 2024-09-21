from django.db import models
from mail.messaging.sendmessage import send_bulk_emails
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
import threading
from ckeditor_uploader.fields import RichTextUploadingField

contenttype = [
        ('text', 'text'),
        ('html', 'html'),
    ]


status_choices = [
        ('success', 'success'),
        ('pending', 'pending'),
        ('failed', 'failed'),
    ]

platform_choices = [
        ('Email', 'Email'),
    ]


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.CharField(max_length=150, default='')
    content_type = models.CharField(choices=contenttype, max_length=12, default="text")
    content = RichTextUploadingField()
    massenger = models.CharField(choices=platform_choices, max_length=15, default="Email")
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class messages_sent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    message = models.ForeignKey(Messages,on_delete=models.CASCADE,blank=True,null=True)
    interacted_users = models.PositiveIntegerField(default=0)
    platform = models.CharField(choices=platform_choices, max_length=12,default="Email")
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.platform
    class Meta:
        verbose_name = "Message sent"
        verbose_name_plural = "Delivered messages"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

def sent_message_history(user,message,interacted_users,platform):
    amount = (interacted_users * 0.5) * -1
    messages_sent.objects.create(user=user,message=message,interacted_users=interacted_users,platform=platform)


class Campaign(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.CharField(max_length=30, default='')
    count = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.message.subject

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def save(self, *args, **kwargs):
        thread = threading.Thread(target=send_bulk_emails,args = (self.user,self.message.id,self.tag,self.count))
        thread.start()
        super().save(*args, **kwargs)

