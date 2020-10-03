from django.contrib.auth.models import AbstractUser
from datetime import datetime  
from django.db import models


class User(AbstractUser):
    pass

class Message(models.Model):
    body = models.CharField(max_length=100, blank=True)   
    date = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)    
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='followed')

class Likes(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='user')
    message = models.ForeignKey(Message, default=None, on_delete=models.CASCADE, related_name='message')
