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
