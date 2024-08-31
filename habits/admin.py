from django.contrib import admin
from .models import Frequency, Habit, HabitLog

@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    filter_horizontal = ('frequencies',) 

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'amount', 'date')