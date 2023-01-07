from django.contrib import admin
from .models import User, friend_request, message

# Register your models here.
admin.site.register(User)
admin.site.register(friend_request)
admin.site.register(message)
