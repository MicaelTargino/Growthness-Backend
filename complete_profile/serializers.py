from rest_framework import serializers
from .models import UserGoals
from authentication.models import User

class UserGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoals
        fields = ['id', 'title', 'icon']  # Expose ID and title


class UserProfileSerializer(serializers.ModelSerializer):
    goals = serializers.SerializerMethodField()  # For displaying all goals with selection status
    goal = serializers.PrimaryKeyRelatedField(
        queryset=UserGoals.objects.all(), write_only=True
    )  # For setting the selected goal by ID

    class Meta:
        model = User
        fields = ['weight', 'weight_measure', 'height', 'height_measure', 'birth_date', 'goal', 'goals']

    # Method to return all available goal titles with selection status
    def get_goals(self, obj):
        all_goals = UserGoals.objects.all()  # Get all available goals
        user_goal_id = obj.goal.id if obj.goal else None  # Get the ID of the user's selected goal, if any

        # Create a list of goals with title and selection status
        return [
            {
                'id': goal.id,
                'title': goal.title,
                'selected': goal.id == user_goal_id  # Check if this goal is the selected one
            }
            for goal in all_goals
        ]

    # Overriding the update method to handle goal ID
    def update(self, instance, validated_data):
        goal_id = validated_data.pop('goal', None)
        if goal_id:
            instance.goal = goal_id  # Set the goal by ID
        return super().update(instance, validated_data)
