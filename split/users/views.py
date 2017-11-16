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
