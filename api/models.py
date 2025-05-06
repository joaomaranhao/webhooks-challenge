from django.db import models


class Conversation(models.Model):
    STATE_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
    ]
    id = models.UUIDField(primary_key=True, editable=False)
    state = models.CharField(max_length=6, choices=STATE_CHOICES, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.state}"


class Message(models.Model):
    TYPE_CHOICES = [
        ("SENT", "Sent"),
        ("RECEIVED", "Received"),
    ]
    id = models.UUIDField(primary_key=True, editable=False)
    direction = models.CharField(max_length=8, choices=TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField()
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.timestamp} - {self.direction} - {self.content[:20]}..."
