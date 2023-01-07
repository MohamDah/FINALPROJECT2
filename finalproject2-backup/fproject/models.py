from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)

    def is_valid_friend(self):
        return self not in self.friends.all() 

class friend_request(models.Model):
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sents")
    requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieveds")

    def is_valid_request(self):
        return self.requestor != self.requested


class message(models.Model):
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="smessages")
    message_reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rmessages")
    message = models.CharField(max_length=500)
    date = models.DateTimeField()

    def serialize(self):
        return {
            "id": self.id,
            "message_sender": self.message_sender.username,
            "message_reciever": self.message_reciever.username,
            "message": self.message,
            "date": self.date.strftime("%b %d %Y, %I:%M %p")
        }
