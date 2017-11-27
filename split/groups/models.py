from django.db import models
from django.contrib.auth.models import User, UserManager

# Group will store all of the groups info that is created in the app
class Group(models.Model):
    name = models.CharField(max_length = 25)
    description = models.CharField(max_length = 250, null=True)
    created_by = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# Member stores all of the different members to each of the created groups
class Member(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, default=1 , on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)
    # 1 = member
    # 2 - host
    created = models.DateTimeField(auto_now_add=True)

# all of the expense in the application will be stored here
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    description = models.CharField(max_length=200, default = 'expense')
    name = models.CharField(max_length=100, default = 'expense')
    location = models.CharField(max_length=100, default = 'location')
    status = models.SmallIntegerField(default = 1)
    # 1 = unpaid
    # 2 = paid
    reference = models.IntegerField(default = '101', null = True)
    # reference is assigned for single transaction for tracking purposes
    created_by = models.CharField(max_length = 200, default = 'username', null=True)
    created = models.DateTimeField(auto_now_add=True)

# Checklist stores the overall infomraiton about each Checklist
class Bundle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='checklist')
    # total amount required from each person
    total = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    # reference number
    reference = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

# Item saves all of the individal items that make a Checklist
# 1 set of items for a checklist shared by everyone
class Item(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    item = models.CharField(max_length=100, default='item')
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    # reference number
    reference = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

# Group Activity stores all of the actiivty related to a group that was create
class GroupActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, null=True, on_delete=models.CASCADE)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=200, default='some action')
    host = models.CharField(max_length=100, null=True)
    reference = models.IntegerField(default=0)
    category = models.SmallIntegerField(default = 1)
    # 1 - general
    # 2 - specific
    # 3 - no validation
    # 4 - validation
    created = models.DateTimeField(auto_now_add=True)
