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
    # Add exercise name and exercise type from the related Exercise model
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    exercise_type = serializers.CharField(source='exercise.exercise_type', read_only=True)

    class Meta:
        model = RoutineExercise
        fields = [
            'id', 
            'exercise',
            'routine',
            'day_of_week', 
            'exercise_name', 
            'exercise_type', 
            'weight_goal', 
            'reps_goal', 
            'duration', 
            'distance', 
            'pace', 
            'average_velocity'
        ]

    def validate(self, data):
        """
        Custom validation logic for RoutineExercise.
        """
        # Clean up fields that might be empty strings
        data['weight_goal'] = data.get('weight_goal') if data.get('weight_goal') not in ["", None] else None
        data['reps_goal'] = data.get('reps_goal') if data.get('reps_goal') not in ["", None] else None
        data['duration'] = data.get('duration') if data.get('duration') not in ["", None] else None
        data['distance'] = data.get('distance') if data.get('distance') not in ["", None] else None
        data['pace'] = data.get('pace') if data.get('pace') not in ["", None] else None
        data['average_velocity'] = data.get('average_velocity') if data.get('average_velocity') not in ["", None] else None

        exercise = data.get('exercise')
        if not exercise:
            raise serializers.ValidationError("Exercise must be provided.")
        exercise_type = exercise.exercise_type

        # Validation for `cardio` exercises
        if exercise_type == 'cardio':
            if not data.get('duration'):
                raise serializers.ValidationError({"duration": "Duration is required for cardio exercises."})
            if not data.get('pace') and not data.get('average_velocity'):
                raise serializers.ValidationError({"pace": "Pace or average velocity is required for cardio exercises."})
            if data.get('weight_goal') is not None:
                raise serializers.ValidationError({"weight_goal": "Weight goal is not applicable for cardio exercises."})
            if data.get('reps_goal') is not None:
                raise serializers.ValidationError({"reps_goal": "Reps goal is not applicable for cardio exercises."})

        # Validation for `gym` exercises
        elif exercise_type == 'gym':
            if not data.get('weight_goal'):
                raise serializers.ValidationError({"weight_goal": "Weight goal is required for gym exercises."})
            if not data.get('reps_goal'):
                raise serializers.ValidationError({"reps_goal": "Reps goal is required for gym exercises."})
            if data.get('duration') is not None:
                raise serializers.ValidationError({"duration": "Duration is not applicable for gym exercises."})
            if data.get('distance') is not None:
                raise serializers.ValidationError({"distance": "Distance is not applicable for gym exercises."})
            if data.get('pace') is not None:
                raise serializers.ValidationError({"pace": "Pace is not applicable for gym exercises."})
            if data.get('average_velocity') is not None:
                raise serializers.ValidationError({"average_velocity": "Average velocity is not applicable for gym exercises."})

        return data

class ExerciseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseLog
        fields = '__all__'

    user = serializers.PrimaryKeyRelatedField(read_only=True)

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
