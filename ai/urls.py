from django.urls import path 
from .views import GenerateData
urlpatterns = [
    path('generate-data/', GenerateData.as_view(), name="ai-generate-data")
]
