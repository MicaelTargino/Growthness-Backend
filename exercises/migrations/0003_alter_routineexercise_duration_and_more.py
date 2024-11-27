# Generated by Django 4.2.15 on 2024-11-26 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_routineexercise_average_velocity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineexercise',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Duration in minutes for cardio exercises', null=True),
        ),
        migrations.AlterField(
            model_name='routineexercise',
            name='reps_goal',
            field=models.IntegerField(blank=True, help_text='Reps goal for this exercise', null=True),
        ),
        migrations.AlterField(
            model_name='routineexercise',
            name='weight_goal',
            field=models.IntegerField(blank=True, help_text='Weight goal for this exercise', null=True),
        ),
    ]