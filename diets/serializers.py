from rest_framework import serializers
from .models import Food, Meal, MealFood

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class MealFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = MealFood
        fields = ['food', 'servings']


class MealSerializer(serializers.ModelSerializer):
    foods = MealFoodSerializer(source='mealfood_set', many=True)

    class Meta:
        model = Meal
        fields = ['name', 'date', 'foods']


class MealCreateSerializer(serializers.ModelSerializer):
    foods = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )

    class Meta:
        model = Meal
        fields = ['name', 'date', 'foods']

    def create(self, validated_data):
        foods_data = validated_data.pop('foods')  # Extract foods data
        meal = Meal.objects.create(**validated_data)
        for food_data in foods_data:
            food = Food.objects.get(id=food_data['food'])
            MealFood.objects.create(
                meal=meal,
                food=food,
                servings=food_data['servings']
            )
        return meal