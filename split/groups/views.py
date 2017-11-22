# sandard import statements for utility usage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from random import randint
from decimal import Decimal

# import all references from this specific app
from .models import *
from .forms import *

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
    expenses = Expense.objects.filter(group = group).all()
    # list of bundles
    bundles = Bundle.objects.filter(group = group).all()
    # list of budle items
    items = Item.objects.filter(group = group).all()
    # a list of all the acitivities
    activities = GroupActivity.objects.filter(group = group).all()
    # everything passed to html template
    parameters = {
        'name':name,
        'group':group,
        'members':members,
        'expenses':expenses,
        'bundles':bundles,
        'items':items,
        'activities':activities,
    }
    return render(request, 'groups/group_home.html', parameters)

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
            # description for creating a new group - user activity
            description = 'You created a new group : ' + name
            # this is a new user activity
            activity = UserActivity.objects.create(
                user = user,
                description = description,
                category = 1
            )
            # same description for the group
            group_description_user = 'You created ' + name
            group_description_general = user.username + ' created ' + name
            # activites for creating the group:
            group_user = GroupActivity.objects.create(
                user = user,
                group = new_group,
                description = group_description_user,
                category = 2,
            )
            group_general = GroupActivity.objects.create(
                user = user,
                group = new_group,
                description = group_description_general,
                category = 1
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
                        # the descriptions for the added members
                        description_user = user.username + ' has added you to ' + name
                        description_general = user.username + ' has added ' + selected.username + ' to ' + name
                        # the following are the new activities that are created for the added member
                        user_activity = GroupActivity.objects.create(
                            user = selected,
                            group = new_group,
                            description = description_user,
                            category = 2,
                        )
                        general_activity = GroupActivity.objects.create(
                            user = selected,
                            group = new_group,
                            description = description_general,
                            category = 1,
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
                        # the descriptions for the added members
                        description_user = user.username + ' has added you to ' + name
                        description_general = user.username + ' has added ' + selected.username + ' to ' + name
                        # the following are the new activities that are created for the added member
                        user_activity = GroupActivity.objects.create(
                            user = selected,
                            group = new_group,
                            description = description_user,
                            category = 2,
                        )
                        general_activity = GroupActivity.objects.create(
                            user = selected,
                            group = new_group,
                            description = description_general,
                            category = 1,
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
# create an expense
def create_expense(request, groupid, groupname):
    # grab the user that is logged in
    user = request.user
    # un slugify the group name
    name = groupname.replace('-', ' ')
    # grab the current group
    group = Group.objects.get(id = groupid)
    # grab all the members of the current group
    members = Member.objects.filter(group = group).all()
    # check to see if form was submitted
    if request.method == 'POST':
        # grabs the create expense form
        form = CreateExpenseForm(request.POST)
        # validate the form
        if form.is_valid():
            # clean the form data
            cd = form.cleaned_data
            # grab the form content
            name = cd['name']
            location = cd['location']
            description = cd['description']
            amount = cd['amount']
            split = cd['split']
            # generate the unique referece number
            reference = generate_number()
            # cucle through the members
            for member in members:
                # check to see if the username was checked in the form
                if member.user.username in request.POST:
                    # create a new expense item for each user
                    new_expense = Expense.objects.create(
                        user = member.user,
                        group = group,
                        name = name,
                        location = location,
                        description = description,
                        amount = amount,
                        reference = reference,
                        created_by = user,
                    )
            # check to see how the bill was splut for processing
            if split == '1':
                print('even split')
                # slugify the expenses name
                expensename = name.replace(' ', '-')
                # redirect and process as a even split
                return redirect('even_expense', expensename = expensename, reference = reference)
            # the bill is split individually
            if split == '2':
                print('individual splut')
                # slugify the expense name
                expensename = name.replace(' ', '-')
                # redirect and process as individual from
                return redirect('individual_expense', expensename = expensename, reference = reference)
        else:
            # print any possible errors
            print(form.errors)
            return redirect('test')
    else:
        # the form to be displayed
        form = CreateExpenseForm()
        # everything that needs to be passed to the html tempalte
        parameters = {
            'form':form,
            'members':members,
        }
        # render the html template for creating expenses
        return render(request, 'groups/create_expense.html', parameters)

# ensure someone is logged in
@login_required
# update an even expense
def even_expense(request, expensename, reference):
    # grab the logged in user
    user = request.user
    # unslugify the expense naem that was passed
    name = expensename.replace('-', ' ')
    # grab the current expenses based on reference number
    expenses = Expense.objects.filter(reference = reference).all()
    # grab the expense counts based on number of expenses
    expenses_count = Expense.objects.filter(reference = reference).count()
    # cylce through the expenses
    for expense in expenses:
        # grab the orifinal total amount of the expense
        amount = expense.amount
        # grab the current group
        group = Group.objects.get(id = expense.group.id)
    # split the amount based on number of members
    total = split_even(amount, expenses_count)
    # cycle through expenses
    for expense in expenses:
        # grab each expense
        update_expense = expense
        # update the amount for each expense
        update_expense.amount = total
        # svae the updated expense
        update_expense.save()
        # descriptions for the new expense
        if expense.user != user:
            description_user = 'You owe ' + user.username + ' $' + str(total) + ' for ' + expense.description
            description_general = expense.user.username + ' owes ' + user.username + ' $' + str(total) + ' for ' + expense.description
            # the following are the two new activities for new expenses
            user_activity = GroupActivity.objects.create(
                user = expense.user,
                expense = expense,
                group = group,
                description = description_user,
                category = 4,
            )
            general_activity = GroupActivity.objects.create(
                user = expense.user,
                expense = expense,
                group = group,
                description = description_general,
                category = 1,
            )
    # slugify group name
    groupname = group.name.replace(' ', '-')
    # redirect
    return redirect('group_home', groupid=group.id, groupname=groupname)

# ensure someone is logged in
@login_required
# update expenses for individuals
def individual_expense(request, expensename, reference):
    # grab the logged in user
    user = request.user
    # unslugify the expense name that was passed
    name = expensename.replace('-', ' ')
    # grab all of the expense based on reference number
    expenses = Expense.objects.filter(reference = reference).all()
    # grab the expense count
    expenses_count = Expense.objects.filter(reference = reference).count()
    # create a set of forms based on number of expenses
    SplitFormSet = formset_factory(IndividualExpenseForm, extra=expenses_count)
    # cylce through the expenses
    for expense in expenses:
        # grab the current group
        group = Group.objects.get(id = expense.group.id)
    # check tp see if form was submitted
    if request.method == 'POST':
        # the returned formset
        formSet = SplitFormSet(request.POST)
        # check for submitted tax
        if 'tax' in request.POST:
            # grab the taz
            tax = request.POST['tax']
            # put amount in decimal form
            amount = Decimal(tax)
            # split tax and set to individual split amount
            individual_tax = split_even(amount, expenses_count)
        # check for submitted top
        if 'tip' in request.POST:
            # grab the tip
            tip = request.POST['tip']
            # put amount in decimal form
            amount = Decimal(tip)
            # split tip and set to individual splut amount
            individual_tip = split_even(amount, expenses_count)
        # validation of the formset
        if formSet.is_valid():
            # initialize the count
            count = 0
            # cucle through the formset
            for form in formSet:
                # grab the cleaned data
                cd = form.cleaned_data
                # grabe the form content
                amount = cd['amount']
                description = cd['description']
                # fidn the total amount owed by each user
                total_amount = amount + individual_tip + individual_tax
                # grab the correct expense
                expense = expenses[count]
                # set as update expense
                update_expense = expense
                # update expense amount and description
                update_expense.amount = total_amount
                update_expense.description = description
                # save the current expense
                update_expense.save()
                # increment the count
                # descriptions for the new expense
                if update_expense.user != user:
                    description_user = 'You owe ' + user.username + ' $' + str(total_amount) + ' for ' + expense.description
                    description_general = expense.user.username + ' owes ' + user.username + ' $' + str(total_amount) + ' for ' + expense.description
                    # the following are the two new activities for new expenses
                    user_activity = GroupActivity.objects.create(
                        user = expense.user,
                        expense = expense,
                        group = group,
                        description = description_user,
                        category = 4,
                    )
                    general_activity = GroupActivity.objects.create(
                        user = expense.user,
                        expense = expense,
                        group = group,
                        description = description_general,
                        category = 1
                    )
                count = count + 1
        # slugify group name
        groupname = group.name.replace(' ', '-')
        # redirect to home
        return redirect('group_home', groupid=group.id, groupname=groupname)
    else:
        # the formset to be submitted
        form = SplitFormSet()
        # everything that nees to be passed
        parameters = {
            'form':form,
            'expenses':expenses,
        }
        # render the html template
        return render(request, 'groups/individual_expense.html', parameters)

# ensure that someone is logged in
@login_required
# creating bundle items
def create_bundle(request, groupid, groupname):
    # grab the logged in user
    user = request.user
    # grab the currentgroup
    group = Group.objects.get(id = groupid)
    # group members
    members = Member.objects.filter(group = group).all()
    members_count = Member.objects.filter(group = group).count()
    # generate a reference number
    reference = generate_number()
    # check to see if the form was submitted
    if request.method == 'POST':
        # grab the form submiited
        form = CreateBundleForm(request.POST)
        # validate the form
        if form.is_valid():
            # grab the cleaned data from form
            cd = form.cleaned_data
            # grab the form content
            cd = form.cleaned_data
            name = cd['name']
            amount1 = cd['amount1']
            item1 = cd['item1']
            amount2 = cd['amount2']
            item2 = cd['item2']
            amount3 = cd['amount3']
            item3 = cd['item3']
            count = 0
            for member in members:
                if member.user.username in request.POST:
                    count = count + 1
            split_1 = split_even(amount1, count)
            split_2 = split_even(amount2, count)
            split_3 = split_even(amount3, count)
            total = split_1 + split_2 + split_3
            for member in members:
                if member.user.username in request.POST:
                    new_bundle = Bundle.objects.create(
                        user = member.user,
                        group = group,
                        name = name,
                        reference = reference,
                        total = total
                    )
                    # only create activities for those who are not the host
                    if member.user != user:
                        # descriptions for the new expense
                        description_user = 'You owe ' + user.username + ' $' + str(total) + ' for ' + new_bundle.name
                        description_general = member.user.username + ' owe ' + user.username + ' $' + str(total) + ' for ' + new_bundle.name
                        # the following are the two new activities for new expenses
                        user_activity = GroupActivity.objects.create(
                            user = member.user,
                            bundle = new_bundle,
                            group = group,
                            description = description_user,
                            category = 4,
                            reference = new_bundle.reference,
                        )
                        general_activity = GroupActivity.objects.create(
                            user = member.user,
                            bundle = new_bundle,
                            group = group,
                            description = description_general,
                            category = 1,
                            reference = new_bundle.reference,
                        )
            # create a bundle item pbject to store in database
            new_item = Item.objects.create(
                group = group,
                item = item1,
                amount = split_1,
                reference = reference
            )
            new_item = Item.objects.create(
                group = group,
                item = item2,
                amount = split_2,
                reference = reference
            )
            new_item = Item.objects.create(
                group = group,
                item = item3,
                amount = split_3,
                reference = reference
            )
            return redirect('group_home', groupid = groupid, groupname = groupname)
    else:
        form = CreateBundleForm()
        parameters = {
            'form':form,
            'members':members,
        }
        return render(request, 'groups/create_bundle.html', parameters)

# ensure someone is logged in
@login_required
# verify personal expense
def verify_expense(request, expenseid, activityid):
    # grab the logged in user
    user = request.user
    # grab the expense by id
    expense = Expense.objects.get(id = expenseid)
    # grab the current group
    group = Group.objects.get(id = expense.group.id)
    # update expense from validation to specific
    expense.status = 2
    # save the change
    expense.save()
    # grab the current activity and the one after it - same activity
    activity = GroupActivity.objects.get(id = activityid)
    secondid = activity.id + 1
    second = GroupActivity.objects.get(id = secondid)
    # description for the new activities
    description_user = 'You transfered $' + str(expense.amount) + ' to host for ' + expense.description
    description_group = user.username + ' transfered $' + str(expense.amount) + ' to host for ' + expense.description
    # new activity that will replce the old activities
    user_activity = GroupActivity.objects.create(
        user = user,
        group = expense.group,
        expense = expense,
        description = description_user,
        category = 2
    )
    group_activity = GroupActivity.objects.create(
        user = user,
        group = expense.group,
        expense = expense,
        description = description_group,
        category = 1
    )
    # delete the two old activities
    activity.delete()
    second.delete()
    # slugify the groups name
    groupname = group.name.replace(' ', '-')
    # return to the groups home page after verification
    return redirect('group_home', groupid = group.id, groupname = groupname)

# ensure someone is logged in
@login_required
# verify bundle expenses
def verify_bundle(request, bundleid, activityid):
    # grab the logged in user
    user = request.user
    # grab the bundle
    bundle = Bundle.objects.get(id = bundleid)
    # grab the current activity and the one after it - same activity
    activity = GroupActivity.objects.get(id = activityid)
    secondid = activity.id + 1
    second = GroupActivity.objects.get(id = secondid)
    # description for the new activities
    description_user = 'You transfered $' + str(bundle.total) + ' to host for ' + bundle.name
    description_group = user.username + ' transfered $' + str(bundle.total) + ' to host for ' + bundle.name
    # new activity that will replce the old activities
    user_activity = GroupActivity.objects.create(
        user = user,
        group = bundle.group,
        bundle = bundle,
        description = description_user,
        reference = bundle.reference,
        category = 2
    )
    group_activity = GroupActivity.objects.create(
        user = user,
        group = bundle.group,
        bundle = bundle,
        description = description_group,
        reference = bundle.reference,
        category = 1
    )
    # delete the two old activities
    activity.delete()
    second.delete()
    # slugify groups name
    groupname = bundle.group.name.replace(' ', '-')
    # return to the groups home page after verification
    return redirect('group_home', groupid = bundle.group.id, groupname = groupname)

# split an amount by number
def split_even(amount, count):
    # assign amount and count
    total = amount
    count = count
    # divide the amount by count
    amount = total/count
    # rount the amount that is returned
    rounded_amount = round(amount, 2)
    # return the rounded amount
    return rounded_amount

# generate a random number
def generate_number():
    # select randome int between to values
    reference = randint(1, 2147483646)
    # return the random number returned
    return reference
