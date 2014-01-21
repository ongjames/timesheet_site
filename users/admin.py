from django.contrib import admin
from users.models import UserProfile,PrivateMessage

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PrivateMessage)