from django.db import models
from django import forms

class bug(models.Model):
	description = models.TextField(null = False , blank = False)
	#project  foreign key , later
	publisher = models.CharField(null = False , blank =False, max_length = 30)
	date = models.DateField()
	severity_CHOICES = ["critical", "normal",  "mild"]
	severity = forms.ChoiceField(choices = severity_CHOICES)
	assigned_to  = models.CharField( max_length = 30)
	closed = models.BooleanField()
	#attachment file field , later

