from datetime import datetime, timezone
from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from api.models import Conversation, Message


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_new_conversation(client):
    conv_id = str(uuid4())
    response = client.post(
        "/webhook/",
        {
            "type": "NEW_CONVERSATION",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"id": conv_id},
        },
        format="json",
    )
    assert response.status_code == 200
    assert Conversation.objects.filter(id=conv_id).exists()


@pytest.mark.django_db
def test_new_message_sent(client):
    conv_id = uuid4()
    Conversation.objects.create(id=conv_id)

    msg_id = str(uuid4())

    response = client.post(
        "/webhook/",
        {
            "type": "NEW_MESSAGE",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "id": msg_id,
                "direction": "SENT",
                "content": "Olá!",
                "conversation_id": str(conv_id),
            },
        },
        format="json",
    )
    assert response.status_code == 200
    assert Message.objects.filter(id=msg_id).exists()


@pytest.mark.django_db
def test_cannot_add_message_to_closed_conversation(client):
    conv_id = uuid4()
    Conversation.objects.create(id=conv_id, state="CLOSED")

    response = client.post(
        "/webhook/",
        {
            "type": "NEW_MESSAGE",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "id": str(uuid4()),
                "direction": "RECEIVED",
                "content": "Teste",
                "conversation_id": str(conv_id),
            },
        },
        format="json",
    )
    assert response.status_code == 400
    assert "Conversation is closed" in response.data.get("error", "")


@pytest.mark.django_db
def test_close_conversation(client):
    conv_id = uuid4()
    conv = Conversation.objects.create(id=conv_id)

    response = client.post(
        "/webhook/",
        {
            "type": "CLOSE_CONVERSATION",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"id": str(conv_id)},
        },
        format="json",
    )
    assert response.status_code == 200
    conv.refresh_from_db()
    assert conv.state == "CLOSED"
