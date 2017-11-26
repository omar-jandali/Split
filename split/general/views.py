# sandard import statements for utility usage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from random import randint
from decimal import Decimal

from synapse_pay_rest import Client, Node, Transaction
from synapse_pay_rest import User as SynapseUser
from synapse_pay_rest.models.nodes import AchUsNode

def test(request):
    return render(request, 'users/test.html')

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
