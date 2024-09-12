from django.urls import path
from .views import CompleteProfileView, GoalsListView, IncompleteProfileView


urlpatterns = [
    path('goals/', GoalsListView.as_view(), name='goals-list'),
    path('', CompleteProfileView.as_view(), name="complete-profile"),
    path('/profile-status/', IncompleteProfileView.as_view(), name="incomplete-profile"),
]
