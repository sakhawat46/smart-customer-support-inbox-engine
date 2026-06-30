from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Conversation, Message
from django.utils import timezone
from apps.analytics.tasks import analyze_sentiment

class ConversationService:

    @staticmethod
    def send_reply(conversation_id, user, message):

        conversation = Conversation.objects.get(
            pk=conversation_id
        )

        Message.objects.create(
            conversation=conversation,
            sender="agent",
            agent=user,
            message=message
        )

        conversation.updated_at = timezone.now()

        conversation.save()

        # analyze_sentiment.delay(conversation.id)

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"conversation_{conversation.id}",
            {
                "type":"chat.message",
                "message":message
            }
        )