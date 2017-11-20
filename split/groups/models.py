from django.db import models
from django.contrib.auth.models import User, UserManager

# Group will store all of the groups info that is created in the app
class Group(models.Model):
    name = models.CharField(max_length = 25)
    description = models.CharField(max_length = 250, null=True)
    location = models.CharField(max_length = 40, null=True)
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
