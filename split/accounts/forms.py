# default django imports for the formset_factory
from django import forms
from django.forms import ModelForm, extras
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# allows user to link bank accounts through account number and routing Number
class LinkLoginForm(forms.Form):
    bank_code_choices = (('ally', 'Ally Bank'),
                         ('arvest', 'Associated Bank'),
                         ('bofa', 'Bank of America'),
                         ('boftw', 'Bank of the West'),
                         ('capone', 'Capital One'),
                         ('capone360', 'Capital One 360'),
                         ('chase', 'Chase'),
                         ('citi', 'Citibank'),
                         ('citizens', 'Citizens Bank'),
                         ('fidelity', 'Fidelity'),
                         ('firsthawaiian', 'First Hawaiian Bank'),
                         ('gobank', 'GoBank'),
                         ('hsbc', 'HSBC Bank'),
                         ('mtb', 'M&T Bank'),
                         ('nfcu', 'Navy Federal Credit Union'),
                         ('svb', 'Silicon Valley Bank'),
                         ('synchrony', 'Synchrony Bank'),
                         ('td', 'TD Bank'),
                         ('union', 'Union Bank'),
                         ('us', 'US Bank'),
                         ('usaa', 'USAA'),
                         ('wells', 'Wells Fargo'))
    bank_code = forms.TypedChoiceField(choices=bank_code_choices)
    bank_id = forms.CharField(max_length=100, label="Bank Username")
    bank_password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label="Bank Password")

# allows user to link bank accounts through bank login
class LinkRoutingForm(forms.Form):
    type_choices = (('PERSONAL', 'PERSONAL'),
                    ('BUSINESS', 'BUSINESS'))
    class_choices = (('CHECKING', 'CHECKING'),
                       ('SAVINGS', 'SAVINGS'))
    accountName = forms.CharField(
        max_length=100, label="Account Name"
    )
    routingNumber = forms.CharField(max_length=22, label="Routing Number")
    accountNumber = forms.CharField(max_length=22, label="Account Number")
    account_class = forms.TypedChoiceField(
        choices = class_choices,
        label = 'Class'
    )
    account_type = forms.TypedChoiceField(
        choices = type_choices,
        label = 'Type'
    )
