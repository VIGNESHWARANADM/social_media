# Generated by Django 5.0.6 on 2024-07-15 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0016_followerscount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followerscount',
            old_name='follower',
            new_name='following',
        ),
    ]
