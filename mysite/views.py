from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm
from .forms import UserPlan
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.contrib.auth import(
authenticate,
get_user_model,
login,
logout,
)
from .forms import UserLoginForm,UserRegisterForm,UserChangeForm,PlanForm

def login_view(request):
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username, password=password)
        login(request,user)
        return redirect("mysite/")
    return render(request,'login_form.html',{'form':form})


def register_view(request):
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user=authenticate(username=user.username, password=password)
        login(request,new_user)
        return redirect("mysite:index") #it means in mysite app go to index.html, like this only happen when we use redirect.

    return render(request,'reg_form.html',{'form':form}) #if form not valid again stay in same page that means goto reg_form.html


def logout_view(request):
    logout(request)
    return redirect("/")
    #return render(request,'reg_form.html',{})

@login_required(login_url='/')  #this is for login compulsory for opening site, for this we should also import login_req at top
def index(request):
    post_list=Post.objects.all().order_by("-published_date")

    paginator = Paginator(post_list, 10)  # this three lines for pagination(to go to nxt page,previous page)
    page = request.GET.get('page')            # this we can find in django documentation(search as 'pagination')
    present_page = paginator.get_page(page)  #no need of pagination if we need continous feeds while scrolling
                         #pagination is just to set number of posts per page, if that many posts over we need to press next page

     #search
    query=request.GET.get("q") # this is needed when search bar is there q is the search result,once check index.html search bar code
                                 #above meaning is these searched word will store in 'query' keyword,to know about 'q' go to index.html
    if query:  #(means if any word is searched)
        post_list=post_list.filter(Q(title__icontains=query)|#post_list is all posts, now what i did is,all posts filtered with searched word
                                   Q(content__icontains=query)|  # is again stored in post_list so that will print
                                   Q(user__first_name__icontains=query)| #this happens only when 'if query' means if there is any searched word
                                   Q(user__last_name__icontains=query) # if there is no word searched,post_list contain every post

                                    )
 #at above there is new one called 'Q', if we want to search with only one thing like title or contect that means only one things
   # then no need of 'Q' we can directly write as post_list=post_list.filter(title__icontains=query)
   #but if we want to search with more than one like title,content,date,user name, then  we need to use 'Q' and also '|' b/w every thing.
   # befor that we need to import Q at top.
   #while we are searching with user name we need to mention first name or last name as (user__first_name__icontains=query) otherwise 'user'search
   # wont work

    context={
    "post_list":post_list,
    "present_page":present_page,
    }
    return render(request,"index.html",context)



@login_required(login_url='/')
def detail(request,id):
     instance=Post.objects.get(id=id)
     return render(request,"detail.html",{"instance":instance})


@login_required(login_url='/')
def create(request):
    form=PostForm(request.POST or None,request.FILES or None ) #if 'request.FILES or None' not given then while creating the post dynimically
    if form.is_valid():                                #it wont take image when user uploaded(in form), we have to add image in admin page
        new=form.save()
        messages.success(request,"successfully posted")
        return HttpResponseRedirect(new.get_absolute_url())

    return render(request,"forms.html",{"form":form})



@login_required(login_url='/')
def plans_view(request):  
    form=UserPlan(request.POST or None,request.FILES or None )
    if form.is_valid():                   #it wont take image when user uploaded(in form), we have to add image in admin page
        form.save()
        messages.success(request,"successfully posted")
        return render(request,"plans.html",{"form":form})
    
    return render(request,"plans.html",{"form":form})

@login_required(login_url='/')
def update(request,id):  #we request 'id' when there is 'id' in url
    instance=Post.objects.get(id=id)         #when we are using get(id) we need to store in same keyword every where
                                                          #like line 14 and 25
    form=PostForm(request.POST or None, request.FILES or None ,instance=instance )# instance=instance is used so that previous data of that
    if form.is_valid():                  #perticular post will be saved then we can edit on that,with out writing from first onwards
        edit=form.save()
        messages.success(request,"saved")
        return HttpResponseRedirect(reverse('mysite:detail',args=(edit.id,))) #it happen when we click respected button
           # (we can also use) return HttpResponseRedirect(edit.get_absolute_url())
           #to work above any two, app_name in urls.py(in app) should be given

    context={
    "instance":instance,
    "form":form,
    }
    return render(request,"forms.html",context)


@login_required(login_url='/')
def delete(request,id):
    instance=Post.objects.get(id=id)
    instance.delete()
    messages.success(request,"successfully deleted")
    return redirect('mysite:index') # it means it come back to index in mysite app

@login_required(login_url='/')
def profile_index(request):
    user = request.user
    user_posts = Post.objects.filter(user=request.user).order_by('-published_date')
    query=request.GET.get("q") # this is needed when search bar is there q is the search result,once check index.html search bar code
                                 #above meaning is these searched word will store in 'query' keyword,to know about 'q' go to index.html
    if query:  #(means if any word is searched)
        user_posts=user_posts.filter(Q(title__icontains=query)|#post_list is all posts, now what i did is,all posts filtered with searched word
                                   Q(content__icontains=query)|  # is again stored in post_list so that will print
                                   Q(user__first_name__icontains=query)| #this happens only when 'if query' means if there is any searched word
                                   Q(user__last_name__icontains=query) # if there is no word searched,post_list contain every post
                                    )
    context={
    'user':user,
    'user_posts':user_posts,
    }
    return render(request,"profile_index.html",context)

@login_required(login_url='/')
def profile_detail(request,id):
    instance=Post.objects.get(id=id)
    return render(request,"profile_detail.html",{"instance":instance})

@login_required(login_url='/')
def edit_profile(request):
        user=request.user
        user_posts = Post.objects.filter(user=request.user).order_by('-published_date')
        form=UserChangeForm(request.POST or None,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mysite:profile_index')
        else:
            form=UserChangeForm(instance=request.user)

            query=request.GET.get("q") # this is needed when search bar is there q is the search result,once check index.html search bar code
                                         #above meaning is these searched word will store in 'query' keyword,to know about 'q' go to index.html
            if query:  #(means if any word is searched)
                user_posts=user_posts.filter(Q(title__icontains=query)|#post_list is all posts, now what i did is,all posts filtered with searched word
                                           Q(content__icontains=query)|  # is again stored in post_list so that will print
                                           Q(user__first_name__icontains=query)| #this happens only when 'if query' means if there is any searched word
                                           Q(user__last_name__icontains=query) # if there is no word searched,post_list contain every post
                                            )
             #above search one(query) is writing for every view if we want to search in every page
            context={
            'user':user,
            'user_posts':user_posts,
            'form':form
            }
            return render(request,'edit_profile.html',context)

@login_required
def other_profile(request,username):
    user = User.objects.get(username=username) #to get perticular user
    user_posts = Post.objects.filter(user=user).order_by('-published_date')
        #if we write user=request.user it will again take only logged in user posts
    context={
    'user':user,
    'user_posts':user_posts,
    }
    return render(request,"other_profile.html",context)
