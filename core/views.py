from multiprocessing import context
from unittest import result
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required #
from django.contrib.auth import authenticate, login,logout 
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import uuid
from .models import Follow, Profile,Post,LikesPost,Notification,Comment,Message,Messenger
from .helpers import verify_account_sendmail,forget_pass_sendmail
from django.utils.timezone import utc
from django import template
from itertools import chain
import random
from operator import attrgetter
from operator import itemgetter




# Create your views here.


#Signin
def signin(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid User')
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
 
#For Verifying Email
def verify_email(request,token):

    if Profile.objects.filter(auth_token = token).exists():                     #checking if the token exists

      profile_obj = Profile.objects.filter(auth_token = token).first()   #getting the profile object via token
      user_obj = User.objects.get(username=profile_obj.username)
      user_obj.is_active=True                                              #Put the user in active mode

      profile_obj.is_verified = True                                    #Put the user in active mode 
      user_obj.save()
      profile_obj.save()
      
      #auto login and direct to welcome Setting Page
    #   username = user_obj.username
    #   password = user_obj.password
    #   print(password)
    #   user = us

    #   if user is not None:
    #         auth.login(request,user)
    #         return redirect('home')
    #   else:
    #         messages.info(request, 'Invalid User')
    #         return redirect('signin')
      user_log = user_obj
      auth.login(request,user_log)
      
    #   messages.info(request, 'Account Has Been Verified.')
    #   return redirect(f'/verify_email/{token}/')
      return redirect('welcomeSettings')                                        
    else:       
      return render(request,'verify_email.html')


#Create a new account
def signup(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # print("ELLO")
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                user= User.objects.filter(email=email).first()
                user_profile = Profile.objects.filter(email=email).first()
                if user.is_active== True:
                    messages.info(request, 'Email Taken')
                    return redirect('signup')
                else:
                    verify_token = user_profile.auth_token
                    verify_account_sendmail(user.email,verify_token)
                    messages.info(request,'An email has been sent again')
                    return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,password=password, email=email)
                user.is_active=False
                user.save()
                verify_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user , username=username,auth_token = verify_token,id_user = user.id,email=email)
                profile_obj.save()
                verify_account_sendmail(user.email,verify_token)
                messages.info(request,'An email has been sent')               
                return redirect('signup')
        else:
            messages.info(request, 'Password dont match')
            return redirect('signup')
    else:
        return render(request,'signup.html')


#logout from site
@login_required(login_url='signin')
def logout_view(request):
    logout(request)
    return redirect('signin')
   

@login_required(login_url='signin')
def welcomeSettings(request):
    profile_obj = Profile.objects.get(user = request.user)
    context = {
        'user_profile' : profile_obj,    
    }

    if request.method=='POST':
        if request.FILES.get('image') == None:
            image = profile_obj.profileimg
        else:
            image = request.FILES.get('image')
            
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']        
        bio = request.POST['bio']
        country = request.POST['country']
        gender = request.POST['gender']
        dob = request.POST['dateofbirth']


        #saving the Profile
        profile_obj.gender = gender
        profile_obj.profileimg = image
        profile_obj.bio = bio
        # profile_obj.gender
        profile_obj.country = country
        profile_obj.dob = dob
        profile_obj.firstname = firstname
        profile_obj.lastname = lastname

        
        #changing the auth token also generating forgot pass token
        auth_token = str(uuid.uuid4())
        forget_pass_token = str(uuid.uuid4())
        profile_obj.auth_token = auth_token
        profile_obj.forget_pass_token = forget_pass_token

        profile_obj.save()
        username = profile_obj.username
        return redirect(f'profile/{username}')
    else:  
        return render(request,'welcomeSettings.html',context)


@login_required(login_url='signin')
def accountSettings(request):
    profile_obj = Profile.objects.get(user = request.user)
    context = {
        'user_profile' : profile_obj,    
    }

    if request.method=='POST':
        if request.FILES.get('image') == None:
            image = profile_obj.profileimg
        else:
            image = request.FILES.get('image')
            
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']        
        bio = request.POST['bio']
        country = request.POST['country']
        gender = request.POST['gender']
        dob = request.POST['dateofbirth']


        #saving the Profile
        profile_obj.gender = gender
        profile_obj.profileimg = image
        profile_obj.bio = bio
        profile_obj.gender
        profile_obj.country = country
        profile_obj.dob = dob
        profile_obj.firstname = firstname
        profile_obj.lastname = lastname

        
        #changing the auth token also generating forgot pass token

        profile_obj.save()
        return redirect('accountSettings')
    else:  
        return render(request,'accountSettings.html',context)

#User Profile page
@login_required(login_url='signin')
def profile(request):
    profile_obj= Profile.objects.get(user = request.user)
    posts = Post.objects.all().order_by('posted_at')
    like = LikesPost.objects.all()
    context = {
        'user_profile' : profile_obj,
        'posts' : posts,   
        'like' : like 
    }
   
    return render(request,'profile.html',context)


@login_required(login_url='signin')
def profiletest(request,name):
    user_object = request.user
    username = request.user.username
    profile_obj = Profile.objects.filter(username = username).first() #browsing user
    view_user_object = User.objects.filter(username = name)   
    view_profile_object = Profile.objects.filter(username = name).first()#Profile User
    # print(view_profile_object)
    # print(name)
    posts = Post.objects.filter(username = name).order_by('posted_at')
    context = {
        'profile_obj' : profile_obj,
        'view_user_object' : view_user_object,
        'user_object' : user_object,   
        'view_profile_object' : view_profile_object,
        'posts' : posts, 
    }
 
    return render(request,'profiletest.html',context)


@login_required(login_url='signin')
def about(request,name):
    profile_obj= Profile.objects.get(username = name)
    context = {
        'user_profile' : profile_obj,    
    }
    return render(request,'about.html',context)




#Default Home Page
@login_required(login_url='signin')
def home(request):
    profile_obj = Profile.objects.get(user = request.user)
    # posts = Post.objects.all()
    likes = LikesPost.objects.all()
    # print(likes)
     
    user_following_username = []
    posts = []

    user_following = Follow.objects.filter(follower_username = profile_obj.username)

    for users in user_following:
        user_following_username .append(users.following_username)
        post_list = Post.objects.filter(username = users.following_username)
        posts.append(post_list)

    post = list(chain(*posts))
    post.sort(key=lambda x: x.posted_at)

    #suggestion
    suggestion_list = []
    suggestion = []
    all_user = Profile.objects.all()
    # print(all_user)
    for u in all_user:
        if u not in list(user_following) and u.username != profile_obj.username:
            s_list = Profile.objects.filter(username = u.username)
            suggestion_list.append(s_list)
    random.shuffle(suggestion_list)
    suggestion = list(chain(*suggestion_list))


    context = {
        'user_profile' : profile_obj,
        'posts' : post,
        'likes' : likes ,
        'suggestion' : suggestion[:4]  
    } 
    return render(request,'home.html',context)  

#If Password is forgotten
def forgetPassword(request):
    if request.method=='POST':
        username = request.POST['username'] 

        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username) #create a object of the user
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            forget_pass_sendmail(user_obj.email ,token)
            profile_obj.forget_pass_token = token
            profile_obj.save()
            messages.info(request,'An email has been sent')
            return redirect('forgetPassword')

        else:
            messages.info(request, 'No User Found.')
            return redirect('forgetPassword')
    else:
        return render(request,'forgetPassword.html')

#reset the password --->> forgetpassword
def resetPassword(request,token):
        
        # context = {'user_id' : profile_obj.user.id}
        
    if request.method == 'POST':
            profile_obj = Profile.objects.filter(forget_pass_token = token).first()
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('password2')

            #checking if the password match      
            if  new_password != confirm_password:
                messages.info(request, 'Password do not match!!')
                return redirect(f'/resetPassword/{token}/')
            

            username = profile_obj.username        
            # user_id = profile_obj.user.name
            user_obj = User.objects.get(username=username)
            user_obj.set_password(new_password)

            user_obj.save()

            #changing the token again
            token = str(uuid.uuid4())
            profile_obj.forget_pass_token = token
            profile_obj.save()
            return redirect('signin')
    else:
        return render(request,'resetPassword.html')

@login_required(login_url='signin')
def changePassword(request):
    user_obj = request.user
    username = user_obj.username
    # messages.info(request, user_obj.username)
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if  new_password != confirm_password:
            messages.info(request, 'Password do not match!!')
            return redirect('changePassword')
        else:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
               user_obj.set_password(new_password)
               user_obj.save()
               return redirect('signin')
            else:
               messages.info(request, 'Incorrect Password')
               return redirect('changePassword')

    else:
        return render(request,'changePassword.html')


@login_required(login_url='signin')
def upload(request,name):
    user_obj = request.user
    username = user_obj.username
    profile_obj = Profile.objects.filter(username = username).first()
    if request.method == 'POST':
        # user = request.user
        image  = request.FILES.get('image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user_post = user_obj,post_image=image,caption=caption,username=username,profileimg = profile_obj.profileimg)
        text = "Has Liked Your "
        type = "Like"
        new_not = Notification.objects.create(new_notification = profile_obj,user_from = username,user_to = profile_obj.username,type = type , text = text)
        profile_obj.notifications = profile_obj.notifications+1
        new_not.save()
        new_post.save()
        profile_obj.posts =profile_obj.posts+1
        profile_obj.save()
        return redirect(f'/profile/{username}')
    else:
        return redirect(f'/profile/{username}')

    

@login_required(login_url='signin')
def like(request):
    username = request.user.username
    post_id = request.GET.get('id')
    post = Post.objects.filter(id=post_id).first()
    post_username = post.username
    post_user_profile = Profile.objects.filter(username = post_username).first()
    isLiked = LikesPost.objects.filter(username=username,post_id = post_id).first()

    if isLiked == None:
        new_like = LikesPost.objects.create(like=post,post_id=post_id,username=username)
        text = "Has Liked Your "
        type = "Like"
        new_not = Notification.objects.create(new_notification = post_user_profile,user_from = username,user_to = post.username,type = type , text = text,post_id = post_id)
        post_user_profile.notifications = post_user_profile.notifications+1
        post_user_profile.save()
        new_not.save()
        new_like.save()
        post.likes = post.likes+1
        post.save()
        value = 1
    else:
        unlike  = LikesPost.objects.filter(username = username,post_id=post_id).first()
        unlike.delete()
        post.likes = post.likes-1
        post.save()
        value = 0
    likedby = post.likes
    context={
        'value':value,
        'likedby':likedby
     }
    # return HttpResponseRedirect(request.path_info)
    # return redirect(request.path)
    # return redirect('home')
    return JsonResponse(context)

@login_required(login_url='signin')
def deletepost(request):
    username = request.user.username
    post_id = request.GET.get('id')
    post = Post.objects.get(id=post_id)
    post.delete()
    profile_obj = Profile.objects.filter(username = username).first()
    profile_obj.posts =profile_obj.posts-1
    profile_obj.save()
    return redirect(f'/profile/{username}')


@login_required(login_url='signin')
def follow(request):
    follower_name = request.user.username
    following_name = request.GET.get('name')
    follower_profile = Profile.objects.filter(username = follower_name).first()
    following_profile = Profile.objects.filter(username = following_name).first()
    isfollowed = Follow.objects.filter(follower_username=follower_name,following_username=following_name).first()

    if isfollowed == None:
        flw = Follow.objects.create(follower = follower_profile,follower_username=follower_name,following_username=following_name)
        follower_profile.following = follower_profile.following+1
        following_profile.follower = following_profile.follower+1
        flw.save()
        text = "Has Followed You"
        type = "Follow"
        new_not = Notification.objects.create(new_notification = following_profile,user_from = follower_name,user_to = following_name,type = type , text = text)
        following_profile.notifications = following_profile.notifications+1
        new_not.save()
        follower_profile.save()
        following_profile.save()
        new_messenger = Messenger.objects.create(username=follower_profile.username,friend=following_profile.username)
        new_messenger.save()
        return redirect(f'profile/{following_name}')
    else:
        isfollowed.delete()
        follower_profile.following = follower_profile.following-1
        following_profile.follower = following_profile.follower-1
        follower_profile.save()
        following_profile.save()
        messenger_obj = Messenger.objects.filter(username=follower_profile.username,friend=following_profile.username)
        messenger_obj.delete()
        return redirect(f'profile/{following_name}')


@login_required(login_url='signin')
def search(request):
    user_obj = request.user
    username = user_obj.username
    profile_obj = Profile.objects.filter(username = username).first()
    context = {}
    if request.method == 'POST':
        search_name = request.POST['search']
        search_profile= Profile.objects.filter(username__icontains = search_name)
        print(search_profile)
        if Profile.objects.filter(username__icontains = search_name).exists():
             context = {
           'user_profile' : profile_obj,
           'search_profiles' : search_profile,
           'Found' : True
           } 
           
        else:
            context = {
           'user_profile' : profile_obj,
           'Found' : False
            }
    else :
         context = {
           'user_profile' : profile_obj,
           'Found' : False
           } 
    return render(request,'search.html',context)  
        
def follower(request,name):
    user_obj = request.user
    username = user_obj.username
    profile_obj = Profile.objects.filter(username = username).first()
    found=True
    follower_list = []
    view_profile_obj = Profile.objects.filter(username = name).first()
    if view_profile_obj.follower == 0:
        found = False
    else:
        get_follower  = Follow.objects.filter(following_username=name)
        lists = []
    
        for prf in get_follower:
            x = Profile.objects.filter(username=prf.follower_username)
            # print(prf.follower_username)
            lists.append(x)

        
        follower_list = list(chain(*lists))


    context={

        'user_profile' : profile_obj,
         'name' : name,
         'found':found,
        'follower_list' : follower_list
    }

    return render(request,'follower.html',context)


def following(request,name):
    user_obj = request.user
    username = user_obj.username
    profile_obj = Profile.objects.filter(username = username).first()
    found=True
    follower_list = []
    view_profile_obj = Profile.objects.filter(username = name).first()
    if view_profile_obj.following == 0:
        found = False
    else:
        get_follower  = Follow.objects.filter(follower_username=name)
        lists = []
    
        for prf in get_follower:
            x = Profile.objects.filter(username=prf.following_username)
            # print(prf.follower_username)
            lists.append(x)

        
        follower_list = list(chain(*lists))


    context={

        'user_profile' : profile_obj,
         'name' : name,
         'found':found,
        'follower_list' : follower_list
    }

    return render(request,'following.html',context)


@login_required(login_url='signin')
def post(request,id):
    user_obj = request.user
    username = user_obj.username
    profile_obj = Profile.objects.filter(username = username).first()
    post_show = Post.objects.filter(id = id).first()
    comment = Comment.objects.filter(post_id=id)
    # print(comment)
    context = {
        'user_profile' : profile_obj,
        'post' : post_show,
        'comments':comment
    }
    return render(request,'post.html',context) 

def notification(request):
    user_obj = request.user
    username = user_obj.username
    profile_obj = Profile.objects.filter(username = username).first()
    found=True
    if profile_obj.notifications ==0:
        found = False
    new_notification = Notification.objects.filter(user_to=username)
    context = {
        'user_profile' : profile_obj,
        'notifications': new_notification,
        'found':found
    }
    for noti in new_notification:
        noti.delete()
    profile_obj.notifications = 0
    profile_obj.save()
    return render(request,'notification.html',context)

def Liked(request):
     username = request.user.username
     post_id = request.GET.get('id')
    #  print(post_id)
     isliked = LikesPost.objects.filter(username=username,post_id = post_id).first()
     post = Post.objects.filter(id=post_id).first()
     likedby = post.likes
    #  print(isliked)
     if isliked == None:
        value = 0
     else:
        value = 1
     context={
        'value':value,
        'likedby':likedby
     }
    #  print(value)
     return JsonResponse(context)



def comment(request):
     
     if request.method == 'POST':
        username = request.user.username
        text = request.POST['text']
        post_id = request.POST['id']
        # print(post_id)
        profile_obj = Profile.objects.filter(username = username).first()
        post = Post.objects.filter(id = post_id).first()
        new_comment = Comment.objects.create(new_comment=post,post_id=post_id,username=username,text=text)
        new_comment.save()
     context={
        'value':0,
     }
     return JsonResponse(context)


@login_required(login_url='signin')
def chat(request):
    username = request.user.username
    friendlist = Messenger.objects.filter(username=username)
    profile_obj = Profile.objects.filter(username=username).first()
    # for friend in friendlist:
    #     print(friend.friend)

    context = {
        'friendlist':friendlist,
        'profile_obj':profile_obj,
    }
    return render(request,'chat.html',context) 


def deleteComment(request):
    pass


def sendMessage(request):
    if request.method == 'POST':
        from_username = request.user.username
        text = request.POST['text']
        to_username = request.POST['name']
        # print(to_username)
        new_message = Message.objects.create(from_username=from_username,to_username=to_username,text=text)
        new_message.save()
        prf_obj = Profile.objects.filter(username=to_username).first()
        prf_obj.messages = prf_obj.messages+1
        prf_obj.save()

    context={
        'value':1,
     }
    return JsonResponse(context)

def getMessage(request):
    to_username = request.user.username
    from_username = request.GET.get('id')
    list1 = Message.objects.filter(from_username=from_username,to_username=to_username).values()
    list2 = Message.objects.filter(from_username=to_username,to_username=from_username).values()
    l1 = list(list1)
    l2 = list(list2)
    result_list = l1+l2
    newlist = sorted(result_list, key=lambda k: k['sends_at']) 
    # result_list = sorted(
    # chain(list1, list2),
    # key=attrgetter('sends_at'))
    # messages = list(result_list)
    # print(result_list)
    # context={
    #     'value':0,
    #     'messages':result_list
    #  }
    return JsonResponse({"messages":newlist})
