from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitLogViewSet, FrequencyViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'habit-logs', HabitLogViewSet, basename='habit-logs')
router.register(r'frequencies', FrequencyViewSet, basename="frequencies")

urlpatterns = [
    path('', include(router.urls)),
]
