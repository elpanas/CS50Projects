from django.contrib import admin
from .models import User, Estabs, Favourite, Comment, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Estabs)
admin.site.register(Booking)
admin.site.register(Favourite)
admin.site.register(Comment)