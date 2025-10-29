from urllib import request
from django import template
from django import core
from core.models import LikesPost,Post,Profile,Follow
from django.contrib.auth.models import User


register = template.Library()

@register.filter(name='isLiked')
def isLiked(post_id,username):
    # username = request.user.username
    isLiked = LikesPost.objects.filter(post_id = post_id,username=username).first()
    if isLiked == None:
        return False
    else:
        return True

@register.filter(name='isFollowed')
def isFollowed(flwing_username,username):
    # username = request.user.username
    isFollowed = Follow.objects.filter(following_username = flwing_username,follower_username=username).first()
    if isFollowed == None:
        return False
    else:
        return True

@register.filter(name='get_by_post')
def get_by_post(post_id):
    post = Post.objects.filter(id=post_id).first()
    
    username = post.username
    
    profile_obj = Profile.objects.filter(username=username).first()
    username = profile_obj.username
    return profile_obj

@register.filter(name='get_by_name')
def get_by_name(username):   
    profile_obj = Profile.objects.filter(username=username).first()
    return profile_obj

