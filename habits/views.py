from rest_framework import viewsets, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='completion-status')
    def completion_status(self, request):
        habits = self.get_queryset()
        results = []

        for habit in habits:
            goal = habit.goal
            frequency = habit.frequencies.first().name
            if frequency == 'daily':
                date_from = timezone.now().date() - timedelta(days=1)
            elif frequency == 'weekly':
                date_from = timezone.now().date() - timedelta(weeks=1)
            elif frequency == 'monthly':
                date_from = timezone.now().date() - timedelta(days=30)
            else:
                continue

            habit_logs = HabitLog.objects.filter(habit=habit, date__gte=date_from)
            total_amount = habit_logs.aggregate(Sum('amount'))['amount__sum'] or 0
            percentage_completion = (total_amount / goal) * 100 if goal else 0
            completed = percentage_completion >= 100

            results.append({
                'habit': habit.name,
                'frequency': frequency,
                'goal': goal,
                'total_amount': total_amount,
                'percentage_completion': percentage_completion,
                'completed': completed,
            })

        return Response(results, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='history')
    def habit_history(self, request):
        habits = self.get_queryset()
        date_from = timezone.now().date() - timedelta(days=7)
        results = []

        for habit in habits:
            habit_logs = HabitLog.objects.filter(habit=habit, date__gte=date_from).order_by('date')
            habit_logs_data = HabitLogSerializer(habit_logs, many=True).data
            results.append({
                'habit': habit.name,
                'logs': habit_logs_data
            })

        return Response(results, status=status.HTTP_200_OK)


class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter habit logs for habits owned by the logged-in user
        print(self.request.user)
        return HabitLog.objects.filter(habit__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
