from django.contrib import admin
from .models import Message, User, Follow, Likes

# Register your models here.
admin.site.register(Message)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Likes)