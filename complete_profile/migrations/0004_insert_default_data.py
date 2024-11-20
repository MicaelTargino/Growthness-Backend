from django.db import migrations


def insert_default_usergoals(apps, schema_editor):
    # Get the UserGoals model
    UserGoals = apps.get_model('complete_profile', 'UserGoals')
    
    # Define the default goals
    default_goals = [
        "Emagrecimento",
        "Hipertrofia",
        "Manutenção da saúde",
    ]

    # Insert default goals
    for goal in default_goals:
        UserGoals.objects.get_or_create(title=goal)


class Migration(migrations.Migration):

    dependencies = [
        ('complete_profile', '0001_initial'),  
        ('complete_profile', '0002_usergoals_icon'),  
        ('complete_profile', '0003_remove_usergoals_icon'),  
    ]

    operations = [
        migrations.RunPython(insert_default_usergoals),
    ]
