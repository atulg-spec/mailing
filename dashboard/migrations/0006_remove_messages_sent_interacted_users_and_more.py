# Generated by Django 5.1.1 on 2024-09-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_messages_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages_sent',
            name='interacted_users',
        ),
        migrations.RemoveField(
            model_name='messages_sent',
            name='platform',
        ),
        migrations.AddField(
            model_name='messages_sent',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='messages_sent',
            name='sent_from',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='messages_sent',
            name='sent_to',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
