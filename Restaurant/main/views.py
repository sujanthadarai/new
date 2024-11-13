import re

from django.shortcuts import render,redirect
from .models import Momo
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm

# Create your views here.
@login_required(login_url='log_in')
def index(request):
    buf=Momo.objects.filter(category='buf')
    chicken=Momo.objects.filter(category='chicken')
    veg=Momo.objects.filter(category='veg')
    
    context={
        'buf':buf,
        'chicken':chicken,
        'veg':veg,
       
        }
    return render(request,'main/index.html',context)
def about(request):
    return render(request,'main/about.html')
def contact(request):
    return render(request,'main/contact.html')

@login_required(login_url='log_in')
def menu(request):
    return render(request,'main/menu.html')
def service(request):
    return render(request,'main/services.html')

'''
===========================================================================
===========================================================================
                   authentication part
===========================================================================
===========================================================================

'''
# regular expression

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']
        
        if password==password1:
            
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username is already exists!!!')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'email is already exists!!!')
                    return redirect('register')
                
                elif not re.search(r'[A-Z]',password): #ramm710@
                    messages.error(request,"your password must contain at least uppercase")
                    return redirect('register')
                elif not re.search(r'\d',password):
                    messages.error(request,'your password must contain at least one digit')
                    return redirect('register')
                elif username.lower() in password.lower():
                    messages.error(request,'your password doesnot similar to username')
                    return redirect('register')
                    
                else:  
                    User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                    messages.success(request,'register successfully!!!')
                    return redirect('log_in')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
        else:
            messages.error(request,'Your password and confirm password doesnot match!!!')
            return redirect('register')
        
        
    return render(request,'auth/register.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username') #david710
        password=request.POST.get('password') #sujan
        remember_me=request.POST.get('remember_me') #true
      
        if not User.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet')
            return redirect('log_in')
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            if remember_me:#true
                request.session.set_expiry(1200000)
            else:
                request.session.set_expiry(0)
           
            messages.success(request,'Login successfullt !!!')
            return redirect('index')
        else:
            messages.error(request,'Invalid keywords!!!')
            return redirect('log_in')
        
            
    return render(request,'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')      
    
    return render(request,'auth/change_password.html',{'form':form})