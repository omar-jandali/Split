# standard imports
from users.models import Profile
from groups.models import GroupActivity, Expense, Group, Member
from general.views import *
from .forms import *
from .models import *

# synapse imports
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

# ensure someone i slogged in
@login_required
# link an account with synapse
def accounts(request):
    user = request.user
    profile = Profile.objects.get(user = user)
    accounts = Accounts.objects.filter(user = user).all()
    parameters = {
        'profile':profile,
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
        print(synapse_id)
        update_profile = profile
        update_profile.synapse_id = synapse_id
        update_profile.save()

    # grab the users synpase id
    user_id = profile.synapse_id
    # send a request to retreive the users synapse account
    synapseUser = SynapseUser.by_id(client, str(user_id))
    options = {
        'email': 'test@test.com',
        'phone_number': '901.111.1111',
        'ip': '127.0.0.1',
        'name': legal_name,
        'alias': 'Test',
        'entity_type': 'M',
        'entity_scope': 'Arts & Entertainment',
        'day': 2,
        'month': 5,
        'year': 1989,
        'address_street': '1 Market St',
        'address_city': 'SF',
        'address_subdivision': 'CA',
        'address_postal_code': '94114',
        'address_country_code': 'US'
    }

    base_document = SynapseUser.add_base_document(synapseUser, **options)
    value = 'https://www.facebook.com/valid'
    url = 'https://cdn.synapsepay.com/static_assets/logo@2x.png'
    # social_document = base_document.add_social_document(type= 'FACEBOOK', value=value)
    # virtual_document = base_document.add_virtual_document(type='SSN', value='2222')
    physical_document = base_document.add_physical_document(type='GOVT_ID', url=url)

# ensure someone i slogged in
@login_required
# link an account with synapse
def link_login(request):
    # grab the logged in user
    user = request.user
    # grab the users profile
    profile = Profile.objects.get(user = user)
    # grab the users synpase id
    user_id = profile.synapse_id
    # check to see if form was submitted
    if request.method == 'POST':
        # send a request to retreive the users synapse account
        synapseUser = SynapseUser.by_id(client, str(user_id))
        # set the testing information
        bank_id = 'synapse_good'
        bank_pw = 'test1234'
        bank_code = 'fake'
        # pass all of the arguments for the request
        args = {
            'bank_name':bank_code,
            'username':bank_id,
            'password':bank_pw,
        }
        # submit the request to link an account through login
        ach_us = AchUsNode.create_via_bank_login(synapseUser, **args)
        # check to see if it needs verification
        verification = ach_us.mfa_verified
        # if it needs verification - verify
        if verification == False:
            # the following is for all the required verification
            ach_us.mfa_message
            nodes = ach_us.answer_mfa('test_answer')
            ach_us.mfa_verified
        # grab the linked accounts and save locally
        local_accounts(request)
        return redirect('accounts')
    else:
        # the form to be submiited by the user
        form = LinkLoginForm()
        # all of the parameters for the html template
        parameters = {
            'form':form,
        }
        # render the html template
        return render(request, 'accounts/link_login.html', parameters)

# ensure someone i slogged in
@login_required
# link an account with synapse
def link_routing(request):
    # grab the logged in user
    user = request.user
    # grab the users profiel
    profile = Profile.objects.get(user = user)
    # grab the users synapse account from database
    user_id = profile.synapse_id
    # check to see if the form was submitted
    if request.method == 'POST':
        # send a request to retreice the users synapse record
        synapseUser = SynapseUser.by_id(client, str(user_id))
        # the following are all of the defauly testing linking account info
        required = {
            'nickname': 'Fake Account',
            'account_number': '1232225674134',
            'routing_number': '051000017',
            'account_type': 'PERSONAL',
            'account_class': 'CHECKING'
        }
        # the following is the request that links the account
        # through routing and account number
        account = AchUsNode.create(synapseUser, **required)
        # saves the new linked accounts locally
        local_accounts(request)
        return redirect('accounts')
    else:
        # the from to be submiited
        form = LinkRoutingForm()
        # the parameters that need to be passed to the html tempalte
        parameters = {
            'form':form,
        }
        # render the html template
        return render(request, 'accounts/link_routing.html', parameters)

# ensure someone is looged in
@login_required
# create transactions between two user accounts
def create_transaction(request, activityid):
    # grab the logged in user
    user = request.user
    # grab the users profile
    profile = Profile.objects.get(user = user)
    # grab the realted activity and expense
    activity = GroupActivity.objects.get(id = activityid)
    group = activity.group
    expense = activity.expense
    print(activity)
    print(group)
    print(expense)
    # store the users synapse account
    user_id = profile.synapse_id
    synapseUser = SynapseUser.by_id(client, str(user_id))
    print(synapseUser)
    # grab the users default accont
    account = Accounts.objects.filter(user = user).filter(main = 2).first()
    node = Node.by_id(synapseUser, str(account.account_id))
    print(node)
    # find the groups host
    member = Member.objects.filter(group = group).filter(status = 1).first()
    # grab the host member
    host = member.user
    host_account = Accounts.objects.filter(user = host).filter(main = 2).first()
    print(host_account)
    # set the transaction inforaiton
    args = {
        'to_type': 'ACH-US',
        'to_id': str(host_account.account_id),
        'amount': str(expense.amount),
        'currency': 'USD',
        'ip': '127.0.0.1',
        'same_day': True,
        'note': 'hi synapse',
        'supp_id': 'ABC123',
    }
    print(args)
    # create the transaction request
    transaction = Transaction.create(node, **args)
    print(transaction)

# ensure someone is logged in
@login_required
# save account info locally
def local_accounts(request):
    # grab the logged in user
    user = request.user
    # grab the logged in users profile
    profile = Profile.objects.get(user = user)
    # grab the users synapse id from the database
    user_id = profile.synapse_id
    # grab the users synapse account
    synapseUser = SynapseUser.by_id(client, str(user_id))
    # set the options for retreiving the users accout
    options = {
        'page':1,
        'per_page':20,
        'type': 'ACH-US',
    }
    # list of all the users nodes from linked accounts
    nodes = Node.all(synapseUser, **options)
    # cycle through the nodes
    for node in nodes:
        # set the node to json format
        node_json = node.json
        # set all of the different values from the nodes
        node_id = node_json['_id']
        node_name = node_json['info']['nickname']
        node_class = node_json['info']['class']
        node_bank_name = node_json['info']['bank_name']
        node_balance = node_json['info']['balance']['amount']
        node_currency = node_json['info']['balance']['currency']
        # check to see if if the account you connected is already saved
        account = Accounts.objects.filter(user = user).filter(account_id = node_id).first()
        # if the account doesnt exist, create an account
        if account == None:
            # create a new synapse account object saved locally
            new_accout = Accounts.objects.create(
                user = user,
                name = node_name,
                account_id = node_id,
                account_class = node_class,
                bank_name = node_bank_name,
                balance = node_balance,
                main = 1
            )
        # grab the account that is saved
        if account:
            # grab the amount that is stored with the balance
            if account.balance != node_balance:
                # update the balance based on the balance of your bank account though synapse
                update_account = account
                update_account.balance = node_balance
                update_account.save()

# ensure someone is logged in
@login_required
# set defauly account
def set_default(request, accountid):
    # grab the logged in user
    user = request.user
    # grab the selected account
    selected = Accounts.objects.filter(id = accountid).filter(user = user).first()
    if selected == None:
        return redirect('accounts')
    # grab the already set main account
    main = Accounts.objects.filter(user = user).filter(main = 2).first()
    # check if there is already a main
    print(selected)
    print(main)
    if main == None:
        # set the selected account as main
        print('setting main')
        update_account = selected
        update_account.main = 2
        print('main is set')
        update_account.save()
        print('main is saved ')
        return redirect('accounts')
    # check if the main exists
    if main:
        # grab the old main account and set a regular account
        old_main = main
        old_main.main == 1
        old_main.save()
        # grab the new main and set it as main
        new_main = selected
        new_main.main == 2
        new_main.save()
        return redirect('accounts')
