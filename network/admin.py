from django.contrib import admin
from .models import User, Posts, Follow, Likes

# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Follow)
admin.site.register(Likes)