from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Exercise, Routine, RoutineExercise, ExerciseLog, Goal
from .serializers import (
    ExerciseSerializer,
    RoutineSerializer,
    RoutineExerciseSerializer,
    ExerciseLogSerializer,
    GoalSerializer
)

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
