# Generated by Django 5.1.1 on 2024-09-21 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_alter_emailaccounts_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='emailaudience',
            unique_together=set(),
        ),
    ]
