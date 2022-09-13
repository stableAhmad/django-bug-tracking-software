from django.db import models
from django import forms
from team.models import team 

class user(models.Model):

    firstname = models.CharField(null=False,blank=False, max_length=20)
    lastname = models.CharField(null=False, blank=False, max_length=20)
    mail = models.EmailField(null=False,blank=False)
    password = models.CharField(null=False, blank=False , max_length=20)
    team = models.ForeignKey(team , blank = True, null=True,on_delete = models.SET_NULL)
    bugsreported = models.IntegerField()
    bugsclosed = models.IntegerField()
