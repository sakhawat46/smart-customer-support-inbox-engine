from rest_framework.views import APIView
from rest_framework.response import Response
from .services import SuggestionService

class SuggestionAPIView(APIView):

    def post(self, request, pk):

        message = request.data["message"]

        suggestion = SuggestionService.suggest(message)

        return Response({
            "suggestion":suggestion
        })