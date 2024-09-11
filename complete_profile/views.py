from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from .serializers import UserProfileSerializer, UserGoalsSerializer
from .models import UserGoals

class GoalsListView(APIView):
    def get(self, request):
        goals = UserGoals.objects.all()
        serializer = UserGoalsSerializer(goals, many=True)
        return Response(serializer.data)

class CompleteProfileView(APIView):
    def patch(self, request):
        # Assuming user is authenticated
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