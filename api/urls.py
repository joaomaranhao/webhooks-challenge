from django.urls import path

from .views import ConversationDetailView, WebhookView

urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
    path(
        "conversation/<uuid:id>/",
        ConversationDetailView.as_view(),
        name="conversation_detail",
    ),
]
