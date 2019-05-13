from django import forms
from .models import Post
from .models import UserPlan
from .models import Plan
from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth import(
authenticate,
get_user_model,
login,
logout,
)

User=get_user_model()

class PostForm(forms.ModelForm):
     class Meta:
         model=Post
         fields=[
         "user",
         "title",
         "content",
         "image",
         ]

class UserPlan(forms.ModelForm):
    class Meta:
         model=UserPlan
         fields=[
         "user",
         "plan"
         ]

class PlanForm(forms.ModelForm):
    class Meta:
        model=Plan
        fields=[
            's_limit',
            'l_limit',
            'c_limit'
        ]
#------------------------------------------------------------------------------------------------------------#

class UserRegisterForm(forms.ModelForm): #not working there are errors white registering,so avoid whole registration class
    email=forms.CharField(label='Email Addrress')
    email2=forms.CharField(label='confirm Email')
    #this is to, if we want to add any extra block or same block 2nd time like confirm password, confirm email

    password=forms.CharField(widget=forms.PasswordInput)

      #widget is to display dots in password

      #username no need to store it is automatically taken and it will check whether any username matches before
      #if any username matches same it wont accept taking while registration , so we need notto write as email matches so
      #dont take like tat

    class Meta:
        model=User
        fields=[
        "username",
        "first_name",
        "last_name",
        "email",
        "email2",
        "password",

        ]

    def clean (self, *args, **kwargs):  #clean should be define, if want ti raise warning messages
        email=self.cleaned_data.get('email')
        email2=self.cleaned_data.get('email2')
        if email!=email2:   #in the same way we can take two passwords also as passord and confirm password
            raise forms.ValidationError("email Does Not Match")

        email_qs=User.objects.filter(email=email)
        if email_qs.exists():        #if this email is already existed in databate it will check
            raise forms.ValidationError("Email already exists")
        return super(UserRegisterForm,self).clean(*args, **kwargs)

        #we should write manually for email,phonenumber..etc for not to match to any others details
        #but for username we need not to write it wont accept same username while registration itself
        #but for email and anything we should write code to not to accept during registration

      # actually ValidationError messages are not working remaing all are working,but this is the correct process for error messages

    #----------------------------------------------------------------------------------------------------------#
class UserLoginForm(forms.Form):  #cool its working
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
           #widget means password appears as dots
    def clean(self, *args, **kwargs):    #clean is to store req values and rise warning messages after checking taken values
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")

        if username and password:   #if usename and password submitted by any user
            user=authenticate(username=username, password=password) #check usename and password matching
            if not user:      # if entered username is not there
                raise forms.ValidationError("User not found")
            if not user.check_password(password):   #if username is there but password not matches to tthat username
                raise forms.ValidationError("Wrong password")
        return super(UserLoginForm,self).clean(*args,**kwargs)

class UserChangeForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
        "username",
        "first_name",
        "last_name",
        "email",
        "password",
        ]
