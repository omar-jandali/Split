from django.db import models
from django.contrib.auth.models import User, UserManager

# Synapse Accounts locally stores a users linked accounts through login or an/rn
class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Bank Account')
    account_id = models.CharField(max_length=100, default='00000')
    account_class = models.CharField(max_length=50, default='Checking')
    bank_name = models.CharField(max_length=150, default='DefaultBank')
    balance = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    main = models.IntegerField(default=1)
    # 1 = standard
    # 2 = default
    create = models.DateTimeField(auto_now_add=True)
