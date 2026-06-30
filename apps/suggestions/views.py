from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import SuggestionService


class SuggestionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        message = request.data.get("message", "").strip()

        if not message:
            return Response(
                {"error": "message field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        suggestion = SuggestionService.suggest(message)

        return Response({
            "suggestion": suggestion
        })