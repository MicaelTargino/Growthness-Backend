from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitLogViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'habit-logs', HabitLogViewSet, basename='habit-logs')

urlpatterns = [
    path('', include(router.urls)),
]
