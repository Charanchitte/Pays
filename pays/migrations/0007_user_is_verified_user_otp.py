# Generated by Django 4.0.8 on 2023-03-11 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pays', '0006_alter_professional_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]