from uuid import UUID

from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message
from .serializers import ConversarionSerializer


class WebhookView(APIView):
    def post(self, request):
        try:
            event_type = request.data.get("type")
            timestamp = request.data.get("timestamp")
            data = request.data.get("data")

            if event_type == "NEW_CONVERSATION":
                conversation_id = UUID(data["id"])
                Conversation.objects.get_or_create(id=conversation_id)

            if event_type == "NEW_MESSAGE":
                conversation_id = UUID(data["conversation_id"])
                try:
                    conversation = Conversation.objects.get(id=conversation_id)
                    if conversation.state == "CLOSED":
                        return Response(
                            {"error": "Conversation is closed"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    msg_id = UUID(data["id"])
                    Message.objects.create(
                        id=msg_id,
                        direction=data["direction"],
                        content=data["content"],
                        timestamp=parse_datetime(timestamp),
                        conversation=conversation,
                    )
                except Conversation.DoesNotExist:
                    return Response(
                        {"error": "Conversation not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            if event_type == "CLOSE_CONVERSATION":
                conversation_id = UUID(data["id"])
                try:
                    conversation = Conversation.objects.get(id=conversation_id)
                    conversation.state = "CLOSED"
                    conversation.save()
                except Conversation.DoesNotExist:
                    return Response(
                        {"error": "Conversation not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            return Response({"status": "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConversationDetailView(RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversarionSerializer
    lookup_field = "id"
