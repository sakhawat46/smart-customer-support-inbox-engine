from django.urls import path

from .views import SuggestionAPIView

urlpatterns = [
    path("conversations/<int:pk>/suggest-reply/", SuggestionAPIView.as_view(), name="suggest-reply"),
]