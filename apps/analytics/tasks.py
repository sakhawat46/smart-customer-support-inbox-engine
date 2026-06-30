from celery import shared_task

from apps.conversations.models import Conversation


@shared_task
def analyze_sentiment(conversation_id):

    conversation = Conversation.objects.get(id=conversation_id)

    last_message = conversation.messages.last()

    if not last_message:
        return

    text = last_message.message.lower()

    positive_words = [
        "thanks",
        "thank you",
        "great",
        "good",
        "awesome",
        "excellent",
    ]

    negative_words = [
        "refund",
        "bad",
        "angry",
        "terrible",
        "poor",
        "worst",
    ]

    if any(word in text for word in positive_words):
        conversation.sentiment = Conversation.Sentiment.POSITIVE

    elif any(word in text for word in negative_words):
        conversation.sentiment = Conversation.Sentiment.NEGATIVE

    else:
        conversation.sentiment = Conversation.Sentiment.NEUTRAL

    conversation.save(update_fields=["sentiment"])