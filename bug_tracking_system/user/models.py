from django.db import models
from django import forms


class user(models.Model):
    firstname = models.CharField(null=False,blank=False, max_length=20)
    lastname = models.CharField(null=False, blank=False, max_length=20)
    mail = models.EmailField(null=False,blank=False)
    password = models.TextField(null=False, blank=False)
    teamleader = models.CharField()
    bugsreported = models.IntegerField()
    bugsclosed = models.IntegerField()
