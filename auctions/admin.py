from django.contrib import admin
from .models import User, Comments, Auction, Bids, Watchlist

admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Auction)
admin.site.register(Bids)
admin.site.register(Watchlist)

# Register your models here.
