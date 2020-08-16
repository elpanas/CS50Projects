from django.contrib.auth.models import AbstractUser
from datetime import datetime   
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=30, default=None, unique=True)
    description = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=15, blank=True)  
    best_bid = models.DecimalField(decimal_places=2, default=None, max_digits=7)  
    deadline = models.DateField(default=datetime.now)
    image_addr = models.URLField(blank=True)    
    seller = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

class Bids(models.Model):    
    bid = models.DecimalField(decimal_places=2, default=None, max_digits=7)
    bidder = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, default=None, on_delete=models.CASCADE)

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, default=None, on_delete=models.CASCADE)

class Comments(models.Model):
    title = models.CharField(max_length=20, default=None)
    content = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(default=datetime.now)
    auction = models.ForeignKey(Auction, default=None, on_delete=models.CASCADE)