# standard import statements
from accounts.views import create_user_synapse
from general.views import *
from .forms import *
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
                # new activity description
                description = 'Welcome ' + user.username + ' to your new Split Account'
                # new activity object to store in database
                activity = UserActivity.objects.create(
                    user = user,
                    description = description,
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
                business = account,
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
    user = request.user
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
            profile = Profile.objects.get(user = user)
            # update profile object
            update_profile = profile
            update_profile.dba = dba
            update_profile.lob = lob
            update_profile.street = street
            update_profile.city = city
            update_profile.zip_code = zip_code
            update_profile.save()
            # create synapse user
            create_user_synapse(request)
            # new activity description
            description = ' Finished setup and verification of your personal account '
            # creating a new activity object
            activity = UserActivity(
                user = user,
                description = description,
            )
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
            # new activity description
            description = ' Finished setup and verification of your business account '
            # creating a new activity object
            activity = UserActivity(
                user = user,
                description = description,
            )
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
    # list of users actiivties
    activities = UserActivity.objects.filter(user = user).all()
    # parameters to pass to html template
    parameters = {
        'user':user,
        'profile':profile,
        'requests':requests,
        'friends':friends,
        'activities':activities
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
    # person sending the request
    requester = request.user
    # grab the user that was passed in the url
    # person receiving the request
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
        # request activity description
        description = requester.username + ' has sent you a friend request '
        # the activity object
        activity = UserActivity.objects.create(
            user = requested,
            description = description,
            request = new_request,
            category = 2
        )
        # activity for the sender of the friend request
        description_user = 'You have sent ' + requested.username + ' a friend request'
        # activity creation
        activity = UserActivity.objects.create(
            user = requester,
            description = description_user,
            category = 2,
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
        # description for person who accepted the request
        description =  ' You and ' + accepted.username + ' are now friends'
        # the activity object
        activity = UserActivity.objects.create(
            user = user,
            description = description
        )
        # description for user who had his request accepted
        description = ' You and ' + user.username + ' are now friends '
        # the activity object
        activity = UserActivity.objects.create(
            user = accepted,
            description = description
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

#ensure someone is logged in
@login_required
# edit a users settings
def update_profile(request):
    # grab the logged in user
    user = request.user
    # grab the users profile
    profile = Profile.objects.get(user = user)
    # commented during initial testing because of dumplcate objects
    privacy = Privacy.objects.filter(user = user).first()
    passwordMessage = ''
    # check to see if the form is submitted
    if request.method == "POST":
        # check if the user updated his info
        if 'userSubmit' in request.POST:
            # grab the first user form after submission
            updateUserOne = AccountUpdateForm(request.POST)
            # check for validation
            if updateUserOne.is_valid():
                # clean the data
                cd = updateUserOne.cleaned_data
                # grab thee content
                username = cd['username']
                email = cd['email']
            # grab the second user form after submission
            updateUserTwo = UserUpdateForm(request.POST)
            # check the validation
            if updateUserTwo.is_valid():
                # clean the data
                cd = updateUserTwo.cleaned_data
                # grab the content
                first_name = cd['first_name']
                last_name = cd['last_name']
                bio = cd['bio']
                # update the users objects to new info
                update_user = user
                update_user.username = username
                update_user.email = email
                update_user.save()
                update_profile = profile
                update_profile.first_name = first_name
                update_profile.last_name = last_name
                update_profile.bio = bio
                update_profile.save()
                # update the users session informaiton saved
                updateSessionUsername(request, update_user.username)
                # new activity for updating your profile
                description = 'You have updated your user profile'
                user_profile_update = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )
                # go back home
                return redirect('home_page')
        # check to see if password was updated
        if 'passwordSubmit' in request.POST:
            # grab the submitted form
            updatePassword = PasswordUpdateForm(request.POST)
            # check to see if the form is validated
            if updatePassword.is_valid():
                # grab the cleaned data
                cd = updatePassword.cleaned_data
                # grab the form info
                current_password = cd['current_password']
                new_password = cd['new_password']
                verify_password = cd['verify_password']
                # authenticate the old password before storing the new password
                user = authenticate(username=currentUser.username, password=current_password)
                # check to see if user is valid
                if user:
                    # check to see if the new and verify passwords are the same
                    if new_password == verify_password:
                        # has the passowrd
                        secured_password = make_password(new_password)
                        # update the users password
                        update_user = user
                        update_user.password = secured_password
                        update_user.save()
                        # new activity for updating your profile
                        description = 'You have updated your password'
                        user_profile_update = UserActivity.objects.create(
                            user = currentUser,
                            description = description,
                            status = 1
                        )
                        # go back to the home page
                        return redirect('home_page')
                    else:
                        # error message
                        passwordMessage = 'The two passwords do not match'
                        # if the passwords do no match
                else:
                    # error message
                    passwordMessage = 'Current password does not match our records'
                    # in case the old password is not what is saved in the database
        # grab the info submited
        if 'infoSubmit' in request.POST:
            # grab the submiited form
            updateInfo = InfoUpdateForm(request.POST)
            # check if form is validated
            if updateInfo.is_valid():
                # clean data from form
                cd = updateInfo.cleaned_data
                # grab the form information
                phone = cd['phone']
                dob = cd['dob']
                street = cd['street']
                city = cd['city']
                state = cd['state']
                zip_code = cd['zip_code']
                # update the exisitng profile
                update_profile = profile
                update_profile.phone = phone
                update_profile.dob = dob
                update_profile.street = street
                update_profile.city = city
                update_profile.state = state
                update_profile.zip_code = zip_code
                update_profile.save()
                # new activity for updating your profile
                description = 'You have updated your profile info'
                user_profile_update = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )
                # send user to home page
                return redirect('home_page')
        # grab the privacy for that was submiited
        if 'privacySubmit' in request.POST:
            # grab the form
            updatePrivacy = PrivacyUpdateForm(request.POST)
            # validate the form
            if updatePrivacy.is_valid():
                # clean the form data
                cd = updatePrivacy.cleaned_data
                # grab the content
                groups = cd['groups']
                friends = cd['friends']
                expenses = cd['expenses']
                searchable = cd['searchable']
                # upate the privacy
                update_privacy = privacy
                update_privacy.groups = groups
                update_privacy.friends = friends
                update_privacy.expenses = expenses
                update_privacy.searchable = searchable
                update_privacy.save()
                # new activity for updating your profile
                description = 'You have updated your privacy settings'
                user_profile_update = UserActivity.objects.create(
                    user = currentUser,
                    description = description,
                    status = 1
                )
                # send the user to the home page
                return redirect('home_page')
    AccountUpdate = AccountUpdateForm(instance=user)
    UserUpdate = UserUpdateForm(instance=profile)
    PasswordUpdate = PasswordUpdateForm()
    InfoUpdate = InfoUpdateForm(instance=profile)
    PrivacyUpdate = PrivacyUpdateForm()
    parameters = {
        'user':user,
        'profile':profile,
        'privacy':privacy,
        'AccountUpdate':AccountUpdate,
        'UserUpdate':UserUpdate,
        'PasswordUpdate':PasswordUpdate,
        'InfoUpdate':InfoUpdate,
        'PrivacyUpdate':PrivacyUpdate,
        'passwordMessage':passwordMessage,
    }
    return render(request, 'users/update_profile.html', parameters)

# ensure someoene is logged in
@login_required(login_url='signup')
# the logout screen
def user_logout(request):
    # logout of session
    logout(request)
    return redirect('login')
