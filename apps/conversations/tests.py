from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.conversations.models import Conversation, Message
from apps.conversations.locking import ConversationLockService, LOCK_TIMEOUT
from apps.suggestions.services import SuggestionService
from apps.suggestions.rules import RULES

User = get_user_model()


def get_tokens_for_user(user):
    """Return JWT Bearer token string for a given user."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def make_conversation(customer_name="Test User", status=Conversation.Status.OPEN):
    return Conversation.objects.create(customer_name=customer_name, status=status)


def make_message(conversation, sender=Message.Sender.CUSTOMER, text="Hello"):
    return Message.objects.create(
        conversation=conversation,
        sender=sender,
        message=text,
    )


# Unit Test 1 — Conversation & Message Model Methods
class ConversationModelTest(TestCase):
    """Tests for Conversation and Message model behaviour."""

    def setUp(self):
        self.conversation = make_conversation(customer_name="Alice")

    def test_conversation_str(self):
        """__str__ returns '<name> (<status>)'."""
        expected = "Alice (open)"
        self.assertEqual(str(self.conversation), expected)

    def test_message_str(self):
        """Message __str__ returns '<sender> - <conversation_id>'."""
        msg = make_message(self.conversation, sender=Message.Sender.CUSTOMER, text="Hi")
        expected = f"customer - {self.conversation.id}"
        self.assertEqual(str(msg), expected)

    def test_messages_ordered_by_timestamp(self):
        """Messages are returned in chronological order."""
        m1 = make_message(self.conversation, text="First")
        m2 = make_message(self.conversation, text="Second")
        messages = list(self.conversation.messages.all())
        self.assertEqual(messages[0].id, m1.id)
        self.assertEqual(messages[1].id, m2.id)

    def test_default_sentiment_is_neutral(self):
        """A new Conversation defaults to Neutral sentiment."""
        self.assertEqual(self.conversation.sentiment, Conversation.Sentiment.NEUTRAL)

    def test_default_status_is_open(self):
        """A new Conversation defaults to Open status."""
        self.assertEqual(self.conversation.status, Conversation.Status.OPEN)



# API Integration Test 1 — JWT Authentication
class JWTAuthenticationTest(APITestCase):
    """Validates that all protected endpoints reject unauthenticated requests."""

    def setUp(self):
        self.client = APIClient()
        self.conversation = make_conversation("Bob")

    def test_conversations_list_requires_auth(self):
        """GET /api/conversations/ returns 401 without token."""
        response = self.client.get("/api/conversations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_messages_list_requires_auth(self):
        """GET /api/conversations/{id}/messages/ returns 401 without token."""
        response = self.client.get(f"/api/conversations/{self.conversation.id}/messages/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reply_requires_auth(self):
        """POST /api/conversations/{id}/reply/ returns 401 without token."""
        response = self.client.post(
            f"/api/conversations/{self.conversation.id}/reply/",
            {"message": "Hi"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_suggest_reply_requires_auth(self):
        """POST /api/conversations/{id}/suggest-reply/ returns 401 without token."""
        response = self.client.post(
            f"/api/conversations/{self.conversation.id}/suggest-reply/",
            {"message": "refund"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acquire_lock_requires_auth(self):
        """POST /api/conversations/{id}/lock/ returns 401 without token."""
        response = self.client.post(f"/api/conversations/{self.conversation.id}/lock/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_conversations(self):
        """A valid JWT token grants access to the conversations list."""
        user = User.objects.create_user(email="agent@test.com", password="pass1234")
        token = get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get("/api/conversations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_is_rejected(self):
        """A tampered/invalid JWT token returns 401."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken.abc.xyz")
        response = self.client.get("/api/conversations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)