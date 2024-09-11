from rest_framework import serializers
from .models import UserGoals
from authentication.models import User

class UserGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoals
        fields = ['id', 'title']  # Expose ID and title

class UserProfileSerializer(serializers.ModelSerializer):
    goals = serializers.SerializerMethodField()  # For reading (displaying titles)
    goals_ids = serializers.PrimaryKeyRelatedField(
        queryset=UserGoals.objects.all(), write_only=True, many=True
    )  # For writing (receiving goal IDs)

    class Meta:
        model = User
        fields = ['weight', 'weight_measure', 'height', 'height_measure', 'goals', 'goals_ids']  # 'goals_ids' for input

    # Method to return goal titles when serializing
    def get_goals(self, obj):
        return obj.goals.values_list('title', flat=True)  # Returns a list of goal titles

    # Overriding the update method to handle goal IDs
    def update(self, instance, validated_data):
        goals_ids = validated_data.pop('goals_ids', None)
        if goals_ids:
            instance.goals.set(goals_ids)  # Update goals by IDs
        return super().update(instance, validated_data)