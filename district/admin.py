from django.contrib import admin
from .models import UserProfile, NeighbourHood, Business, Post
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(NeighbourHood)
admin.site.register(Business)
admin.site.register(Post)