# Generated by Django 4.2.2 on 2023-06-28 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
