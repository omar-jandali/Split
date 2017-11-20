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
from .models import *

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
                return redirect('groups')
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
                return redirect('profile')
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

# ensure someone is logged in
@login_required(login_url='/login/')
# setup user profile
def profile(request):
    # assign the logged in user as User
    User = request.user
    # check for form submission
    if request.method == 'POST':
        # grab the form
        form = ProfileForm(request.POST)
        # validate form content
        if form.is_valid():
            # cleaned version of the form content
            cd = form.cleaned_data
            # assign all the form fields
            f_name = cd['f_name']
            l_name = cd['l_name']
            bio = cd['bio']
            dob = cd['dob']
            gender = cd['gender']
            phone = cd['phone']
            account = cd['account']
            # create a profile for the user
            profile = Profile.objects.create(
                user = User,
                f_name = f_name,
                l_name = l_name,
                bio = bio,
                gender = gender,
                phone = phone,
            )
            # redirect user to verify based on account type
            if account == 'INDIVIDUAL':
                # personal account
                return redirect('personal')
            if account == 'BUSINESS':
                # business account
                return redirect('business')
        else:
            # if form is not valid redirect to testing page
            return redirect('test')
    else:
        # initial profile form
        form = ProfileForm()
        # parameters to pass to the html template
        parameters = {
            'form':form,
        }
        # render the profile form for user to fill out
        return render(request, 'users/profile.html', parameters)

# ensure someoene is logged in
@login_required(login_url='/login/')
# verify users information
def verify_personal(request):
    # grab the logged in user
    User = request.user
    # check to see if form was submitted
    if request.method == 'POST':
        # grab the submitted form
        form = VerifyPersonalForm(request.POST)
        # validate the inputs
        if form.is_valid():
            # grab the cleaned version of form
            cd = form.cleaned_data
            # assign all of the values
            dba = cd['dba']
            lob = cd['lob']
            street = cd['street']
            city = cd['city']
            state = cd['state']
            zip_code = cd['zip_code']
            # grab the users existing Profile
            profile = Profile.objects.get(user = User)
            # update profile object
            update_profile = profile
            update_profile.dba = dba
            update_profile.lob = lob
            update_profile.street = street
            update_profile.city = city
            update_profile.zip_code = zip_code
            update_profile.save()
            # redirect to users home page
            return redirect('groups')
        else:
            # redirect to test if invaid form
            return redirect('test')
    else:
        # the form to be submitted
        form = VerifyPersonalForm()
        # content passed to the html page
        parameters = {
            'form':form,
        }
        # render initial form for user to fill out
        return render(request, 'users/personal.html', parameters)

# make sure someone is logged in
@login_required(login_url='/login/')
# add busines verification to project
def verify_business(request):
    # grab the logged in user
    User = request.user
    # check to see if form was submitted
    if request.method == 'POST':
        # grab the submitted form
        form = VerifyBusinessForm(request.POST)
        # validate the inputs
        if form.is_valid():
            # grab the cleaned version of form
            cd = form.cleaned_data
            # assign all of the values
            dba = cd['dba']
            lob = cd['lob']
            street = cd['street']
            city = cd['city']
            state = cd['state']
            zip_code = cd['zip_code']
            # grab the users existing Profile
            profile = Profile.objects.get(user = User)
            # update profile object
            update_profile = profile
            update_profile.dba = dba
            update_profile.lob = lob
            update_profile.street = street
            update_profile.city = city
            update_profile.zip_code = zip_code
            update_profile.save()
            # redirect to users home page
            return redirect('groups')
        else:
            print(form.errors)
            return redirect('test')
    else:
        # the form to be submitted
        form = VerifyBusinessForm()
        # everyting that is passed to html template
        parameters = {
            'form':form,
        }
        # render the template for user to fill out
        return render(request, 'users/business.html', parameters)

# ensure someoene is logged in
@login_required(login_url='/login/')
# the users home page
def user_home(request):
    # grab the current user
    user = request.user
    # grab the users Profile
    profile = Profile.objects.get(user = user)
    # grab all of the request that the logged in user has
    requests = Request.objects.filter(requested = user).all()
    # list of all the users friends
    friender = Friend.objects.filter(user = user.username).all()
    friended = Friend.objects.filter(friend = user).all()
    friends = friender | friended
    # parameters to pass to html template
    parameters = {
        'user':user,
        'profile':profile,
        'requests':requests,
        'friends':friends
    }
    # first template
    return render(request, 'users/home.html', parameters)

# ensure someone is logged in
@login_required(login_url='/login/')
# a users Profile
def search_user(request):
    #check to see if form was submitted
    if request.method == 'POST':
        # grab the view_user form
        searched = request.POST['searched']
        # search for the username in the database
        view = User.objects.filter(username = searched).first()
        # validate if there is a user with username
        if view == None:
            # if no user with username, print error
            print('invalid username')
            # redirect logged in user to home
            return redirect('home')
        else:
            # redirect to the users profile if the username is valid
            return redirect('user_profile', username=view.username)

# ensure someone is logged in
@login_required
# view any users profile
def user_profile(request, username):
    # grab the valid username from the user url
    view = User.objects.filter(username = username).first()
    # validate searched Username
    if view == None:
        # redirect if no user with username
        return redirect('home')
    # grab selected users profile
    profile = Profile.objects.get(user = view)
    # pass all the required info to the template
    parameters = {
        'view':view,
        'profile':profile,
    }
    # render the users profile template with users information
    return render(request, 'users/view_profile.html', parameters)

# ensure that soeone is logged in
@login_required
# send requests between two users
def send_request(request, username):
    # grab the current user logged in
    requester = request.user
    # grab the user that was passed in the url
    requested = User.objects.filter(username = username).first()
    # validate the user that was passed through
    if requested == None:
        # if invalid, redirect to testing page
        return redirect('test')
    else:
        # if valid, create a new request objects between the two users
        new_request = Request.objects.create(
            user = requester.username,
            requested = requested,
        )
        # return home
        return redirect('home')

# ensure that someone is logged in
@login_required
# accept a friends request
def accept_request(request, username):
    # grab the logged in user
    user = request.user
    # grab the user object of the person whose friend request is being accepted
    accepted = User.objects.get(username = username)
    # check to see that there is a friend request
    request = Request.objects.filter(requested = user).filter(user = accepted.username).first()
    # if the friend request is valid process the acceptance
    if request:
        # create a friends object that will make the two users friends
        new_friend = Friend.objects.create(
            user = user.username,
            friend = accepted
        )
        # delete the request that was sent
        request.delete()
        # send the user back to home page
        return redirect('home')
    else:
        # if invalid friend request, sent user back to test
        return redirect('test')

# ensure someone is logged in
@login_required
# decline a friend request sent to you
def decline_request(request, username):
    # grab the logged in user
    user = request.user
    # grab the user object of the person whose friend request was being declined
    declined = User.objects.get(username = username)
    # check to see if there is a friend request
    request = Request.objects.filter(requested = user).filter(user = declined.username).first()
    # if the friend request is valid, process the request
    if request:
        # delete the friend request from teh database
        request.delete()
        # redirect the user to home
        return redirect('home')
    else:
        # if not valid, return the user to the test page
        return redirect('test')

# ensure someoene is logged in
@login_required(login_url='signup')
# the logout screen
def user_logout(request):
    # logout of session
    logout(request)
    return redirect('login')
