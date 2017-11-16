from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import *
from .method import *

def login(request):
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

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            verify = cd['verify']
            email = cd['email']
            if password == verify:
                secure_password = make_password(password)
                user = User.objects.create(
                    username = username,
                    password = secure_password,
                    email = email,
                )
                request.session['username'] = username
                return redirect('test')
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

def home(request):
    user = loggedInUser(request)
    parameters = {
        'user':user,
    }
    return render(request, 'users/home.html', parameters)

def logout(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session['username']
        request.session.pop('username')
        return redirect('login')
