from django.shortcuts import render
from auth_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

#---index view function--------------
def index(request):
    return render(request, 'auth_app/index.html')


#---example of a specisl page to display log status----
@login_required
def special(request):
    return HttpResponse('You are login. Thanks!')

#----user-logout view function-------
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth_app:index'))


#---registration view function-------------
def register(request):
    
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        
        if user_form.is_valid and profile_form.is_valid:
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user 
            
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()
            
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        
    return render(request, 'auth_app/registration.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })
    
    
#---login view function------------
def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                #return HttpResponse('Login Successfull!')
                return HttpResponseRedirect(reverse('auth_app:index'))
            
            else:
                return HttpResponse('Account is Not activated!')
        else:
            print('someone tried to login and failed!')
            print(f'usename: {username} and password provide: {password}')
            return HttpResponse('Invalide login detail supplied!')
    
    else:
        return render(request, 'auth_app/login.html', {})