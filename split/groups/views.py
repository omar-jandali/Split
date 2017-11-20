# sandard import statements for utility usage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# import all references from this specific app
from .forms import *
from .models import *

# ensure someone is logged in
@login_required
# groups home page
def groups_home(request):
    # grab the logged in user
    user = request.user
    return render(request, 'groups/groups.html')
