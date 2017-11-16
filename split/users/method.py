from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import *
from .method import *


def test(request):
    return render(request, 'users/test.html')


def loggedInUser(request):
    if 'username' in request.session:
        username = request.session['username']
        currentUser = User.objects.get(username = username)
        return currentUser
    else:
         return redirect('test')