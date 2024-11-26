from django.db import models
from authentication.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    exercise_type = models.CharField(max_length=50, choices=[('gym', 'Gym'), ('cardio', 'Cardio')])
    duration = models.PositiveIntegerField(help_text='Duration in minutes', blank=True, null=True)
    # Additional fields for cardio exercises
    distance = models.FloatField(help_text='Distance in kilometers', blank=True, null=True)
    average_velocity = models.FloatField(help_text='Average velocity in km/h', blank=True, null=True)
    pace = models.FloatField(help_text='Pace in minutes per kilometer', blank=True, null=True)

    def __str__(self):
        return self.name

class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
    exercises = models.ManyToManyField(Exercise, through='RoutineExercise')
    week_start_date = models.DateField()

    def __str__(self):
        return f'Routine for {self.user.email} starting on {self.week_start_date}'

class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ], null=True, blank=True)
    weight_goal = models.IntegerField(help_text='Weight goal for this exercise', blank=True, null=True)
    reps_goal = models.IntegerField(help_text='Reps goal for this exercise', blank=True, null=True)
    duration = models.IntegerField(help_text='Duration in minutes for cardio exercises', blank=True, null=True)
    distance = models.FloatField(help_text='Distance in kilometers for cardio exercises', blank=True, null=True)
    pace = models.FloatField(help_text='Pace in minutes per kilometer for cardio exercises', blank=True, null=True)
    average_velocity = models.FloatField(help_text='Average velocity in km/h for cardio exercises', blank=True, null=True)

    def __str__(self):
        return f'{self.exercise.name} on {self.day_of_week} in {self.routine}'

class ExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_logs')
    routine_exercise = models.ForeignKey(RoutineExercise, on_delete=models.CASCADE)
    date_logged = models.DateField()
    weight = models.PositiveIntegerField(help_text='Weight used during exercise', blank=True, null=True)
    reps = models.PositiveIntegerField(help_text='Reps completed', blank=True, null=True)
    # Additional fields for cardio exercise logs
    distance_logged = models.FloatField(help_text='Distance in kilometers logged', blank=True, null=True)
    average_velocity_logged = models.FloatField(help_text='Average velocity in km/h logged', blank=True, null=True)
    pace_logged = models.FloatField(help_text='Pace in minutes per kilometer logged', blank=True, null=True)

    def __str__(self):
        return f'Log for {self.routine_exercise.exercise.name} on {self.date_logged}'


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    description = models.TextField()
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)

    def __str__(self):
        return f'Goal for {self.user.email}: {self.description}'
