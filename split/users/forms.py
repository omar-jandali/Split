# default django imports for the formset_factory
from django import forms
from django.forms import ModelForm, extras
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from localflavor.us.forms import USStateField, USPhoneNumberField, USZipCodeField
 
# all model imports related to this project
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class SignupForm(forms.ModelForm):
    username = forms.CharField(
        max_length=16,
        help_text="4 - 16 characters, (Aa-Zz), (0-9), (@), (.), (+), (-). (_)")
    password = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput,
        help_text='Must be 8 - 16 characters')
    verify = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput,
        help_text='Must match password')
    class Meta:
        model = User
        fields = ['username', 'password', 'verify', 'email']

class ProfileForm(forms.ModelForm):
    gender_choices = (('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Other'))
    account_choices = (('INDIVIDUAL', 'Individual'),
                       ('BUSINESS', 'Business'))
    f_name = forms.CharField(label='First Name')
    l_name = forms.CharField(label='Last Name')
    bio = forms.CharField(label='Bio')
    dob = forms.DateField(
        label='Date of Birth',
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )
    gender = forms.TypedChoiceField(
        choices = gender_choices,
        label='Gender'
    )
    account = forms.TypedChoiceField(
        choices = account_choices
    )
    class Meta:
        model = Profile
        fields = ['f_name', 'l_name', 'bio', 'dob', 'gender', 'phone', 'account']

class VerifyPersonalForm(forms.ModelForm):
    dba = forms.CharField(label='Company')
    lob = forms.CharField(label='Occupation')
    street = forms.CharField(label='Street')
    city = forms.CharField(label='City')
    ssn = forms.IntegerField(label='SSN - Last 4')
    class Meta:
        model = Profile
        fields = ['dba', 'lob', 'street', 'city', 'state', 'zip_code']

class VerifyBusinessForm(forms.ModelForm):
    dba = forms.CharField(label='Company')
    lob = forms.CharField(label='Industry')
    street = forms.CharField(label='Street')
    city = forms.CharField(label='City')
    tin = forms.IntegerField(label='TIN/EIN')
    class Meta:
        model = Profile
        fields = ['dba', 'lob', 'street', 'city', 'state', 'zip_code']
