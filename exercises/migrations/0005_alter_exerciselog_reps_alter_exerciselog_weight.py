from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_alter_exercise_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciselog',
            name='reps',
            field=models.IntegerField(blank=True, help_text='Reps completed', null=True),
        ),
        migrations.AlterField(
            model_name='exerciselog',
            name='weight',
            field=models.IntegerField(blank=True, help_text='Weight used during exercise', null=True),
        ),
    ]
