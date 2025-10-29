from django.db import models
from ast import Pass
# from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime 
import uuid
from django.utils import timezone


# Create your models here.

User = get_user_model()

GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female')
    )

class Profile(models.Model):
  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30,default='user')
    email = models.EmailField(max_length=100,blank=True)
    auth_token = models.CharField(max_length=100,blank=True )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    # password = models.CharField(max_length=100)
    id_user = models.IntegerField()
    firstname = models.CharField(max_length=50,blank=True)
    lastname = models.CharField(max_length=50,blank=True)
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES,blank=True)
    phonenumber = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)
    dob = models.DateField(default=timezone.now) 
    forget_pass_token = models.CharField(max_length=100,blank=True)
    bio = models.TextField(blank=True,default='Hey its me')
    profileimg = models.ImageField(upload_to = 'profile_images',default='profilepic.jpg')
    location = models.CharField(max_length=100,blank=True)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)                       
    posts = models.IntegerField(default=0)
    notifications = models.IntegerField(default=0)
    messages = models.IntegerField(default=0)
    

    def __str__(self) :
        return self.user.username

    def get_age(self):
        age = datetime.date.today()-self.dob
        return int((age).days/365.25)


class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    # only_image = models.BooleanField(default=False)
    user_post = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=30,default='user')
    profileimg = models.ImageField(upload_to = 'profile_images',default='profilepic.jpg')
    post_image  = models.ImageField(upload_to = 'Post_image')
    caption = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now) 
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username


class LikesPost(models.Model):
    like = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,
        null=True)
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    likes_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower =  models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,
        null=True)
    follower_username = models.CharField(max_length=30)
    following_username = models.CharField(max_length=30)
    
    def __str__(self):
        return self.following_username

class Notification(models.Model):
    new_notification = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,
        null=True)
    user_from = models.CharField(max_length=30)
    user_to = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    post_id = models.CharField(max_length=100)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.user_to

class Comment(models.Model):
    new_comment = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,
        null=True)
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.post_id


class Message(models.Model):
    text = models.CharField(max_length=300)
    from_username = models.CharField(max_length=30)
    to_username = models.CharField(max_length=30)
    sends_at = models.DateTimeField(default=timezone.now)

class Messenger(models.Model):
     username = models.CharField(max_length=30)
     friend = models.CharField(max_length=30)

     def __str__(self):
        return self.username


