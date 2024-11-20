from django.db import migrations

def insert_default_frequencies(apps, schema_editor):
    # Get the Frequency model
    Frequency = apps.get_model('habits', 'Frequency')
    
    # Define the default frequencies
    default_frequencies = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    # Insert default frequencies
    for name, display in default_frequencies:
        Frequency.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_rename_daily_goal_habit_goal')
    ]

    operations = [
        migrations.RunPython(insert_default_frequencies),
    ]
