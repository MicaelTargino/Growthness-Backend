
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitLogViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'habit-logs', HabitLogViewSet, basename='habit-logs')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
