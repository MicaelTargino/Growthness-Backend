from rest_framework import serializers
from .models import Exercise, Routine, RoutineExercise, ExerciseLog, Goal

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'


class RoutineExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)  # Include the exercise name
    exercise_type = serializers.CharField(source='exercise.exercise_type', read_only=True)  # Include the exercise type

    class Meta:
        model = RoutineExercise
        fields = [
            'id', 
            'day_of_week', 
            'weight_goal', 
            'reps_goal', 
            'duration', 
            'distance', 
            'pace', 
            'average_velocity', 
            'exercise_name',    # Include exercise name
            'exercise_type'     # Include exercise type
        ]

    def validate(self, data):
        exercise_type = data['exercise'].exercise_type
        
        if exercise_type == 'cardio':
            # Validate cardio-specific fields
            if not data.get('duration'):
                raise serializers.ValidationError("Duration is required for cardio exercises.")
            if not data.get('pace') and not data.get('average_velocity'):
                raise serializers.ValidationError("Pace or average velocity is required for cardio exercises.")
            # Ensure gym-specific fields are not provided
            if data.get('weight_goal') or data.get('reps_goal'):
                raise serializers.ValidationError("Weight and reps goals are not applicable for cardio exercises.")
        
        elif exercise_type == 'gym':
            # Validate gym-specific fields
            if not data.get('weight_goal'):
                raise serializers.ValidationError("Weight goal is required for gym exercises.")
            if not data.get('reps_goal'):
                raise serializers.ValidationError("Reps goal is required for gym exercises.")
        
        return data


class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
