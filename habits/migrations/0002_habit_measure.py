# Generated by Django 4.2.15 on 2024-08-30 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='measure',
            field=models.CharField(max_length=48, null=True),
        ),
    ]