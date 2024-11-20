from rest_framework import generics, status
from rest_framework.response import Response
from .models import Food, Meal, MealFood
from .serializers import FoodSerializer, MealSerializer, MealCreateSerializer, MealFoodSerializer
from rest_framework.permissions import IsAuthenticated

class FoodListCreateView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]


class MealListCreateView(generics.ListCreateAPIView):
    serializer_class = MealCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)


class MealFoodsListView(generics.ListAPIView):
    serializer_class = MealFoodSerializer

    def get(self, request, meal_id):
        try:
            meal = Meal.objects.get(id=meal_id, user=request.user)  # Fetch the meal for the logged-in user
        except Meal.DoesNotExist:
            return Response({"error": "Meal not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get all MealFood objects related to the meal
        meal_foods = MealFood.objects.filter(meal=meal)
        serializer = self.get_serializer(meal_foods, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)