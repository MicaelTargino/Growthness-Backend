from django.urls import path
from .views import CompleteProfileView, GoalsListView


urlpatterns = [
    path('goals/', GoalsListView.as_view(), name='goals-list'),
    path('', CompleteProfileView.as_view(), name="complete-profile")
]
