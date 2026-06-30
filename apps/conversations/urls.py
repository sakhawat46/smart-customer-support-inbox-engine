from django.urls import path

from .views import (
    ConversationListAPIView,
    MessageListAPIView,
    ReplyAPIView,
    ConversationCreateAPIView,
    AcquireLockAPIView,
    ReleaseLockAPIView,
    LockStatusAPIView
)

urlpatterns = [

    path("conversations/", ConversationListAPIView.as_view(), name="conversation-list",),
    path("conversations/<int:pk>/messages/", MessageListAPIView.as_view(), name="conversation-messages",),
    path("conversations/<int:pk>/reply/", ReplyAPIView.as_view(), name="conversation-reply",),

    path("conversations/create/", ConversationCreateAPIView.as_view(), name="conversation-create",),

    path("conversations/<int:pk>/lock/", AcquireLockAPIView.as_view(), name="conversation-lock",),
    path("conversations/<int:pk>/unlock/", ReleaseLockAPIView.as_view(), name="conversation-unlock",),
    path("conversations/<int:pk>/lock-status/", LockStatusAPIView.as_view(), name="conversation-lock-status",),
]