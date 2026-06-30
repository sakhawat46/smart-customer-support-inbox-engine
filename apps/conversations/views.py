from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationListSerializer, MessageSerializer, ReplySerializer
from .pagination import CustomPagination





class ConversationListAPIView(ListAPIView):

    serializer_class = ConversationListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Conversation.objects.all()

        search = self.request.query_params.get("search")

        status = self.request.query_params.get("status")

        if search:
            queryset = queryset.filter(
                customer_name__icontains=search
            )

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-updated_at")
    

class MessageListAPIView(ListAPIView):

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        conversation_id = self.kwargs["pk"]

        return Message.objects.filter(
            conversation_id=conversation_id
        )
    


class ReplyAPIView(APIView):

    def post(self, request, pk):

        serializer = ReplySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        ConversationService.send_reply(
            conversation_id=pk,
            user=request.user,
            message=serializer.validated_data["message"]
        )

        return Response(
            {"message":"Reply Sent"}
        )