from rest_framework import serializers
from .models import Conversation
from .models import Message

class ConversationListSerializer(serializers.ModelSerializer):

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "customer_name",
            "last_message",
            "status",
            "created_at",
        )

    def get_last_message(self, obj):
        message = obj.messages.last()
        return message.message if message else None
    

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "message",
            "timestamp",
        )

    
class ReplySerializer(serializers.Serializer):
    message = serializers.CharField()



class ConversationCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    message = serializers.CharField()