from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class UserSettings(models.Model):
    UserAccount = models.ForeignKey(User,unique=True,verbose_name="IdAccount",on_delete=models.CASCADE)
    DisplayName = models.CharField(max_length=50,null=False)
    
    def __str__(self):
        return self.UserAccount.username

    class Meta:
       db_table = "UserSettings"