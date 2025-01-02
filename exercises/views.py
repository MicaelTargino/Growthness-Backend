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

from django.db.models import Max, OuterRef, Subquery
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
        all_dates = [date_from + timedelta(days=i) for i in range(0, start_date_range, date_step)]

        # Fetch logs with only the last record for each date
        latest_logs_subquery = ExerciseLog.objects.filter(
            routine_exercise=routine_exercise,
            date_logged=OuterRef('date_logged')
        ).order_by('-id')

        exercise_logs = ExerciseLog.objects.filter(
            routine_exercise=routine_exercise,
            date_logged__gte=date_from,
            id=Subquery(latest_logs_subquery.values('id')[:1]) 
        ).order_by('date_logged')

        # Check the type of exercise (gym or cardio) and prepare appropriate data
        is_gym = exercise_logs.filter(weight__isnull=False).exists()  # Check if weight is logged
        is_cardio = exercise_logs.filter(distance_logged__isnull=False).exists()  # Check if distance is logged

        if is_gym:
            # Convert the exercise logs to a dictionary keyed by the date for weights
            logs_dict = {log.date_logged: log.weight for log in exercise_logs}
            data_type = "weight"
        elif is_cardio:
            # Convert the exercise logs to a dictionary keyed by the date for distances
            logs_dict = {log.date_logged: log.distance_logged for log in exercise_logs}
            data_type = "distance_logged"
        else:
            return Response([0 for date in all_dates], status=status.HTTP_200_OK)

        # Prepare the data for the chart, ensuring all dates are present
        exercise_data = [logs_dict.get(date, 0) for date in all_dates]

        # Include metadata for the frontend
        response_data = exercise_data

        return Response(response_data, status=status.HTTP_200_OK)

# class RoutineExerciseViewSet(viewsets.ModelViewSet):
#     queryset = RoutineExercise.objects.all()
#     serializer_class = RoutineExerciseSerializer
#     permission_classes = [IsAuthenticated]

#     @action(detail=True, methods=['get'], url_path='exercise-graph-logs', url_name='exercise-graph-logs')
#     def get_exercise_logs(self, request, pk=None):
#         routine_exercise_id = pk  # Get RoutineExercise ID from the URL
#         try:
#             routine_exercise = RoutineExercise.objects.get(id=routine_exercise_id, routine__user=self.request.user)
#         except RoutineExercise.DoesNotExist:
#             return Response({"error": "Routine exercise not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Get query parameters for date range
#         start_date_range = request.query_params.get('startDateRange', '7')
#         date_step = request.query_params.get('dateStep', '1')

#         try:
#             # Convert start_date_range and date_step to integers
#             start_date_range = int(start_date_range)
#             date_step = int(date_step)
#         except ValueError:
#             return Response({"error": "startDateRange and dateStep must be integers"}, status=status.HTTP_400_BAD_REQUEST)

#         # Calculate the date range
#         today = timezone.now().date()
#         date_from = today - timedelta(days=start_date_range - 1)

#         # Generate the list of dates within the range, spaced by `date_step`
#         all_dates = [date_from + timedelta(days=i) for i in range(0, start_date_range, date_step)]

#         # Fetch existing logs within the range
#         exercise_logs = ExerciseLog.objects.filter(
#             routine_exercise=routine_exercise, 
#             date_logged__gte=date_from
#         ).order_by('date_logged')

#         # Check the type of exercise (gym or cardio) and prepare appropriate data
#         is_gym = exercise_logs.filter(weight__isnull=False).exists()  # Check if weight is logged
#         is_cardio = exercise_logs.filter(distance_logged__isnull=False).exists()  # Check if distance is logged

#         if is_gym:
#             # Convert the exercise logs to a dictionary keyed by the date for weights
#             logs_dict = {log.date_logged: log.weight for log in exercise_logs}
#             data_type = "weight"
#         elif is_cardio:
#             # Convert the exercise logs to a dictionary keyed by the date for distances
#             logs_dict = {log.date_logged: log.distance_logged for log in exercise_logs}
#             data_type = "distance_logged"
#         else:
#             return Response([0 for date in all_dates], status=status.HTTP_200_OK)

#         # Prepare the data for the chart, ensuring all dates are present
#         exercise_data = [logs_dict.get(date, 0) for date in all_dates]

#         # Include metadata for the frontend
#         response_data = exercise_data

#         return Response(response_data, status=status.HTTP_200_OK)
    

class GetRoutineIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # The user is authenticated via the token, so we can access it via `request.user`
        user = request.user

        # Retrieve the user's routine
        try:
            routine = Routine.objects.filter(user=user).first()  # Get the first routine for the user
            if not routine:
                return Response({"error": "No routine found for this user."}, status=status.HTTP_404_NOT_FOUND)
        except Routine.DoesNotExist:
            return Response({"error": "No routine found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Return the routine ID
        return Response({"routine_id": routine.id}, status=status.HTTP_200_OK)
    
class WeeklyExercisesView(APIView):
    """
    View to return exercises assigned for each day of the week for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch the user's routines
        routines = Routine.objects.filter(user=request.user)

        if not routines.exists():
            return Response({"error": "No routines found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch all RoutineExercises for the user's routines
        weekly_exercises = RoutineExercise.objects.filter(routine__in=routines).values(
            'day_of_week', 'exercise__name', 'exercise__exercise_type', 'weight_goal', 'reps_goal',
            'duration', 'distance', 'pace', 'average_velocity'
        ).order_by('day_of_week', 'exercise__name')

        # Initialize the result dictionary with days of the week
        result = {day: [] for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']}
        # result['unknown'] = []  # For any exercises with no day_of_week set

        for exercise in weekly_exercises:
            day = exercise.pop('day_of_week')
            if day in result:
                result[day].append(exercise)
            # else:
                # result['unknown'].append(exercise)  # Handle exercises without a valid day_of_week

        return Response(result, status=status.HTTP_200_OK)
