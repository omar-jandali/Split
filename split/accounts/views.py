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

# import neccesary apps files
from users.method import test
from users.models import Profile
from groups.views import generate_number

# synapse import statements that are needed
from synapse_pay_rest import Client, Node, Transaction
from synapse_pay_rest import User as SynapseUser
from synapse_pay_rest.models.nodes import AchUsNode

# the following are all of the different credentials that are needed in order to
# initiate the connect between the api and opentab
APP_CLIENT_ID = 'client_id_SOJMCFkagKAtvTpem0ZWPRbwznQ2yc5h0dN6YiBl'
APP_CLIENT_SECRET = 'client_secret_muUbizcGBq2oXKQTMEphg0S4tOyH5xLYNsPkC3IF'
APP_FINGERPRINT = '599378e9a63ec2002d7dd48b'
APP_IP_ADRESS = '127.0.0.1'

# the following are going to be all of the different credentials that are going
# to be needed in order to establish connection
args = {
    'client_id':APP_CLIENT_ID,
    'client_secret':APP_CLIENT_SECRET,
    'fingerprint':APP_FINGERPRINT,
    'ip_address':APP_IP_ADRESS,
    'development_mode':True,
    'logging':False,
}

# this is the call that takes the credentials and sends the connect request to
# validate credentials
client = Client(**args)

def account_test(request):
    return redirect('test')

# ensure someone i slogged in
@login_required
# link an account with synapse
def accounts(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    accounts = SynapseAccounts.objects.filter(user = user).all()
    parameters = {
        'accounts':accounts,
    }
    return render(request, 'accounts/accounts.html', parameters)

# enuser someoen is logged in
@login_required
# create a synsep user though api
def create_user_synapse(request):
    # grab the loggged in user
    user = request.user
    # grab users profile
    profile = Profile.objects.get(user = user)
    # assign values that will be passed
    legal_name = profile.f_name + " " + profile.l_name
    note = legal_name + " has just created his synapse profile "
    supp_id = generate_number()
    cip_tag = user.id
    # the following is all of the information that is required in order to make a
    # new user within the Synapse application
    args = {
        'email':str(user.email),
        'phone_number':str(profile.phone),
        'legal_name':str(legal_name),
        'note': str(note),
        'supp_id':str(supp_id),
        'is_business':False,
        'cip_tag':cip_tag,
    }
    # the following is the request to the synapse api as well as the returned
    # json that contains information that needs to ba saved in local database
    create_user = SynapseUser.create(client, **args)
    response = create_user.json
    # the following updates the current profile to add the users synapse id within
    # the local database.
    if response:
        synapse_id = response['_id']
        update_profile = profile
        update_profile.synapse_id = synapse_id
        update_profile.save()

# ensure someone i slogged in
@login_required
# link an account with synapse
def link_login(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    user_id = profile.synapse_id
    synapseUser = SynapseUser.by_id(client, str(user_id))
    if request.method == 'POST':
        bank_id = 'synapse_good'
        bank_pw = 'test1234'
        bank_code = 'fake'
        args = {
            'bank_name':bank_code,
            'username':bank_id,
            'password':bank_pw,
        }
        ach_us = AchUsNode.create_via_bank_login(synapseUser, **args)
        verification = ach_us.mfa_verified
        if verification == False:
            ach_us.mfa_message
            nodes = ach_us.answer_mfa('test_answer')
            ach_us.mfa_verified
        local_accounts(request)
        return redirect('accounts')
    else:
        form = LinkLoginForm()
        parameters = {
            'form':form,
        }
    return render(request, 'accounts/link_login.html', parameters)

# ensure someone i slogged in
@login_required
# link an account with synapse
def link_routing(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    user_id = profile.synapse_id
    synapseUser = SynapseUser.by_id(client, str(user_id))
    if request.method == 'POST':
        required = {
            'nickname': 'Fake Account',
            'account_number': '1232225674134',
            'routing_number': '051000017',
            'account_type': 'PERSONAL',
            'account_class': 'CHECKING'
        }
        account = AchUsNode.create(synapseUser, **required)
        local_accounts(request)
        return redirect('accounts')
    else:
        form = LinkRoutingForm()
        parameters = {
            'form':form,
        }
    return render(request, 'accounts/link_routing.html', parameters)

@login_required
def local_accounts(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    user_id = profile.synapse_id
    synapseUser = SynapseUser.by_id(client, str(user_id))
    options = {
        'page':1,
        'per_page':20,
        'type': 'ACH-US',
    }
    nodes = Node.all(synapseUser, **options)
    for node in nodes:
        node_json = node.json
        node_id = node_json['_id']
        node_name = node_json['info']['nickname']
        node_class = node_json['info']['class']
        node_bank_name = node_json['info']['bank_name']
        node_balance = node_json['info']['balance']['amount']
        node_currency = node_json['info']['balance']['currency']
        account = SynapseAccounts.objects.filter(user = user).filter(account_id = node_id).first()
        if account == None:
            new_accout = SynapseAccounts.objects.create(
                user = user,
                name = node_name,
                account_id = node_id,
                account_class = node_class,
                bank_name = node_bank_name,
                balance = node_balance,
                main = 1
            )
        if account:
            if account.balance != node_balance:
                update_account = account
                update_account.balance = node_balance
                update_account.save()
