from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import *

def test(request):
    return render(request, 'users/test.html')

def login(request):
    if request.method == 'POST':
        cheese = 'cheese'
        return redirect('test')
    else:
        form = LoginForm()
        parameters = {
            'form':form,
        }
        return render(request, 'users/login.html', parameters)

def signup(request):
    if request.method == 'POST':
        cheese = 'cheese'
        return redirect('test')
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
