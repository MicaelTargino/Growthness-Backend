from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_data, create_models_data
import json

class GenerateData(APIView):
    def get(self, request):
        return Response({"detail": "Method Not Supported"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # try:
            data = request.data
            # print(data)
            goal = data.get('goal', '')

            if not goal:
                return Response({"detail": "Insufficient data."},status=status.HTTP_400_BAD_REQUEST)

            print(goal)
            
            # get the habits, exercises and diets data
            new_data = get_data(data)
            if new_data is None:
                return Response({"detail": "Error generating data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Get the authenticated user
            user = request.user

            # Save the data to the correct models for the user
            create_models_data(new_data, user)

            return Response({"detail": "OK"},status=200)
        # except json.JSONDecodeError:
        #     return Response({"detail": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        # except ValueError as e:
        #     return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # except Exception as e:
        #     return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
