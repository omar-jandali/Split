from django import forms
from django.forms import ModelForm, extras
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# import all models
from .models import *

# form for creating a new group
class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'location', 'description']

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
