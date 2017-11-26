from django.db import models
from django.contrib.auth.models import User, UserManager
from localflavor.us.models import USStateField, PhoneNumberField, USZipCodeField
# import modesl from other apps
from groups.models import Expense

# the following is the users profile model
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    f_name = models.CharField(max_length=25, default='first')
    l_name = models.CharField(max_length=25, default='last')
    bio = models.CharField(max_length=220, default='bio')
    street = models.CharField(max_length=200, default='street address')
    city = models.CharField(max_length=100, default='city')
    state = USStateField(default='CA')
    zip_code = USZipCodeField(default=12345)
    phone = PhoneNumberField(default=0)  # user
    dob = models.DateField(default='1950-01-01')
    gender = models.CharField(max_length=5, default='Other')
    lob = models.CharField(max_length=40, default='occupation')
    dba = models.CharField(max_length=40, default='comapny')
    business = models.CharField(max_length=20, default='INDIVIDUAL')
    synapse_id = models.CharField(max_length=200, default='123456789')
    created = models.DateTimeField(auto_now_add=True)  # server

# the following is the model for sending friend requests
class Request(models.Model):
    user = models.CharField(max_length=22, default='current user')
    requested = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# the following are models for accepted friend requests
class Friend(models.Model):
    user = models.CharField(max_length=22, default='current user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField(auto_now_add=True)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=150, null=True)
    expense = models.ForeignKey(Expense, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='some action')
    reference = models.IntegerField(default = '101', null = True)
    category = models.IntegerField(default=1)
    status = models.SmallIntegerField(default=1)
    # 1 = unseen
    # 2 = seen
    created = models.DateTimeField(auto_now_add=True)
