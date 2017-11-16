from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from .forms import *
from .method import *

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user:
                request.session['username'] = username
                return redirect('home')
            else:
                form = LoginForm()
                parameters = {
                    'form':form,
                }
                return render(request, 'users/login.html', parameters)
    else:
        form = LoginForm()
        parameters = {
            'form':form,
        }
        return render(request, 'users/login.html', parameters)

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            verify = cd['verify']
            email = cd['email']
            valid_user = User.objects.filter(username = username).first()
            if valid_user:
                return redirect('login')
            if password == verify:
                secure_password = make_password(password)
                user = User.objects.create(
                    username = username,
                    password = secure_password,
                    email = email,
                )
                login(request, user)
                return redirect('home')
            else:
                form = SignupForm()
                parameters = {
                    'form':form,
                }
                return render(request, 'users/signup.html', parameters)
    else:
        form = SignupForm()
        parameters = {
            'form':form
        }
        return render(request, 'users/signup.html', parameters)

def profile(request):
    if request.method == 'POST':
        cheese = 'cheese'
        return redirect('test')
    else:
        form = ProfileForm()
        parameters = {
            'form':form,
        }
        return render(request, 'users/profile.html', parameters)

def verify_personal(request):
    if request.method == 'POST':
        cheese = 'cheese'
        return redirect('test')
    else:
        form = VerifyPersonalForm()
        parameters = {
            'form':form,
        }
        return render(request, 'users/personal.html', parameters)

def verify_business(request):
    if request.method == 'POST':
        cheese = 'cheese'
        return redirect('test')
    else:
        form = VerifyBusinessForm()
        parameters = {
            'form':form,
        }
        return render(request, 'users/business.html', parameters)

@login_required(login_url='/signup/')
def user_home(request):
    return render(request, 'users/home.html')

def user_logout(request):
    logout(request)
    return redirect('login')
