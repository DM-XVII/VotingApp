from django.db import models
from django.contrib.auth.models import User
class Poll(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Option(models.Model):
    value = models.CharField(max_length=255)
    poll = models.ForeignKey('Poll',on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)


class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    poll = models.ForeignKey('Poll',on_delete=models.CASCADE)
    vote = models.ForeignKey('Option',on_delete=models.CASCADE)