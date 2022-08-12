# Generated by Django 4.0.6 on 2022-08-12 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscription',
            name='rewardClaimed',
            field=models.IntegerField(default=0),
        ),
    ]
