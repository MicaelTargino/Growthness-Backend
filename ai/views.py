from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_data_with_gpt, create_models_data
import json

class GenerateData(APIView):
    def get(self, request):
        return Response({"detail": "Method Not Supported"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            print(data)
            
            # Send data to GPT and retrieve the response
            new_data = generate_data_with_gpt(data)
            
            if new_data is None:
                return Response({"detail": "Error generating data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            print(new_data)

            # Get the authenticated user
            user = request.user

            # Save the GPT data to the correct models for the user
            create_models_data(new_data, user)

            return Response({"detail": "OK"}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
