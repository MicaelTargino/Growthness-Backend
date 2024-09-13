from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .serializers import UserProfileSerializer, UserGoalsSerializer
from .models import UserGoals

class GoalsListView(APIView):
    def get(self, request):
        goals = UserGoals.objects.all()
        serializer = UserGoalsSerializer(goals, many=True)
        return Response(serializer.data)

class CompleteProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        user = request.user

        # Retrieve the user's profile
        try:
            profile = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Partial update (only update fields provided in the request body)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncompleteProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):

        user = request.user 

        try:
            user = User.objects.get(pk=user.id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check which fields are missing
        field_status = []

        field_status.append({"name": "weight", "description": "Adcione seu peso", "completed": True if user.weight else False})
        field_status.append({"name": "height", "description": "Adcione sua altura", "completed": True if user.height else False})
        field_status.append({"name": "goals", "description": "Adcione seu objetivo", "completed": True if user.goals else False})


        # Check if the profile is complete
        import math
        completion_percentage = math.ceil(100/len(field_status) * (len(field_status)-len([i for i in field_status if i["completed"] == False])))

        return Response({"profile_complete": False, "percentage": completion_percentage, "fields": field_status}, status=status.HTTP_200_OK)