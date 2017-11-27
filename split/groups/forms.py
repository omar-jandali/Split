from django import forms
from django.forms import ModelForm, extras
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

# form for creating a new group
class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

# create a new expense form - group
class CreateExpenseForm(forms.ModelForm):
    split_choices = (('1', 'even'),
                      ('2', 'individual'))
    split = forms.TypedChoiceField(
        choices=split_choices
    )
    amount = forms.DecimalField(decimal_places=2,
        max_digits=9,
        label='amount (even split)')
    class Meta:
        model = Expense
        fields = ['name', 'location', 'description', 'amount', 'split']

# this is going to be where indiviual split bills will be submiited
class IndividualExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description']

# the form to create a checklist
class CreateBundleForm(forms.ModelForm):
    item1 = forms.CharField(max_length=50, label='Item')
    item2 = forms.CharField(max_length=50, label='Item')
    item3 = forms.CharField(max_length=50, label='Item')
    amount1 = forms.DecimalField(decimal_places=2, max_digits=9, label='Amount')
    amount2 = forms.DecimalField(decimal_places=2, max_digits=9, label='Amount')
    amount3 = forms.DecimalField(decimal_places=2, max_digits=9, label='Amount')
    class Meta:
        model = Bundle
        fields = ['name', 'item1', 'amount1', 'item2', 'amount2', 'item3', 'amount3']
