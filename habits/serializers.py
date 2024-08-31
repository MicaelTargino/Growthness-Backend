from rest_framework import serializers
from .models import Habit, HabitLog

class HabitSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = ['id', 'user', 'name', 'goal', 'measure', 'frequencies', 'created_at']
    
    def validate_frequencies(self, value):
        # Ensure at least one frequency is selected
        if not value:
            raise serializers.ValidationError("Pelo menos uma frequência de acompanhamento precisa ser selecionada.")
        return value

    def create(self, validated_data):
        frequencies = validated_data.pop('frequencies')
        habit = Habit.objects.create(**validated_data)
        habit.frequencies.set(frequencies)
        return habit

    def update(self, instance, validated_data):
        frequencies = validated_data.pop('frequencies', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if frequencies is not None:
            instance.frequencies.set(frequencies)
        instance.save()
        return instance

class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ['id', 'habit', 'date', 'amount', 'created_at']
