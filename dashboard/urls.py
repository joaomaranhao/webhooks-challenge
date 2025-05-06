from django.urls import path

from . import views

urlpatterns = [
    path("", views.conversations_view, name="conversations"),
    path(
        "messages/<uuid:conv_id>/",
        views.conversation_detail,
        name="conversation_detail",
    ),
]
