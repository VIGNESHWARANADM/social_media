from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile,Post,LikePost,FollowersCount
from django.template import loader
from itertools import chain

# Create your views here.
@login_required(login_url='signin')
def index(request):
   user_object = User.objects.get(username=request.user.username)
   user_profile = Profile.objects.get(user=user_object)

   user_following_list = []
   feed = []

   user_following = FollowersCount.objects.filter(user=request.user.username)

   for following_memebers in user_following:
       user_following_list.append(following_memebers.following)
   for following_member_posts in user_following_list:
       feed_list = Post.objects.filter(user=following_member_posts)
       feed.append(feed_list)
   feed_lists = list(chain(*feed))
 

   user_object1 = User.objects.exclude(username='vigneshbaskaran')
   user_following_object = FollowersCount.objects.filter(user=request.user)
   user_following = []
   user_not_following = []
   for i in user_following_object:
       user_following.append(i.following)
   for i in user_object1:
       if (i != request.user) and (i.username not in user_following):
           user_not_following.append(Profile.objects.filter(user=i))
   user_not_following =list(chain(*user_not_following))
#    return HttpResponse(user)
   return render(request,'index1.html',{'user_profile': user_profile,'posts':feed_lists,'user_not_following':user_not_following})
def signup(request): 
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
   
         
        if password == password2:
           if User.objects.filter(email=email).exists():
               messages.info(request,'email taken')
               return redirect('signup')
           elif User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('signup')
           else:
               user = User.objects.create_user(username=username,password=password,email=email)
               user.save()
               user_login=auth.authenticate(username=username,password=password)
               auth.login(request,user_login)
               user_model = User.objects.get(username=username)
               
               new_profile = Profile.objects.create(user = user_model,id_user =user_model.id)
               new_profile.save()
               return redirect('settings')
        else:
            messages.info(request,'password not matching')
            return redirect('signup')
        
    else:
       return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
        
    else:
        return render(request,'signin.html')
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')    

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image')== None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image')!= None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            return redirect('settings')
       
    return render(request,'setting.html',{'user_profile':user_profile})

def sample(request):
    #if request.method == 'POST':
    follower = request.POST['follower']
    #user=request.POST['user']
    return render(request,'sample.html',{'user':follower})
 
    
    #return render(request,'sample.html',{'user':user})
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()

         
        return redirect('/')
    else:
        return redirect('/')
@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter= LikePost.objects.filter(post_id=post_id,username=username).first()
    if like_filter == None:
       new_like = LikePost.objects.create(username=username,post_id=post_id)
       new_like.save()
       post.no_of_likes = post.no_of_likes+1
       post.save()
       return redirect('/')
    else :
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    user = User.objects.get(username=request.user)

    if FollowersCount.objects.filter(user=user.username,following=user_object.username).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
      
    user_following= len(FollowersCount.objects.filter(following=user.username))
    user_followers= len(FollowersCount.objects.filter(following=pk))
    
    context = {
        'user_object':user_object,
        'user_posts':user_posts,
        'user_profile':user_profile,
        'user_post_length' :user_post_length,
        'user':user,
        'button_text':button_text,
        'user_following':user_following,
        'user_followers':user_followers

 
    }
    return render(request,'profile.html',context)
    #return render(request,'sample.html',context)
@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
       following = request.POST['following']
       user=request.POST['user']
        
       
       if FollowersCount.objects.filter(following = following,user=user).first():
            delete_follower = FollowersCount.objects.get(following = following,user=user)
            delete_follower.delete()
            return redirect('/profile/'+following)
       else:
            new_follower = FollowersCount.objects.create(following = following,user=user)
            new_follower.save()
            return redirect('/profile/'+following)
    else:
       return redirect('/')   
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.filter(user=user_object)
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username=username)
        username_profile=[]
        
        
        for users in username_object:
            username_profile.append(Profile.objects.filter(user=users))
        username_profile=list(chain(*username_profile))
        return render(request,'search.html',{'username_profile':username_profile,'username':username})
       


        
    return render(request,'search.html')
def sug(request):
   user_object1 = User.objects.exclude(username='vigneshbaskaran')
   user_following_object = FollowersCount.objects.filter(user=request.user)
   user_following = []
   user_not_following = []
   for i in user_following_object:
       user_following.append(i.following)
   for i in user_object1:
       if (i != request.user) and (i.username not in user_following):
           user_not_following.append(Profile.objects.filter(user=i))
   user_not_following =list(chain(*user_not_following))
  
   return render(request,'sample.html',{'user_not_following':user_not_following})