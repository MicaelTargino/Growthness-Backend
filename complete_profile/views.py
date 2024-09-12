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
        missing_fields = []
        
        if not user.weight:
            missing_fields.append("weight")
        if not user.height:
            missing_fields.append("height")
        if not user.goals.exists():  # If no goals are associated with the user
            missing_fields.append("goals")

        # Check if the profile is complete
        if not missing_fields:
            return Response({"profile_complete": True, "missing_fields": [], "percentage": 100}, status=status.HTTP_200_OK)
        else:
            return Response({"profile_complete": False, "percentage": (100/3 * (3-len(missing_fields))), "missing_fields": missing_fields}, status=status.HTTP_200_OK)