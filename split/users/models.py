from django.db import models
from django.contrib.auth.models import User

from django_localflavor_us.models import USStateField

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # server
    f_name = models.CharField(max_length=25, default='first')
    l_name = models.CharField(max_length=25, default='last')
    bio = models.CharField(max_length=220, default='bio')
    street = models.CharField(max_length=200, default='street address')
    city = models.CharField(max_length=100, default='city')
    state = USStateField(default='CA')
    zip_code = models.IntegerField(default=12345)
    phone = models.BigIntegerField(default=0)  # user
    dob = models.DateField(default='1950-01-01')
    gender = models.CharField(max_length=5, default='Other')
    lob = models.CharField(max_length=40, default='occupation')
    dba = models.CharField(max_length=40, default='comapny')
    synapse_id = models.CharField(max_length=200, default='123456789')
    created = models.DateTimeField(auto_now_add=True)  # server
