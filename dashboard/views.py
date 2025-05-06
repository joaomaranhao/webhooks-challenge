from django.shortcuts import render

from api.models import Conversation


def conversations_view(request):
    conversations = Conversation.objects.all()
    return render(
        request, "dashboard/conversations.html", {"conversations": conversations}
    )


def conversation_detail(request, conv_id):
    conversation = Conversation.objects.get(id=conv_id)

    # Assuming you have a related name 'messages' in your Conversation model
    return render(
        request,
        "dashboard/messages.html",
        {"conversation": conversation, "messages": ""},
    )
