from django.contrib import admin
from .models import Profile,Post,LikesPost,Follow,Notification,Comment,Message,Messenger

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikesPost)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Messenger)
