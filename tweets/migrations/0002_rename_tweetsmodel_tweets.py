# Generated by Django 5.2.1 on 2025-05-27 02:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TweetsModel',
            new_name='Tweets',
        ),
    ]
