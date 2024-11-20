from django.contrib import admin
from .models import Exercise, ExerciseLog, Routine, RoutineExercise, Goal
# Register your models here.
admin.site.register(Exercise)
admin.site.register(Goal)
admin.site.register(Routine)
admin.site.register(RoutineExercise)
admin.site.register(ExerciseLog)