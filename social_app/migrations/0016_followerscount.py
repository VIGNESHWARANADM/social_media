# Generated by Django 5.0.6 on 2024-07-14 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0015_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
