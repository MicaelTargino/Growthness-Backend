import datetime 
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Exercise, Routine, RoutineExercise, ExerciseLog, Goal
from .serializers import (
    ExerciseSerializer,
    RoutineSerializer,
    RoutineExerciseSerializer,
    ExerciseLogSerializer,
    GoalSerializer
)

# Mapping the current day in English
DAY_MAPPING = {
    0: 'monday',
    1: 'tuesday',
    2: 'Wednesday',
    3: 'thursday',
    4: 'friday',
    5: 'saturday',
    6: 'sunday'
}

class ExercisesForTodayView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.date.today().weekday()
        current_day = DAY_MAPPING.get(today).lower()

        print(current_day)

        # Filter RoutineExercises for the current day
        exercises = RoutineExercise.objects.filter(day_of_week=current_day, routine__user=request.user)
        
        # Serialize the exercises
        serializer = RoutineExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

# Exercise Views
class ExerciseListCreateView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]  # Require authentication


# Routine Views
class RoutineListCreateView(generics.ListCreateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class RoutineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [IsAuthenticated]  # Require authentication


# RoutineExercise Views
class RoutineExerciseListCreateView(generics.ListCreateAPIView):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class RoutineExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

# ExerciseLog Views
class ExerciseLogListCreateView(generics.ListCreateAPIView):
    queryset = ExerciseLog.objects.all()
    serializer_class = ExerciseLogSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        # Automatically set the user field to request.user
        serializer.save(user=self.request.user)

class ExerciseLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExerciseLog.objects.all()
    serializer_class = ExerciseLogSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

# Goal Views
class GoalListCreateView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]  # Require authentication



class RoutineExerciseViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='exercise-graph-logs', url_name='exercise-graph-logs')
    def get_exercise_logs(self, request, pk=None):
        routine_exercise_id = pk  # Get RoutineExercise ID from the URL
        try:
            routine_exercise = RoutineExercise.objects.get(id=routine_exercise_id, routine__user=self.request.user)
        except RoutineExercise.DoesNotExist:
            return Response({"error": "Routine exercise not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get query parameters for date range
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
        date_from = today - timedelta(days=start_date_range - 1)

        # Generate the list of dates within the range, spaced by `date_step`
        all_dates = []
        for i in range(0, start_date_range, date_step):
            date = date_from + timedelta(days=i)
            all_dates.append(date)

        # Fetch existing logs within the range
        exercise_logs = ExerciseLog.objects.filter(routine_exercise=routine_exercise, date_logged__gte=date_from).order_by('date_logged')

        # Convert the exercise logs to a dictionary keyed by the date for easier lookup
        logs_dict = {log.date_logged: log.weight for log in exercise_logs}

        # Prepare the data for the chart, ensuring all dates are present (only the weight data)
        weights_data = [logs_dict.get(date, 0) for date in all_dates]

        return Response(weights_data, status=status.HTTP_200_OK)