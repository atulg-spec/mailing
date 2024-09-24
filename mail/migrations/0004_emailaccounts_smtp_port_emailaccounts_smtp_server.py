# Generated by Django 5.1.1 on 2024-09-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_alter_emailaudience_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaccounts',
            name='smtp_port',
            field=models.PositiveIntegerField(default=587),
        ),
        migrations.AddField(
            model_name='emailaccounts',
            name='smtp_server',
            field=models.CharField(default='smtp.gmail.com', max_length=255),
        ),
    ]
