# sandard import statements for utility usage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# import all references from this specific app
from .models import *

# import references from other apps
from users.models import *
from users.forms import *

# ensure someone is logged in
@login_required
# groups home page
def groups_home(request):
    # grab the logged in user
    user = request.user
    # grab all of the groups you are a member of
    groups = Member.objects.filter(user = user).all()
    # everythin that is going to be passed to the html template
    parameters = {
        'groups':groups,
    }
    return render(request, 'groups/groups.html', parameters)

# ensure someone is logged in
@login_required
# create a groups
def create_group(request):
    # grab the logged in user
    user = request.user
    # grab the users friends
    friender = Friend.objects.filter(user = user.username).all()
    friended = Friend.objects.filter(friend = user).all()
    friends = friender | friended
    # check to see if the from was submitted
    if request.method == 'POST':
        # grab the submitted form
        form = CreateGroupForm(request.POST)
        # validate form
        if form.is_valid():
            # clean the passed in data
            cd = form.cleaned_data
            # grab the form informaiton
            name = cd['name']
            location = cd['location']
            description = cd['description']
            # create a new group
            new_group = Group.objects.create(
                name = name,
                location = location,
                description = description,
                created_by = user,
            )
            # add founding member and default host
            new_member = Member.objects.create(
                user = user,
                group = new_group,
                status = 2,
            )
            # add selected friends as members
            # go through all friends
            for friend in friends:
                # check friend
                if friend.user == user.username:
                    # grab the friend object
                    selected = friend.friend
                    # check for selected in form
                    if selected.username in request.POST:
                        # create a new member object
                        new_member = Member.objects.create(
                            user = selected,
                            group = new_group,
                            status = 1,
                        )
                # chekc friend
                if friend.friend == user:
                    # grab the user object of the friend
                    selected = User.objects.get(username = friend.user)
                    # validate of the friend was selected
                    if selected.username in request.POST:
                        # create a new member objects
                        new_member = Member.objects.create(
                            user = selected,
                            group = new_group,
                            status = 1,
                        )
            # redirect to the groups home page
            return redirect('groups')
        else:
            # invalid form will redirect to a testing page
            return redirect('test')
    else:
        # the form to be displayed
        form = CreateGroupForm()
        # all of the parameters required
        parameters = {
            'form':form,
            'friends':friends,
        }
        # rendering the html template if form was not submitted
        return render(request, 'groups/create_group.html', parameters)

# ensure someone is logged in
@login_required
# individual groups home page
def group_home(request, groupid, groupname):
    # grab the logged in user
    user = request.user
    # unslugify the group name
    name = groupname.replace('-', ' ')
    # grab all of the groups from the members records
    group = Group.objects.get(id = groupid)
    # validate group passed
    if group.name != name:
        return redirect('groups')
    # grab the group members
    members = Member.objects.filter(group = group).all()
    # everything passed to html template
    parameters = {
        'name':name,
        'group':group,
        'members':members
    }
    return render(request, 'groups/group_home.html', parameters)
