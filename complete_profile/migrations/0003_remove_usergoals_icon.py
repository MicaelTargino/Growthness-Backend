# Generated by Django 4.2.15 on 2024-09-15 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complete_profile', '0002_usergoals_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergoals',
            name='icon',
        ),
    ]
