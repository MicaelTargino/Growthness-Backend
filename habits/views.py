from rest_framework import viewsets, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Directly filter habits for the logged-in user
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the habit with the current user
        serializer.save(user=self.request.user)

class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter habit logs for habits owned by the logged-in user
        return HabitLog.objects.filter(habit__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
