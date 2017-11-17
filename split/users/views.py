# sandard import statements for utility usage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# import all references from this specific app
from .forms import *
from .method import *

# the users login  view
def user_login(request):
    # check if the form was submitted 
    if request.method == 'POST':
        # grab the form
        form = LoginForm(request.POST)
        # validation of the form
        if form.is_valid():
            # cleaned up data from form
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            # authenticate with the user record
            user = authenticate(username=username, password=password)
            # check if login credentials are authentic
            if user:
                # login the user to django session
                login(request, user)
                return redirect('home')
            else:
                # re-display form with error message
                # the same form
                form = LoginForm()
                # the error
                error = 'Invalid Username/Password'
                # template parameters to display
                parameters = {
                    'form':form,
                    'error':error
                }
                # re-render the template
                return render(request, 'users/login.html', parameters)
    else:
        # display the form for submission
        form = LoginForm()
        # the template parameters
        parameters = {
            'form':form,
        }
        # render the login template
        return render(request, 'users/login.html', parameters)

# the users signup view
def user_signup(request):
    # check if the form was submitted
    if request.method == "POST":
        # grab the form
        form = SignupForm(request.POST)
        # validation of the form
        if form.is_valid():
            # cleaned up data from form
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            verify = cd['verify']
            email = cd['email']
            # check if the pasword and verify match
            if password == verify:
                # create a hashed password
                secure_password = make_password(password)
                # create and save the user object in db
                user = User.objects.create(
                    username = username,
                    password = secure_password,
                    email = email,
                )
                # login the user that was just created
                login(request, user)
                return redirect('home')
            else:
                # re-display the form after error
                form = SignupForm()
                # form error
                error = ' Passwords don\'t match '
                # the template parameters
                parameters = {
                    'form':form,
                    'error':error
                }
                # re-render the template
                return render(request, 'users/signup.html', parameters)
        else:
            # the validation errors
            error = form.errors
            # re-display the form
            form = SignupForm()
            # the template parameters
            parameters = {
                'form':form,
                'error':error,
            }
            # re-rendper template
            return render(request, 'users/signup.html', parameters)
    else:
        # display the form for signing up
        form = SignupForm()
        # the teplate parameters
        parameters = {
            'form':form
        }
        # render the template
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

# ensure someoene is logged in
@login_required(login_url='/signup/')
# the users home page
def user_home(request):
    # first template
    return render(request, 'users/home.html')

# ensure someoene is logged in
@login_required(login_url='signup')
# the logout screen
def user_logout(request):
    # logout of session
    logout(request)
    return redirect('login')
