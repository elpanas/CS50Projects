from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.db import models

# Create your models here.
class User(AbstractUser): #aggiungi il flag per il gestore/bagnante
    is_manager = models.BooleanField(default = False)

class Estabs(models.Model):
    name = models.CharField(max_length=30, default=None)
    street = models.CharField(max_length=50, default=None)
    number = models.CharField(max_length=8, default=None)
    city = models.CharField(max_length=40, default=None)
    zipcode = models.IntegerField(default=None)    
    country = models.CharField(max_length=20, default=None)
    phone = models.CharField(max_length=15, blank=True, default=None)
    available = models.SmallIntegerField(default=None)
    umbrellas = models.SmallIntegerField(default=None)
    manager = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='manager')

class Booking(models.Model):
    estab = models.ForeignKey(Estabs, default=None, on_delete=models.CASCADE, related_name='bookestab')
    booker = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='bookuser')
    umb = models.IntegerField(default=1)
    date = models.DateTimeField(default=(datetime.now() + timedelta(days=1))) 

class Comment(models.Model): 
    body = models.CharField(max_length=100, default=None)   
    date = models.DateTimeField(default=datetime.now())  
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name = 'comuser')
    estab = models.ForeignKey(Estabs, null=True, default=None, on_delete=models.CASCADE, related_name = 'comestab')

class Favourite(models.Model):
    favestab = models.ForeignKey(Estabs, default=None, on_delete=models.CASCADE, related_name='favestab')
    favuser = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='favuser')
