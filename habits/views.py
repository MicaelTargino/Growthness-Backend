from rest_framework import viewsets, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, OuterRef, Subquery
from datetime import timedelta
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer, FrequencySerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .models import Habit, HabitLog, Frequency
from .serializers import HabitSerializer, HabitLogSerializer

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
 
    # New endpoint to retrieve habit logs by habit ID, date step, and start date range
    @action(detail=True, methods=['get'], url_path='habit-graph-logs', url_name='habit-graphlogs')
    def get_habit_logs(self, request, pk=None):
        habit_id = pk  # Get habitId from URL
        try:
            habit = Habit.objects.get(id=habit_id, user=self.request.user)  # Fetch habit for the logged-in user
        except Habit.DoesNotExist:
            return Response({"error": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get query parameters for date step and range
        start_date_range = request.query_params.get('startDateRange', '7')
        date_step = request.query_params.get('dateStep', '1')

        try:
            # Convert start_date_range and date_step to integers
            start_date_range = int(start_date_range)
            date_step = int(date_step)
        except ValueError:
            return Response({"error": "startDateRange and dateStep must be integers"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the date range
        today = timezone.now().date()
        date_from = today - timedelta(days=start_date_range-1)

        # Generate the list of dates within the range, spaced by `date_step`
        all_dates = []
        for i in range(0, start_date_range, date_step):
            date = date_from + timedelta(days=i)
            all_dates.append(date)

        # Fetch existing logs within the range
        habit_logs = HabitLog.objects.filter(habit=habit, date__gte=date_from).order_by('date')

        # Convert the habit logs to a dictionary keyed by the date for easier lookup
        logs_dict = {log.date: log.amount for log in habit_logs}

        # Prepare the data for the chart, ensuring all dates are present
        logs_data = []
        for date in all_dates:
            logs_data.append({
                'date': date.strftime('%Y-%m-%d'),  # Format the date
                'amount': logs_dict.get(date, 0),  # Use 0 if no log exists for the date
            })

        return Response({
            'habit': habit.name,
            'goal': habit.goal,
            'measure': habit.measure,
            'logs': logs_data,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='completion-status', url_name='completion-status')
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
                'id': habit.id,
                'habit': habit.name,
                'frequency': frequency,
                'goal': goal,
                'total_amount': total_amount,
                'percentage_completion': percentage_completion,
                'completed': completed,
            })

        return Response(results, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='history', url_name='history')
    def habit_history(self, request):
        habits = self.get_queryset()
        date_from = timezone.now().date() - timedelta(days=7)
        results = []

        for habit in habits:
            # Get the last log for each date
            latest_logs_subquery = HabitLog.objects.filter(
                habit=habit,
                date=OuterRef('date')
            ).order_by('-id')

            habit_logs = HabitLog.objects.filter(
                habit=habit,
                date__gte=date_from,
                id=Subquery(latest_logs_subquery.values('id')[:1])
            ).order_by('date')

            # Serialize the filtered logs
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

class FrequencyViewSet(viewsets.ModelViewSet):
    serializer_class = FrequencySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Frequency.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()