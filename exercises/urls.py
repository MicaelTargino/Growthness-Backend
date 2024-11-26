from django.urls import path
from .views import (
    ExerciseListCreateView,
    ExerciseDetailView,
    RoutineListCreateView,
    RoutineDetailView,
    RoutineExerciseListCreateView,
    RoutineExerciseDetailView,
    ExerciseLogListCreateView,
    ExerciseLogDetailView,
    GoalListCreateView,
    GoalDetailView,
    ExercisesForTodayView,
    RoutineExerciseViewSet,
    GetRoutineIdView
)

urlpatterns = [
    path('exercises/', ExerciseListCreateView.as_view(), name='exercise-list-create'),
    path('exercises/<int:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('routines/', RoutineListCreateView.as_view(), name='routine-list-create'),
    path('routines/get-id/', GetRoutineIdView.as_view(), name='get-routine-id'),
    path('routines/<int:pk>/', RoutineDetailView.as_view(), name='routine-detail'),
    path('routines-exercises/', RoutineExerciseListCreateView.as_view(), name='routine-exercise-list-create'),
    path('routines-exercises/<int:pk>/', RoutineExerciseDetailView.as_view(), name='routine-exercise-detail'),
    path('exercise-logs/', ExerciseLogListCreateView.as_view(), name='exercise-log-list-create'),
    path('exercise-logs/<int:pk>/', ExerciseLogDetailView.as_view(), name='exercise-log-detail'),
    path('exercises-today/', ExercisesForTodayView.as_view(), name='exercises-for-today'),
    path('routines-exercises/<int:pk>/exercise-graph-logs/', RoutineExerciseViewSet.as_view({'get': 'get_exercise_logs'}), name='exercise-graph-logs'),
    path('goals/', GoalListCreateView.as_view(), name='goal-list-create'),
    path('goals/<int:pk>/', GoalDetailView.as_view(), name='goal-detail'),
]
