from django.urls import path

from .views import (
    ConversationListAPIView,
    MessageListAPIView,
    ReplyAPIView,
)

urlpatterns = [

    path("conversations/", ConversationListAPIView.as_view(), name="conversation-list",),
    path("conversations/<int:pk>/messages/", MessageListAPIView.as_view(), name="conversation-messages",),
    path("conversations/<int:pk>/reply/", ReplyAPIView.as_view(), name="conversation-reply",),
]