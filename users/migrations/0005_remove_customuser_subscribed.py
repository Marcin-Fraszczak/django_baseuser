# Generated by Django 4.2.2 on 2023-06-28 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_subscribed_idea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='subscribed',
        ),
    ]
